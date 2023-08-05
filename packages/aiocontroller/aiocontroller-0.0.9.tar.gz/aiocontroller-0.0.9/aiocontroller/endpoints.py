import inspect
import logging
import re
from abc import ABC
from dataclasses import dataclass
from typing import Callable, Type, Any, Iterator, Optional, Dict, Mapping, \
    MutableMapping, Sequence, MutableSequence, Set, Generic, Iterable, Protocol, runtime_checkable, TypeVar

from aiohttp import web, client
from pydantic import BaseModel, parse_obj_as

from .abstraction import AbstractRequestBuilder, AbstractParamDef, AbstractResultDef, AbstractSignature, \
    AbstractEndpointDef, TController, AbstractEndpointCollection
from .exceptions import WrongReturnType

log = logging.getLogger(__name__)

HTTP_METHODS = {'get', 'post', 'put', 'delete'}


class _UNDEFINED:
    pass


class BaseParamDef(AbstractParamDef, ABC):
    def __init__(self, *,
                 param_info: inspect.Parameter,
                 param_index: int,
                 alias: str | None = None,
                 default: Any = None,
                 default_factory: Optional[Callable] = None,
                 optional: Optional[bool] = None):

        if isinstance(default, AbstractParamDef):
            raise ValueError('default cannot be another parameter definition!')

        self._alias = alias
        self._default = default
        self._default_factory = default_factory
        self._parameter_info = param_info
        self._parameter_index = param_index
        self._is_optional = \
            optional or \
            default is not None or \
            default_factory is not None or \
            self._parameter_info.default != inspect.Parameter.empty

    @property
    def is_kwarg(self) -> bool:
        return self._parameter_info.kind == inspect.Parameter.KEYWORD_ONLY

    @property
    def name(self) -> str:
        return self._parameter_info.name

    @property
    def type(self) -> Type:
        return self._parameter_info.annotation or Any

    @property
    def payload_name(self) -> str:
        return self._alias or self._parameter_info.name

    def get_default_value(self):
        if self._default is not None:
            return self._default

        if self._default_factory:
            return self._default_factory()

        if self._parameter_info.default != inspect.Parameter.empty:
            return self._parameter_info.default

        return None

    def serialize_value(self, v):
        if isinstance(v, BaseModel):
            v = v.dict()

        return v

    def deserialize_value(self, v):
        if v and issubclass(self._parameter_info.annotation, BaseModel):
            v = self._parameter_info.annotation.parse_obj(v)

        return v

    def _read_value(self, mapping: Mapping):
        return mapping.get(self.payload_name)

    def _read(self, mapping: Mapping, args: MutableSequence, kwargs: MutableMapping):
        val = self._read_value(mapping)

        if val is None:
            if not self._is_optional:
                raise RuntimeError(f'request payload is missing a required parameter '
                                   f'{self.name} ({self.payload_name})')
            val = self.get_default_value()
        else:
            val = self.deserialize_value(val)

        if self.is_kwarg:
            kwargs[self.name] = val
        else:
            args.append(val)

    def _write_value(self, mapping: MutableMapping, val):
        mapping[self.payload_name] = val

    def _write(self, mapping: MutableMapping, args: Sequence, kwargs: Mapping):
        if self.is_kwarg:
            val = kwargs.get(self.name)
        else:
            if len(args) > self._parameter_index:
                val = args[self._parameter_index]
            else:
                val = _UNDEFINED

        if val is _UNDEFINED:
            if not self._is_optional:
                raise RuntimeError(f'arguments are missing a required parameter '
                                   f'{self.name} ({self.payload_name})')
            val = self.get_default_value()

        val = self.serialize_value(val)
        self._write_value(mapping, val)


class FromQuery(BaseParamDef):

    def __init__(self,
                 param_info: inspect.Parameter,
                 param_index: int,
                 **kwargs):
        super().__init__(param_info=param_info, param_index=param_index, **kwargs)

    async def deserialize(self, req: web.Request, args: MutableSequence, kwargs: MutableMapping):
        self._read(req.query, args, kwargs)

    def serialize(self, msg: AbstractRequestBuilder, args: Sequence, kwargs: Mapping):
        self._write(msg.query, args, kwargs)


class FromBody(BaseParamDef):

    def __init__(self,
                 param_info: inspect.Parameter,
                 param_index: int,
                 is_root=False,
                 **kwargs):
        """
        :param param_info: the inspected parameter
        :param param_index: index of this parameter in the parameter list.
        :param is_root: a true value indicates this parameter is the FULL body of the request, not just a field in the
                        request body.
        """
        super().__init__(param_info=param_info, param_index=param_index, **kwargs)
        self.is_root = is_root

    def _read_value(self, mapping: Mapping):
        """
        Return the (root) of the mapping, instead of a field from inside it.
        """
        if self.is_root:
            return mapping
        return super()._read_value(mapping)

    def _write_value(self, mapping: MutableMapping, val):
        if self.is_root:
            mapping.update(val)
        else:
            super()._write_value(mapping, val)

    async def deserialize(self, req: web.Request, args: MutableSequence, kwargs: MutableMapping):
        # cache the result for other parameters.
        if not (body := req.get('_body')):
            if req.content_type == 'application/json':
                body = await req.json()
            else:
                body = await req.post()
            req['_body'] = body

        self._read(body, args, kwargs)

    def serialize(self, msg: AbstractRequestBuilder, args: Sequence, kwargs: Mapping):
        self._write(msg.body, args, kwargs)


class FromUrl(BaseParamDef):

    def __init__(self,
                 param_info: inspect.Parameter,
                 param_index: int,
                 **kwargs):
        super().__init__(param_info=param_info, param_index=param_index, **kwargs)

    async def deserialize(self, req: web.Request, args: MutableSequence, kwargs: MutableMapping):
        self._read(req.match_info, args, kwargs)

    def serialize(self, msg: AbstractRequestBuilder, args: Sequence, kwargs: Mapping):
        self._write(msg.url_params, args, kwargs)

    def serialize_value(self, v):
        return str(v)

    def deserialize_value(self, v):
        if self._parameter_info.annotation:
            v = self._parameter_info.annotation(v)
        return v


@dataclass
class Param:
    type: Callable[[inspect.Parameter, int, ...], AbstractParamDef]
    kwargs: Any

    @staticmethod
    def Body(**kwargs):
        return Param(FromBody, kwargs)

    @staticmethod
    def Query(**kwargs):
        return Param(FromBody, kwargs)

    @staticmethod
    def Url(**kwargs):
        return Param(FromBody, kwargs)


class JsonResultDef(AbstractResultDef):
    def __init__(self, return_type: Type[BaseModel]):
        self._type = return_type

    @property
    def type(self) -> Type:
        return self._type

    def deserialize_value(self, value: Any) -> Any:
        return parse_obj_as(self._type, value)

    def serialize_value(self, value: Any) -> Any:
        return self._type.json(value)

    async def deserialize(self, resp: client.ClientResponse) -> Any:
        if resp.content_type == 'application/json':
            data = await resp.json()
        else:
            data = await resp.text()

        return self.deserialize_value(data)

    def serialize(self, result: Any) -> web.Response:
        return web.json_response(text=self.serialize_value(result))


TInnerResult = TypeVar('TInnerResult')


@runtime_checkable
class CustomResult(Protocol[TInnerResult]):
    def __into_web_response__(self) -> web.Response:
        """
        Convert this instance into an aiohttp.web.Response. (Server side)
        """
        raise NotImplementedError()

    @classmethod
    async def __from_web_response__(cls, resp: client.ClientResponse) -> TInnerResult:
        """
        Convert a response from the server into the transferred instance. (Client side)
        """
        raise NotImplementedError()


class CustomResultDef(AbstractResultDef):

    def __init__(self, result_type: Type[CustomResult]):
        self._type = result_type

    @property
    def type(self) -> Type:
        return self._type

    async def deserialize(self, resp: client.ClientResponse) -> Any:
        return self._type.__from_web_response__(resp)

    def serialize(self, result: Any) -> web.Response:
        if not isinstance(result, self._type):
            raise WrongReturnType(self._type, type(result))
        return result.__into_web_response__()


class Signature(AbstractSignature):

    def __init__(self, url_params: Set[str], user_params: Mapping[str, Param], sig_info: inspect.Signature):
        self._params: Dict[str, BaseParamDef] = {}
        self._result: Optional[AbstractResultDef] = None
        self._analyze_signature(url_params, user_params, sig_info)

    @property
    def params(self) -> Sequence[AbstractParamDef]:
        return list(self._params.values())

    @property
    def result(self) -> Optional[AbstractResultDef]:
        return self._result

    async def deserialize_args(self, req: web.Request, args: MutableSequence, kwargs: MutableMapping):
        for param in self.params:
            await param.deserialize(req, args, kwargs)

    def serialize_args(self, msg: AbstractRequestBuilder, args: Sequence, kwargs: Mapping):
        for param in self.params:
            param.serialize(msg, args, kwargs)

    async def deserialize_result(self, resp: client.ClientResponse) -> Any:
        if self.result is None or resp.content_length == 0:
            return None

        return await self.result.deserialize(resp)

    def serialize_result(self, result: Any) -> web.Response:
        if self.result is None:
            return web.Response()

        return self.result.serialize(result)

    def _analyze_signature(self, url_params: Set[str], user_params: Mapping[str, Param],
                           sig: inspect.Signature):
        sig_params = list(sig.parameters.values())

        if len(sig_params) and sig_params[0].name == 'self':
            sig_params = sig_params[1:]

        # construct params
        for i, p in enumerate(sig_params):
            # if the parameter is an url param handle it specially
            if p.name in url_params:
                pdef = FromUrl(p, i)
            # if the parameter was user defined then use that definition
            elif isinstance(p.default, Param):
                pargs = p.default
                pdef = pargs.type(**pargs.kwargs)
            else:
                if pargs := user_params.get(p.name):
                    pdef = pargs.type(p, i, **pargs.kwargs)
                else:
                    pdef = FromBody(p, i)

            self._params[p.name] = pdef

        # construct result parser
        if sig.return_annotation is None or issubclass(sig.return_annotation, type(None)):
            self._result = None
        elif issubclass(sig.return_annotation, CustomResult):
            self._result = CustomResultDef(sig.return_annotation)
        elif issubclass(sig.return_annotation, BaseModel):
            self._result = JsonResultDef(sig.return_annotation)
        else:
            raise TypeError(f'endpoints are required to return None or pydantic.BaseModel.')


class EndpointDef(AbstractEndpointDef):

    def __init__(self, controller_method: Callable):
        self._controller_method = controller_method
        self._http_method = 'get'
        self._route_path = '/'
        # these are manually defined param definitions
        self._user_defined_params: MutableMapping[str, Param] = {}
        # these are defined by analyzing the method signature and including user defined.
        self._signature: Signature | None = None

    @property
    def http_method(self) -> str:
        return self._http_method

    @http_method.setter
    def http_method(self, val: str):
        val = val.lower()
        if val not in HTTP_METHODS:
            supported = ', '.join(HTTP_METHODS)
            raise ValueError(f'{val} is not a supported http method ({supported}).')
        self._http_method = val

    @property
    def route_path(self) -> str:
        return self._route_path

    @route_path.setter
    def route_path(self, val: str):
        if not val.startswith('/'):
            raise ValueError('route_path must begin with /.')
        self._route_path = val

    @property
    def controller_method(self) -> Callable:
        return self._controller_method

    @property
    def user_defined_params(self) -> MutableMapping[str, Param]:
        return self._user_defined_params

    @property
    def signature(self) -> Signature:
        if self._signature is None:
            self._signature = Signature(
                set(re.findall(r'{(\w+)}', self.route_path)),
                self.user_defined_params,
                inspect.signature(self.controller_method))
        return self._signature


class EndpointDefTable(Mapping[Callable, EndpointDef]):

    def __init__(self, prefix: str = ''):
        if prefix.endswith('/'):
            raise ValueError('endpoints prefix should not end with /')

        self._endpoints: Dict[Callable, EndpointDef] = {}
        self._prefix = prefix

    def __getitem__(self, f: Callable) -> EndpointDef:
        if not (e := self._endpoints.get(f)):
            e = EndpointDef(f)
            self._endpoints[f] = e
        return e

    def __iter__(self) -> Iterator[Callable]:
        return iter(self._endpoints)

    def __len__(self) -> int:
        return len(self._endpoints)

    def param(self, name: str, param_cls: Type[AbstractParamDef], **kwargs):
        def ann(f):
            e = self[f]
            e.user_defined_params[name] = Param(param_cls, kwargs)
            return f

        return ann

    def body_param(self, name: str, **kwargs):
        return self.param(name, FromBody, **kwargs)

    def url_param(self, name: str, **kwargs):
        return self.param(name, FromUrl, **kwargs)

    def query_param(self, name: str, **kwargs):
        return self.param(name, FromQuery, **kwargs)

    def endpoint(self, method: str, path: str, handler: Callable = None):
        method = method.lower()
        if method not in HTTP_METHODS:
            raise ValueError(f'{method} is not a valid http method')

        if not path.startswith('/'):
            raise ValueError(f'endpoint path must begin with /')

        def ann(f):
            e = self[f]
            e.http_method = method
            e.route_path = self._prefix + path
            return f

        if handler is None:
            return ann

        ann(handler)

    def post(self, path: str, **kwargs):
        return self.endpoint('post', path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.endpoint('put', path, **kwargs)

    def get(self, path: str, **kwargs):
        return self.endpoint('get', path, **kwargs)


class BoundEndpoints(Generic[TController], AbstractEndpointCollection[TController], Iterable[AbstractEndpointDef]):
    """
    Adapts an EndpointDefTable into an AbstractEndpointCollection.
    """

    def __init__(self, controller_cls: Type[TController], table: EndpointDefTable):
        self._controller_cls = controller_cls
        self._table = table

    def __iter__(self) -> Iterator[AbstractEndpointDef]:
        return iter(self._table.values())

    @property
    def controller_type(self) -> Type[TController]:
        return self._controller_cls
