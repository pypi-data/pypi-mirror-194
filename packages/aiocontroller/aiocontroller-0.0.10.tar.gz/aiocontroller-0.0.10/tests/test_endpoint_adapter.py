from dataclasses import dataclass
from typing import TypeVar, Callable, Awaitable, Optional

import pytest
from aiohttp import client, web
from di_ioc import ServiceContainer, auto
from pydantic.main import BaseModel

from aiocontroller import CustomResult, EndpointDefTable, server, client as api_client


class MyModel(BaseModel):
    """
    Test model
    """
    value: str


@dataclass
class MyCustomResult(CustomResult[str]):
    """
    Example of a custom result
    """
    value: str

    def __into_web_response__(self) -> web.Response:
        return web.Response(text=self.value)

    @classmethod
    async def __from_web_response__(cls, resp: client.ClientResponse) -> str:
        return await resp.text()


class Controller:
    async def return_none(self, value: str) -> None:
        pass

    async def return_pydantic(self, value: str) -> MyModel:
        return MyModel(value=value)

    async def return_custom(self, value: str) -> MyCustomResult:
        return MyCustomResult(value)


async def static_return_none(value: str) -> None:
    pass


async def static_return_pydantic(value: str) -> MyModel:
    return MyModel(value=value)


async def static_return_custom(value: str) -> MyCustomResult:
    return MyCustomResult(value)


TResult = TypeVar('TResult')
TestHandler = Callable[[str], Awaitable[TResult]]


def map_handlers(return_none: TestHandler[None], return_pydantic: TestHandler[MyModel],
                 return_custom: TestHandler[MyCustomResult]):
    endpoints = EndpointDefTable()
    endpoints.get('/none/{value}', handler=return_none)
    endpoints.get('/pydantic/{value}', handler=return_pydantic)
    endpoints.get('/custom/{value}', handler=return_custom)
    return endpoints


def controller_app():
    container = ServiceContainer()
    container[Controller] = auto(Controller)
    app = web.Application()
    server.prepare_app_services(app, container)
    endpoints = map_handlers(Controller.return_none, Controller.return_pydantic, Controller.return_custom)
    app.add_routes(server.controller_routes(Controller, endpoints))
    return app


def static_app():
    app = web.Application()
    endpoints = map_handlers(static_return_none, static_return_pydantic, static_return_custom)
    app.add_routes(server.routes(endpoints))
    return app


@pytest.mark.parametrize('app_factory', [controller_app, static_app])
async def test_controller_mapped_handlers(aiohttp_client, app_factory: web.Application):
    app = app_factory()
    api = await aiohttp_client(app)

    res = await api.get('/none/hello')
    assert res.status == 200

    res = await api.get('/pydantic/hello')
    assert res.status == 200
    assert MyModel.parse_obj(await res.json()).value == 'hello'

    res = await api.get('/custom/hello')
    assert res.status == 200
    assert (await MyCustomResult.__from_web_response__(res)) == 'hello'


async def test_http_exceptions_pass_through(aiohttp_client):
    endpoints = EndpointDefTable()

    @endpoints.get('/')
    async def handler() -> None:
        raise web.HTTPNotFound()

    app = web.Application()
    app.add_routes(server.routes(endpoints))
    api = await aiohttp_client(app)
    resp = await api.get('/')
    assert resp.status == 404


def test_optional_parameters():
    def handler(arg: int, optional_arg: Optional[str], optional_kwarg: Optional[str] = 'blah') -> None:
        pass

    endpoints = EndpointDefTable()
    endpoints.get('/', handler=handler)

    req = api_client.RequestBuilder('get', '/')
    sig = endpoints[handler].signature
    sig.serialize_args(req, [1, None], {})

    assert req.body['arg'] == 1
    assert req.body['optional_arg'] is None
    assert req.body['optional_kwarg'] == 'blah'
