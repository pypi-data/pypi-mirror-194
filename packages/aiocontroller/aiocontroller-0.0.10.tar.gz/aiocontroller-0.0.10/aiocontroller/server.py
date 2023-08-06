import http
import inspect
import logging
from typing import Generic, Callable, Type, Any, Iterable, Iterator

from aiohttp import web
from di_ioc import AbstractServiceProvider, ServiceContainer

from .abstraction import TController, AbstractEndpointCollection, AbstractEndpointDef
from .endpoints import EndpointDefTable, BoundEndpoints

log = logging.getLogger(__name__)

_EMPTY_CONTAINER = ServiceContainer()


def request_scope(req: web.Request) -> AbstractServiceProvider:
    scope = req.get('scoped_container')
    if scope is None:
        container = req.app.get('service_container')
        if container is None:
            scope = _EMPTY_CONTAINER
        else:
            scope = container.create_scope()
        req['scoped_container'] = scope
    return scope


class ControllerRoutesAdapter(Generic[TController], Iterable[web.AbstractRouteDef]):
    """
    Defines how endpoints map to web.AbstractRouteDefs. Many of the steps during
    the process to convert are exposed as methods that can be overridden.
    """

    def __init__(self, endpoints: AbstractEndpointCollection[TController]):
        self._endpoints = endpoints

    def __iter__(self) -> Iterator[web.AbstractRouteDef]:
        return iter(self.create_routes())

    def create_route(self, endpoint: AbstractEndpointDef) -> web.AbstractRouteDef:
        return web.route(
            endpoint.http_method,
            endpoint.route_path,
            self.create_req_handler(endpoint))

    def create_routes(self) -> Iterable[web.AbstractRouteDef]:
        for f in self._endpoints:
            yield self.create_route(f)

    def create_req_handler(self, endpoint: AbstractEndpointDef):
        async def req_handler(req: web.Request) -> web.Response:
            with request_scope(req):
                try:
                    controller = self.create_controller(req)
                    args, kwargs = await self.create_args(endpoint, req)
                    result = self.call_handler_method(endpoint, controller, args, kwargs)
                    if inspect.isawaitable(result):
                        result = await result
                    return self.create_response(endpoint, result)
                except BaseException as e:
                    return self.handle_exception(endpoint, e)

        return req_handler

    def create_controller(self, req: web.Request) -> TController:
        return request_scope(req).get_service(self._endpoints.controller_type)

    def call_handler_method(self, endpoint: AbstractEndpointDef, controller: TController, args, kwargs):
        return endpoint.controller_method(controller, *args, **kwargs)

    @staticmethod
    def create_response(endpoint: AbstractEndpointDef, result: Any) -> web.Response:
        return endpoint.signature.serialize_result(result)

    @staticmethod
    def create_error_response(endpoint: AbstractEndpointDef, exception: BaseException) -> web.Response:
        return web.json_response(
            {'error': str(exception)},
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    @staticmethod
    async def create_args(endpoint: AbstractEndpointDef, req: web.Request):
        args, kwargs = [], {}
        await endpoint.signature.deserialize_args(req, args, kwargs)
        return args, kwargs

    def handle_exception(self, endpoint: AbstractEndpointDef, e: BaseException) -> web.Response:
        if isinstance(e, web.HTTPException):
            raise
        return self.create_error_response(endpoint, e)


class StaticRoutesAdapter(ControllerRoutesAdapter):
    def call_handler_method(self, endpoint: AbstractEndpointDef, controller: TController, args, kwargs):
        return endpoint.controller_method(*args, **kwargs)


RouteFactory = Callable[[AbstractEndpointCollection[TController]], Iterable[web.AbstractRouteDef]]


def controller_routes(cls: Type[TController],
                      endpoints: AbstractEndpointCollection[TController] | EndpointDefTable,
                      factory: RouteFactory[TController] = ControllerRoutesAdapter
                      ) -> Iterable[web.AbstractRouteDef]:
    """
    Map routes from the controller using default conventions.
    :param cls: the controller class.
    :param endpoints: the controller endpoints.
    :param factory: the mapping that converts endpoints to server routes.
    :return:
    """
    if isinstance(endpoints, EndpointDefTable):
        endpoints = BoundEndpoints(cls, endpoints)
    return factory(endpoints)


def routes(endpoints: AbstractEndpointCollection[TController] | EndpointDefTable,
           factory: RouteFactory[TController] = StaticRoutesAdapter
           ) -> Iterable[web.AbstractRouteDef]:
    """
    Map routes from static handlers using default conventions.
    :param endpoints: the controller endpoints.
    :param factory: the mapping that converts endpoints to server routes.
    :return:
    """
    if isinstance(endpoints, EndpointDefTable):
        endpoints = BoundEndpoints(type(None), endpoints)
    return factory(endpoints)


def prepare_app_services(app: web.Application, services: AbstractServiceProvider):
    app['service_container'] = services
