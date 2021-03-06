from server import create_app
import pytest


@pytest.fixture(scope='class')
def test_app():
    app = create_app('testing')
    context = app.app_context()
    context.push()
    yield app
    app.drop_all()
    context.pop()
