import asyncio
from unittest.mock import MagicMock, patch

import aiohttp
import pytest

pytestmark = pytest.mark.asyncio


@pytest.fixture
def add_method(web_port):
    base = f'http://localhost:{web_port}'

    def _inner(cli, name):
        method_url = f'{base}/{name}'

        async def actual_method(*params):
            params_str = '/'.join([str(x) for x in params])
            url = f'{method_url}/{params_str}/'
            resp = await cli.get(url)
            data = await resp.json()
            return int(data['response'])  # we have all ints as responses

        return actual_method

    def maker(cli, name):
        setattr(cli, name, _inner(cli, name))

    return maker


@pytest.fixture
async def cli(running_app, web_port, add_method):
    async with aiohttp.ClientSession() as session:
        add_method(session, 'fibonacci')
        add_method(session, 'ackermann')
        add_method(session, 'factorial')
        yield session


@pytest.fixture
def web_port(unused_tcp_port_factory):
    yield unused_tcp_port_factory()


@pytest.fixture
async def running_app(event_loop, web_port):
    from service.run import app

    server = app.create_server(port=web_port)
    await server
    yield server


async def test_factorial(cli, factorial_data):
    for x, y in factorial_data:
        assert int(await cli.factorial(x)) == y


async def test_ackermann(cli, ackermann_data):
    for x, y in ackermann_data:
        assert int(await cli.ackermann(*x)) == y


async def test_fibonacci(cli, fibonacci_data):
    for x, y in fibonacci_data:
        assert int(await cli.fibonacci(x)) == y
