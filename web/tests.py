import pytest
import re

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
    number_of_res = None
    url_regex = "^www\.[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$"

    def test_resources(self, client):
        rv = client.get("/api/resources")
        json_data = rv.get_json()
        self.number_of_res = len(json_data)

    def test_post_resource(self, client):
        rv = client.post('/api/resources', json={
            'url': 'www.google.com', 'type': 'text'
        })
        json_data = rv.get_json()
        assert json_data["status_code"] == 102 or json_data["status_code"] == 200

    def test_post_resource_image(self, client):
        rv = client.post('/api/resources', json={
            'url': 'www.google.com', 'type': 'images'
        })
        json_data = rv.get_json()
        assert json_data["status_code"] == 102 or json_data["status_code"] == 200

    def test_resource_not_found(self, client):
        rv = client.get("/api/resources/99999")
        json_data = rv.get_json()

        assert json_data["status_code"] == 404

    def test_first_resource(self, client):
        rv = client.get("/api/resources/1")
        json_data = rv.get_json()

        assert json_data["id"] == 1
        assert json_data["text"] is not None or json_data["images"] is not None
        assert re.search(self.url_regex, json_data["url"])