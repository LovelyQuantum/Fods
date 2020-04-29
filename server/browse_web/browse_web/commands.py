import click
from browse_web import app, db
from browse_web.models import Admin, Device, Status, Cfg, Network, Gpu
from flask import current_app
import os
import shutil
from datetime import datetime


@app.cli.command()
@click.option("--username", prompt=True, help="The username used to login.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password used to login.",
)
def init_admin(username, password):
    admin = Admin.query.first()
    if admin is not None:
        click.echo("The administrator already exists, updating...")
        admin.username = username
        admin.set_password(password)
    else:
        click.echo("Init the administrator account...")
        admin = Admin(username=username, name="Admin")
        admin.set_password(password)
        db.session.add(admin)
    db.session.commit()
    click.echo("Done.")


@app.cli.command()
@click.option("--username", prompt=True, help="The username used to login.")
@click.option(
    "--password",
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help="The password used to login.",
)
def init_db(username, password):
    click.echo("Init path...")
    # FIXME 在部署前把这部分去掉
    paths = [
        current_app.config["STORAGE_PATH"],
        current_app.config["TEMP_PATH"],
        current_app.config["SHOW_PATH"],
        current_app.config["SCREEN_SHOT_PATH"],
    ]
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            os.makedirs(path)
    click.echo("Updating tables...")
    db.drop_all()
    db.create_all()
    network1 = Network(
        name="无",
        usage="helmet",
        loss="00.0000",
        timestamp=datetime.now(),
        classes="安全帽 未佩戴安全帽",
        storage_path="/home/user/Server/yolo3/weights/default/helmet.pb",
    )
    network2 = Network(
        name="皮带异物检测模型   -检测种类:石块（默认）",
        usage="belt",
        loss="00.0000",
        timestamp=datetime.now(),
        classes="辅助类型1 辅助类型2 石块",
        storage_path="/home/user/Server/yolo3/weights/default/belt.pb",
    )
    sys_status = Status()
    alarm_status_1 = Status(status="idle")
    alarm_status_2 = Status(status="idle")
    gpu1 = Gpu()
    gpu2 = Gpu()
    cfg = Cfg()
    db.session.add(sys_status)
    db.session.add(alarm_status_1)
    db.session.add(alarm_status_2)
    db.session.add(cfg)
    db.session.add(network1)
    db.session.add(network2)
    db.session.add(gpu1)
    db.session.add(gpu2)
    db.session.commit()
    for i in range(10):
        device = Device()
        db.session.add(device)
    # 初始化管理员账户
    click.echo("Init the administrator account...")
    admin = Admin(username=username, name="Admin")
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    click.echo("Done.")


@app.cli.command()
def init_fs():
    # FIXME　检检查全部需要创建的文件夹
    paths = [
        current_app.config["STORAGE_PATH"],
        current_app.config["TEMP_PATH"],
        current_app.config["SHOW_PATH"],
        current_app.config["SCREEN_RECORD_PATH"],
        current_app.config["SCREEN_SHOT_PATH"],
    ]
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            os.makedirs(path)

    click.echo("Done.")
