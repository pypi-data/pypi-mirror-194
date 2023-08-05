from pydantic.main import BaseModel

from aiocontroller import EndpointDefTable, client
from aiocontroller.endpoints import FromBody

endpoints = EndpointDefTable()


class Body(BaseModel):
    arg1: int
    arg2: str


class Controller:
    @endpoints.get('/')
    @endpoints.body_param('body', is_root=True)
    def handler(self, body: Body) -> None:
        pass


def test_root_param():
    h = Controller.handler
    endpoint = endpoints[h]

    arg_param = endpoint.signature.params[0]
    assert isinstance(arg_param, FromBody)
    assert arg_param.is_root

    body = Body(arg1=1, arg2='2')
    new_client = client.client_factory(Controller, endpoints)
    req = new_client.build_request(endpoint, [body], {})
    assert Body.parse_obj(req.body) == body
