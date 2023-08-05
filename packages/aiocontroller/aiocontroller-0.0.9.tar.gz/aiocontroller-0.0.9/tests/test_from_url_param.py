from aiocontroller import EndpointDefTable, client
from aiocontroller.endpoints import FromUrl

endpoints = EndpointDefTable()
route_path = '/api/{arg}'


class Controller:
    @endpoints.get(route_path)
    def handler(self, arg: int) -> None:
        pass


def static_handler(arg: int) -> None:
    pass


def test_read_param():
    h = Controller.handler
    endpoint = endpoints[h]

    assert endpoint.route_path == route_path
    assert endpoint.controller_method == h

    arg_param = endpoint.signature.params[0]
    assert isinstance(arg_param, FromUrl)
    assert arg_param.payload_name == 'arg'

    new_client = client.client_factory(Controller, endpoints)
    req = new_client.build_request(endpoint, [1], {})
    assert req.url_params['arg'] == '1'
    assert req.route == '/api/1'
