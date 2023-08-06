import flask
import pytest
from flask import request

from pyspass import PySpassRequest


@pytest.fixture()
def flask_app():
    app = flask.Flask(__name__)
    app.testing = True
    return app.test_client()


@pytest.fixture()
def requ():
    return PySpassRequest(request, framework="flask")


class TestPySpassRequest:

    def test_init_for_flask(self):
        requ = PySpassRequest(request, framework="flask")
        assert requ

    def test_init_for_wrong_framework(self):
        with pytest.raises(NotImplementedError):
            PySpassRequest(request, framework="ABC")

    def test_access_to_posted_content(self, flask_app, requ):
        with flask_app as c:
            c.post("/?abc=abc")
            assert requ.get('abc') == 'abc'
        with flask_app as c:
            c.post("/?abc=123")
            assert requ.get('abc') == '123'

    def test_access_to_missing_content(self, flask_app, requ):
        """Empty string, if not in request obj"""
        with flask_app as c:
            c.post("/?abc=abc")
            assert requ.get("not_there") == ''

    def test_access_to_missing_content_as_int(self, flask_app, requ):
        """None, if not in request obj"""
        with flask_app as c:
            c.post("/?abc=abc")
            assert requ.get_int("not_there") is None

    def test_access_to_str_content_as_int(self, flask_app, requ):
        with flask_app as c:
            c.post("/?abc=abc")
            assert requ.get_int("abc") is None
        with flask_app as c:
            c.post("/?abc=123")
            result = requ.get_int("abc")
            assert result == 123
            assert isinstance(result, int)

    def test_access_to_missing_content_as_float(self, flask_app, requ):
        """None, if not in request obj"""
        with flask_app as c:
            c.post("/?abc=abc")
            assert requ.get_float("not_there") is None
        with flask_app as c:
            c.post("/?abc=abc")
            assert requ.get_float("not_there", 0.0) == 0.0
        with flask_app as c:
            c.post("/?abc=1.23")
            result = requ.get_float("abc")
            assert result == 1.23
            assert isinstance(result, float)
