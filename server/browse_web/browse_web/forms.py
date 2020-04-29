from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class CameraSettingForm(FlaskForm):
    camera_id = StringField()
    name = StringField()
    ip = StringField()
    username = StringField()
    password = StringField()
    client = SelectField(choices=[(0, "无"), (1, "1号井"), (2, "1号井")], coerce=int)
    mode = SelectField(
        choices=[
            ("none", "监控"),
            ("belt", "皮带异物与跑偏检测"),
            ("helmet", "安全监测"),
            ("bunker", "煤仓堆煤检测"),
        ],
        coerce=str,
    )
    enhancement = SelectField(choices=[(0, "关闭"), (1, "开启")], coerce=int)
    start_point = StringField()
    nor_lim = SelectField(
        choices=[
            (10000, "10000"),
            (15000, "15000"),
            (20000, "20000"),
            (25000, "25000"),
        ],
        coerce=int,
    )
    ext_lim = SelectField(
        choices=[
            (35000, "35000"),
            (40000, "40000"),
            (45000, "45000"),
            (50000, "50000"),
        ],
        coerce=int,
    )
    borderline = StringField()
    submit = SubmitField("保存")


# FIXME 训练前的参数选择
