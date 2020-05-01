from server.models import Admin
from server.extensions import db


def test_initdb_command(test_app):
    create_all()
    create_all()
    result = test_app.test_cli_runner().invoke(args=["initdb"])
    assert "Initialized database." in result.output


def test_initdb_command_with_drop(test_app):
    result = test_app.test_cli_runner().invoke(args=["initdb", "--drop"], input="y\n")
    assert (
        "This operation will delete the database, do you want to continue?"
        in result.output
    )
    assert "Drop tables." in result.output


def test_init_command(test_app):
    result = test_app.test_cli_runner().invoke(
        args=["init", "--username", "grey", "--password", "123"]
    )
    assert "Creating the temporary administrator account..." in result.output
    assert "Done." in result.output
    assert Admin.query.count() == 1
    assert Admin.query.first().username == "grey"
