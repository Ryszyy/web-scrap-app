import pytest

from web.app import create_app


@pytest.yield_fixture(scope='session')
def app():
    _app = create_app()
    ctx = _app.app_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    yield app.test_client()


class TestResources(object):
    def test_all_resources(self, client):
        assert 1 == 1
