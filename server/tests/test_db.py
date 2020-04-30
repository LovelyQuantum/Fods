from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_db_connection():
    engine = create_engine("postgresql://hina:429526000@postgres/mydb")
    Session = sessionmaker(engine)
    session = Session()
    sql = text("SELECT 1")
    assert session.execute(sql)
