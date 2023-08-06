import logging
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Callable, Type, Any, Iterable, Optional, Dict, Mapping, \
    MutableMapping, Sequence, MutableSequence, Protocol

from aiohttp import web, client

log = logging.getLogger(__name__)

TController = TypeVar('TController')


class AbstractRequestBuilder(Protocol):
    http_method: str
    route: str
    url_params: Dict
    query: Dict
    body: Dict
    headers: Dict


class AbstractParamDef(ABC):

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def type(self) -> Type: ...

    @abstractmethod
    async def deserialize(self, req: web.Request, args: MutableSequence, kwargs: MutableMapping): ...

    @abstractmethod
    def serialize(self, msg: AbstractRequestBuilder, args: Sequence, kwargs: Mapping): ...


class AbstractResultDef(ABC):

    @property
    @abstractmethod
    def type(self) -> Type: ...

    @abstractmethod
    async def deserialize(self, resp: client.ClientResponse) -> Any: ...

    @abstractmethod
    def serialize(self, result: Any) -> web.Response: ...


class AbstractSignature(ABC):

    @property
    @abstractmethod
    def params(self) -> Sequence[AbstractParamDef]: ...

    @property
    @abstractmethod
    def result(self) -> Optional[AbstractResultDef]: ...

    @abstractmethod
    async def deserialize_args(self, req: web.Request, args: MutableSequence, kwargs: MutableMapping):
        """
        Read values from the req and place into args and kwargs to satisfy the
        controller_method signature.
        :param req:
        :param args:
        :param kwargs:
        :return: None
        """

    @abstractmethod
    def serialize_args(self, msg: AbstractRequestBuilder, args: Sequence, kwargs: Mapping):
        """

        :param msg:
        :param args:
        :param kwargs:
        """

    @abstractmethod
    async def deserialize_result(self, resp: client.ClientResponse) -> Any:
        """
        Read the controller response and return the value, converting it
        to the correct type according to the controller_method signature
        is necessary.
        :param resp:
        :return:
        """

    @abstractmethod
    def serialize_result(self, result: Any) -> web.Response: ...


class AbstractEndpointDef(ABC):
    @property
    @abstractmethod
    def http_method(self) -> str: ...

    @property
    @abstractmethod
    def route_path(self) -> str: ...

    @property
    @abstractmethod
    def controller_method(self) -> Callable: ...

    @property
    @abstractmethod
    def signature(self) -> AbstractSignature: ...


class AbstractEndpointCollection(Generic[TController], Iterable[AbstractEndpointDef], ABC):

    @property
    @abstractmethod
    def controller_type(self) -> Type[TController]: ...
