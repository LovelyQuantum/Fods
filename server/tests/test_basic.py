from sqlalchemy import text
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_app_exist(test_app):
    assert current_app is not None


def test_app_is_testing(test_app):
    assert current_app.config["TESTING"] is True


def test_db_connection():
    engine = create_engine("postgresql://hina:429526000@postgres/mydb")
    Session = sessionmaker(engine)
    session = Session()
    sql = text("SELECT 1")
    assert session.execute(sql)


def test_api_server_connection(test_app):
    response = test_app.test_client().get("apis/test")
    data = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "success" in data
