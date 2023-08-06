from typing import Any

from aiohttp import web, client

from aiocontroller import CustomResult, EndpointDefTable, server


class MyType(CustomResult):
    def __init__(self, value: str):
        self.value = value

    def __into_web_response__(self) -> web.Response:
        return web.Response(text=self.value)

    @classmethod
    async def __from_web_response__(cls, resp: client.ClientResponse) -> Any:
        return await resp.text()


def handler(arg: str) -> MyType:
    return MyType(arg)


async def test_return_custom_type(aiohttp_client):
    endpoints = EndpointDefTable()
    endpoints.get('/{arg}', handler=handler)

    app = web.Application()
    app.add_routes(server.routes(endpoints))
    api = await aiohttp_client(app)
    resp = await api.get('/hello')
    value = await MyType.__from_web_response__(resp)
    assert value == 'hello'
