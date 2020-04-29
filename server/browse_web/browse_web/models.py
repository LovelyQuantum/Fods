from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from browse_web.extensions import db


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, default='摄像头')
    ip = db.Column(db.String(30), default='0.0.0.0')
    username = db.Column(db.String, default='admin')
    password = db.Column(db.String, default='12345')
    client = db.Column(db.Integer, default=0)
    mode = db.Column(db.String, default='none')
    gpu = db.Column(db.Integer, default=-1)
    start_point = db.Column(db.String, default='432 0')
    nor_lim = db.Column(db.Integer, default=10000)
    ext_lim = db.Column(db.Integer, default=40000)
    borderline = db.Column(db.String, default='None')
    images = db.relationship('Image', back_populates='device')
    network_id = db.Column(db.Integer, db.ForeignKey('network.id'), default=1)
    network = db.relationship('Network')

    def to_json(self):
        to_dict = self.__dict__
        if "_sa_instance_state" in to_dict:
            del to_dict["_sa_instance_state"]
        return to_dict


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String)
    storage_path = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True)
    tags = db.Column(db.String, default='')
    areas = db.Column(db.String, default='')
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship('Device', back_populates='images')


class Timage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    storage_path = db.Column(db.String, default='')  # 用于训练的原始图片存储位置
    show_path = db.Column(db.String, default='')  # 用于用户浏览的标注后图片存储位置
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True)
    status = db.Column(db.String)
    tags = db.Column(db.String, default='')
    areas = db.Column(db.String, default='')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, default='running')
    client = db.Column(db.Integer)


class Cfg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ANCHOR_PER_SCALE = db.Column(db.Integer, default=3)
    LEARN_RATE_INIT = db.Column(db.Float, default=1e-4)
    LEARN_RATE_END = db.Column(db.Float, default=1e-6)
    FIRST_STAGE_EPOCHS = db.Column(db.Integer, default=30)
    SECOND_STAGE_EPOCHS = db.Column(db.Integer, default=30)
    WARMUP_EPOCHS = db.Column(db.Integer, default=2)
    INITIAL_WEIGHT = db.Column(db.String, default='./checkpoint/initial/yolov3_coco_demo.ckpt')
    MOVING_AVE_DECAY = db.Column(db.Float, default=0.9995)
    # TODO CLASSES_IN_USE应该与全局的CLASSES绑定，且与本次训练对应的模型绑定
    CLASSES_IN_USE = db.Column(db.String, default='辅助类型1 辅助类型2 石头')
    CLASSES = db.Column(db.PickleType, default=['辅助类型1', '辅助类型2', '石头', '木块', '其他'])
    # CLASSES_ENGLISH = db.Column(db.PickleType, default=['secondary1', 'secondary2', 'stone', 'wood', 'others'])
    TRAIN_BATCH_SIZE = db.Column(db.Integer, default=4)
    TEST_BATCH_SIZE = db.Column(db.Integer, default=2)


class Network(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    usage = db.Column(db.String)
    loss = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, index=True)
    classes = db.Column(db.String)
    storage_path = db.Column(db.String)


class Gpu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_num = db.Column(db.Integer)
