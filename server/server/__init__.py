import os
import click
from flask import Flask
from server.settings import config
from server.extensions import db, migrate
from server.models import Device, DnnModel, VirtualGpu
from server.apis import apis


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")

    app = Flask("server")
    app.config.from_object(config[config_name])

    register_blueprints(app)
    register_extensions(app)
    register_commands(app)
    register_shell_context(app)
    # register_template_context(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(apis, url_prefix="/apis")


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        pass


def register_commands(app):
    @app.cli.command()
    @click.option("--drop", is_flag=True, help="Create after drop.")
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                "This operation will delete the database, do you want to continue?",
                abort=True,
            )
            db.drop_all()
            click.echo("Drop tables.")
        db.create_all()
        click.echo("Initialized database.")

    @app.cli.command()
    def init():
        db.drop_all()
        click.echo("Initializing the database...")
        db.create_all()

        for i in range(1):
            device = Device()
            db.session.add(device)
        dnn_model = DnnModel(
                weight="./checkpoints/yolov3.tf", category="fod", classes="stone"
            )
        for i in range(6):
            device = VirtualGpu(used=False)
            db.session.add(device)
        db.session.add(dnn_model)
        db.session.commit()
