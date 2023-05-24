import pytest
from moto.moto_server.threaded_moto_server import ThreadedMotoServer


def get_open_port() -> int:
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()

    return port


@pytest.fixture
def moto_server() -> ThreadedMotoServer:
    port = get_open_port()
    return ThreadedMotoServer(ip_address="127.0.0.1", port=port)
