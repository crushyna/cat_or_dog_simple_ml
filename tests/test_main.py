import pytest
from flask import session
from flask_api import status

from main import APP


@pytest.fixture
def client(app):
    """Get a test client for your Flask app"""
    return app.test_client()


@pytest.fixture
def app():
    """Yield your app with its context set up and ready"""
    with APP.app_context():
        yield APP


class TestRoot:
    def test_root_page(self, client):
        response = client.get("/")
        assert response.status_code == 200


class TestAbout:
    def test_about_page(self, client):
        response = client.get("/about")
        assert response.status_code == 200


class TestResults:
    def test_about_page(self, client):
        """
        This page should not be available until proper data is available, thus
        response == 502 is valid.
        """
        response = client.get("/results")
        assert response.status_code == 500


class TestUnsupportedPaths:
    def test_unsupported_paths(self, client):
        """
        response = client.get("/-2")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert b'Factoring of "-2" is not supported' in response.data

        Non-existing pages should always redirect to starting page.
        """
        response = client.get("/hello")
        assert response.status_code == 200
        assert b'Hello World from Flask in a uWSGI Nginx Docker container' in response.data

        response = client.get("/-2")
        assert response.status_code == 200

        response = client.get("/kox")
        assert response.status_code == 200
