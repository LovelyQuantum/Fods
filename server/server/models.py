from datetime import datetime
from server.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# filled when init system
class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# init when init system update when submit device settings
class Device(db.Model):
    __tablename__ = "device"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default="摄像头")
    ip = db.Column(db.String, default="0.0.0.0")
    type = db.Column(db.String, default="camera")
    username = db.Column(db.String, default="admin")
    password = db.Column(db.String, default="12345")


# Foreign object detection
# filled when submit device settings
class FodCfg(db.Model):
    __tablename__ = "fodCfg"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    n_warning_threshold = db.Column(db.Integer, default=10000)
    ex_warning_threshold = db.Column(db.Integer, default=40000)


class FodRecord(db.Model):
    __tablename__ = "fodRecord"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    device_id = db.Column(db.Integer)
    dnn_model_id = db.Column(db.Integer, default=1)
    status = db.Column(db.String)
    storage_path = db.Column(db.String)
    tags = db.Column(db.String)
    areas = db.Column(db.String)


# Belt deviation detection
# filled when submit device settings
class BddCfg(db.Model):
    __tablename__ = "bddCfg"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    offset_distance = db.Column(db.Integer)


# filled when init system
class ModeCategory(db.Model):
    __tablename__ = "modeCategory"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


# filled when submit device settings
# all dnn models include fod, bdd and others
class DnnModel(db.Model):
    __tablename__ = "dnnModel"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String)
    classes = db.Column(db.String)  # use whitespace to split class names
    weight = db.Column(db.String)


# filled when init system
class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.Integer)


# filled when init system
class VirtualGpu(db.Model):
    __tablename__ = "virtualGpu"
    id = db.Column(db.Integer, primary_key=True)
    used = db.Column(db.Boolean)


# filled when submit device settings
class DeviceLocation(db.Model):
    __tablename__ = "deviceLocation"
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)


# system status(running training or erroring...)
class SystemStatus(db.Model):
    __tablename__ = "systemStatus"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, default="running")
