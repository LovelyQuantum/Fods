from server.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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
    ip = db.Column(db.String(30), default="0.0.0.0")
    username = db.Column(db.String, default="admin")
    password = db.Column(db.String, default="12345")
    images = db.relationship("Image", back_populates="device")


# filled when submit device settings
class FodCfg(db.Model):
    __tablename = "fodCfg"
    Id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    nor_lim = db.Column(db.Integer, default=10000)
    ext_lim = db.Column(db.Integer, default=40000)
    category_id = db.Column(db.Integer, default=0)


# Belt deviation detection
# filled when submit device settings
class BddCfg(db.Model):
    __tablename__ = "bddCfg"
    Id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    nor_lim = db.Column(db.Integer, default=10000)
    category_id = db.Column(db.Integer, default=1)


# filled when init system
class ModeCategory(db.Model):
    __tablename__ = "modeCategory"
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


# filled when submit device settings
class DnnModel(db.Model):
    __tablename__ = "dnnModel"
    Id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    model_id = db.Column(db.Integer)
    gpu_id = db.Column(db.Integer)


# filled when init system
class Location(db.Model):
    __tablename__ = "location"
    Id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.Integer)


# filled when init system
class Gpu(db.Model):
    __tablename__ = "gpu"
    Id = db.Column(db.Integer, primary_key=True)


# filled when submit device settings
class DeviceLocation(db.Model):
    __tablename__ = "deviceLocation"
    Id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
