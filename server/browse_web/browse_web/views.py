from flask import (
    render_template,
    redirect,
    url_for,
    Response,
    request,
    make_response,
    json,
    jsonify,
    current_app,
)
from flask_login import login_user, logout_user, current_user, login_required
from browse_web.models import Admin, Device, Image, Timage, Status, Network, Cfg
from browse_web import app
from browse_web.forms import CameraSettingForm
from browse_web.extensions import db
from browse_web.utils import generate_screen_shot, paint_target, resize_image
from flask_dropzone import random_filename
from wtforms import SelectField
import os
from datetime import datetime, timedelta
import cv2


@app.route("/", methods=["GET", "POST"])
def index():
    networks = Network.query.order_by(Network.loss.desc()).limit(10)
    setattr(
        CameraSettingForm,
        "network",
        SelectField(
            choices=[(network.id, network.name) for network in networks], coerce=int
        ),
    )
    form = CameraSettingForm()
    if form.is_submitted():
        sys_status = Status.query.get(1)
        if sys_status.status == "running":
            camera = Device.query.get(int(form.camera_id.data))
            camera.name = form.name.data
            camera.ip = form.ip.data
            camera.username = form.username.data
            camera.password = form.password.data
            camera.client = form.client.data
            camera.mode = form.mode.data
            if form.mode.data == "belt":
                if form.network.data and form.network.data != 1:
                    camera.network_id = form.network.data
                else:
                    camera.network_id = 2
            else:
                camera.network_id = 1
            camera.start_point = form.start_point.data
            camera.nor_lim = form.nor_lim.data
            camera.ext_lim = form.ext_lim.data
            camera.borderline = form.borderline.data
            db.session.commit()
            return redirect(url_for("index"))
    # TODO 这里的逻辑还不够完善
    else:
        # page = int(request.form['page'])
        # page = 1
        # TODO page不能写死
        # per_page = current_app.config['INFO_PER_PAGE']
        devices = Device.query.order_by(Device.id)
        # pagination = Image.query.filter_by(usage='belt').order_by(Image.timestamp.desc()).paginate(page, per_page)
        # infos = pagination.items
        return render_template("index.html", devices=devices, form=form)


# @app.route("/camera_feed/<int:camera_id>")
# # FIXME 处理预览的情况
# @app.route("/camera_feed/<int:camera_id>/<int:mode>")
# def video_feed(camera_id, mode=0):
#     return Response(
#         gen_frame(camera_id, mode), mimetype="multipart/x-mixed-replace; boundary=frame"
#     )


@app.route("/is_login", methods=["POST"])
def is_login():
    if current_user.is_authenticated:
        data = {"boo": True}
    else:
        data = {"boo": False}
    response = make_response(json.dumps(data))
    return response


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = Admin.query.filter_by(username=username).first()
    if user is not None and user.validate_password(password):
        login_user(user)
        data = {"boo": True}
    else:
        data = {"boo": False}
    response = make_response(json.dumps(data))
    return response


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/getDevice", methods=["POST"])
def get_device():
    camera_id = request.form["deviceId"][6]
    # 调用Device类内置函数，将查询到的Device对象转化为json格式
    response = Device.query.get(camera_id).to_json()
    return jsonify(response)


@app.route("/checkStatus", methods=["POST"])
def check_status():
    sys_status = Status.query.get(1)
    if sys_status.status == "running":
        cfg = Cfg.query.get(1)
        data = {"boo": True, "classes": cfg.CLASSES[2:]}
    else:
        data = {"boo": False}
    response = make_response(json.dumps(data))
    return response


@app.route("/getBackground", methods=["POST"])
def get_background():
    camera_id = int(request.form["deviceId"][6:])
    # FIXME 传输图片大小
    generate_screen_shot(camera_id)
    # FIXME 部署前需修改配置
    data = {
        "boo": True,
        "imgUrl": url_for(
            "static", filename="img/screen_shot/camera%s.jpg" % camera_id
        ),
        "width": 1280,
        "height": 720,
    }
    response = make_response(json.dumps(data))
    return response


@app.route("/warningRecord", methods=["POST"])
def warning_record():
    camera_id = request.form["deviceId"]
    if camera_id == "all":
        records = Image.query.order_by(Image.timestamp.desc()).limit(10)
    else:
        records = (
            Image.query.filter(Image.camera_id == int(camera_id))
            .order_by(Image.timestamp.desc())
            .limit(10)
        )
    data = [
        [
            record.device.name,
            record.timestamp.strftime("%y年%m月%d日 %H:%M"),
            record.level,
            record.storage_path,
        ]
        for record in records
    ]
    response = make_response(json.dumps(data))
    return response


@app.route("/chart", methods=["POST"])
def chart():
    # camera_id = request.form['deviceId']
    data = {
        "data_x": [
            datetime.strftime(datetime.now() - timedelta(days=i), "%m-%d")
            for i in range(25, -1, -5)
        ],
        "data_normal": [],
        "data_extreme": [],
    }
    # if camera_id == 'all':
    for i in range(25, -1, -5):
        normal_records = Image.query.filter(
            Image.timestamp.between(
                datetime.now() - timedelta(days=i + 5),
                datetime.now() - timedelta(days=i),
            ),
            Image.level == "普通",
        ).count()
        extreme_records = Image.query.filter(
            Image.timestamp.between(
                datetime.now() - timedelta(days=i + 5),
                datetime.now() - timedelta(days=i),
            ),
            Image.level == "严重",
        ).count()
        data["data_normal"].append(normal_records)
        data["data_extreme"].append(extreme_records)
    response = make_response(json.dumps(data))
    return response
    # else:
    #     records = Image.query.filter(
    #         datetime.now() - timedelta(days=1) <= Image.timestamp <= datetime.now() - timedelta(days=1)).count()


@app.route("/viewHistory", methods=["POST"])
def view_history():
    data = {}
    camera_id = request.form["deviceId"]
    page = request.form["page"]
    if not page:
        page = 1
    else:
        page = int(page)
    per_page = current_app.config["HISTORY_INFOS_PER_PAGE"]
    if not camera_id:
        pagination = Image.query.order_by(Image.timestamp.desc()).paginate(
            page, per_page
        )
    else:
        pagination = (
            Image.query.filter(Image.device_id == int(camera_id))
            .order_by(Image.timestamp.desc())
            .paginate(page, per_page)
        )
    records = pagination.items
    data["maxPage"] = pagination.pages
    data["list"] = [
        [
            record.device.name,
            record.timestamp.strftime("%y年%m月%d日 %H:%M"),
            record.level,
            record.storage_path,
        ]
        for record in records
    ]
    response = make_response(json.dumps(data))
    return response


# 获取当前分页和分页中的图片
@app.route("/getPhotos", methods=["POST"])
def get_photos():
    data = {}
    if current_user.is_authenticated:
        data["boo"] = True
        temp_page = int(request.form["temp_page"])
        dataset_page = int(request.form["dataset_page"])
        temp_per_page = current_app.config["TEMP_IMAGES_PER_PAGE"]
        dataset_per_page = current_app.config["DATASET_IMAGES_PER_PAGE"]
        temp = (
            Timage.query.filter(Timage.status == "temp")
            .order_by(Timage.timestamp.desc())
            .paginate(temp_page, temp_per_page)
        )
        dataset = (
            Timage.query.filter(Timage.status == "db")
            .order_by(Timage.timestamp.desc())
            .paginate(dataset_page, dataset_per_page)
        )
        dataset_images = dataset.items
        temp_images = temp.items
        data["temp_maxpage"] = temp.pages if temp.pages else 1
        data["dataset_maxpage"] = dataset.pages if dataset.pages else 1
        data["temp"] = [
            {
                "id": image.id,
                "src": image.storage_path[
                    len(os.path.abspath("")) + len("/browse_web") :
                ],
                "height": image.height,
                "width": image.width,
            }
            for image in temp_images
        ]
        data["dataset"] = [
            {
                "id": image.id,
                "src": image.show_path[len(os.path.abspath("")) + len("/browse_web") :],
            }
            for image in dataset_images
        ]
    else:
        data["boo"] = False
    response = make_response(json.dumps(data))
    return response


# 检查是否还存在未标注图片
@app.route("/checkExist", methods=["POST"])
def check_exist():
    data = {"boo": False}
    if current_user.is_authenticated:
        temp = Timage.query.filter(Timage.status == "temp").count()
        if not temp:
            data = {"boo": True}
    response = make_response(json.dumps(data))
    return response


# 图片上传
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and "file" in request.files:
        f = request.files.get("file")
        filename = random_filename(f.filename)
        storage_path = os.path.join(current_app.config["STORAGE_PATH"], filename)
        f.save(storage_path)
        file = cv2.imread(storage_path)
        file = resize_image(file)
        cv2.imwrite(storage_path, file)
        img = Timage(
            storage_path=storage_path,
            height=file.shape[0],
            width=file.shape[1],
            timestamp=datetime.now(),
            status="temp",
        )
        db.session.add(img)
        db.session.commit()
    return redirect(url_for("index"))


# 提交单个框和标记
@login_required
@app.route("/saveStep", methods=["POST"])
def save_step():
    data = {}
    x_min = int(float(request.form["data[0][minX]"]))
    y_min = int(float(request.form["data[0][minY]"]))
    x_max = int(float(request.form["data[0][maxX]"]))
    y_max = int(float(request.form["data[0][maxY]"]))
    img_id = request.form["imgId"]
    cfg = Cfg.query.get(1)
    classes = cfg.CLASSES
    classes_num = int(request.form["type"][3:]) + 2
    class_name = classes[classes_num]
    data["boo"] = True
    timestamp = datetime.now()
    show_path = (
        current_app.config["TEMP_PATH"] + timestamp.strftime("%Y%m%d%H%M%S%f") + ".jpg"
    )
    image = Timage.query.get(int(img_id))
    ori_image_path = image.storage_path
    c1, c2 = (x_min, y_min), (x_max, y_max)
    ori_image = cv2.imread(ori_image_path)
    paint_target(ori_image, class_name, c1, c2, show_path=show_path)
    area = str(x_min) + "," + str(y_min) + "," + str(x_max) + "," + str(y_max)
    tag = class_name
    push_image = Timage(
        show_path=show_path,
        timestamp=timestamp,
        tags=tag,
        areas=area,
        status=str(img_id),
    )
    db.session.add(push_image)
    db.session.commit()
    steps = Timage.query.filter(Timage.status == str(img_id))
    # TODO 按时间进行排列
    data["list"] = [
        {
            "id": image.id,
            "src": image.show_path[len(os.path.abspath("")) + len("/browse_web") :],
        }
        for image in steps
    ]
    response = make_response(json.dumps(data))
    return response


@app.route("/viewSteps", methods=["POST"])
def view_steps():
    img_id = request.form["imgId"]
    data = {"boo": True}
    steps = Timage.query.filter(Timage.status == str(img_id))
    data["list"] = [
        {
            "id": image.id,
            "src": image.show_path[len(os.path.abspath("")) + len("/browse_web") :],
        }
        for image in steps
    ]
    response = make_response(json.dumps(data))
    return response


@app.route("/deleteStep", methods=["POST"])
def delete_step():
    img_id = int(request.form["imgId"])
    step = Timage.query.get(img_id)
    os.remove(step.show_path)
    db.session.delete(step)
    db.session.commit()
    data = {"boo": True}
    response = make_response(json.dumps(data))
    return response


# 保存所有的PULL并将图片转存至数据库
@app.route("/savePhoto", methods=["POST"])
def save_photo():
    timestamp = datetime.now()
    img_id = str(request.form["imgId"])
    # TODO 把这里的文件名和storage_path中的统一起来
    show_path = (
        current_app.config["SHOW_PATH"] + timestamp.strftime("%Y%m%d%H%M%S%f") + ".jpg"
    )
    if Timage.query.filter(Timage.status == img_id).count():
        steps = Timage.query.filter(Timage.status == img_id)
        image = Timage.query.get(int(img_id))
        ori_image = cv2.imread(image.storage_path)
        for step in steps:
            image.tags = image.tags + step.tags + " "
            image.areas = image.areas + step.areas + " "
            area = step.areas.split(",")
            tag = step.tags
            c1, c2 = (int(area[0]), int(area[1])), (int(area[2]), int(area[3]))
            cv2.rectangle(ori_image, c1, c2, (37, 232, 209), 8)
            ori_image = paint_target(ori_image, tag, c1, c2, save=False)
            os.remove(step.show_path)
            db.session.delete(step)
        cv2.imwrite(show_path, ori_image)
        image.show_path = show_path
        image.status = "db"
        db.session.commit()
        data = {"boo": True}
    else:
        data = {"boo": False}
    response = make_response(json.dumps(data))
    return response


@app.route("/deleteDB", methods=["POST"])
def delete_db():
    img_id = request.form["imgId"]
    image = Timage.query.get(int(img_id))
    os.remove(image.storage_path)
    os.remove(image.show_path)
    db.session.delete(image)
    db.session.commit()
    data = {"boo": True}
    response = make_response(json.dumps(data))
    return response


# 对已经添加入数据库的图片进行重新绘制
@app.route("/redrawDB", methods=["POST"])
def redraw():
    img_id = request.form["imgId"]
    image = Timage.query.get(int(img_id))
    os.remove(image.show_path)
    image.show_path = ""
    image.timestamp = datetime.now()
    image.status = "temp"
    image.tags = ""
    image.areas = ""
    db.session.commit()
    data = {"boo": True}
    response = make_response(json.dumps(data))
    return response


@app.route("/training", methods=["POST"])
def training():
    status = Status.query.get(1)
    if status.status == "running":
        image_num = Timage.query().filter(Timage.status == "db").count()
        if image_num > 2000:
            # TODO 确定这里的数值设置合理
            status.status = "training"
            db.session.commit()
            # TODO 确定status的状态总数并返回对应的错误信息
            data = {"boo": True}
        else:
            data = {"boo": False}
    else:
        data = {"boo": False}
    response = make_response(json.dumps(data))
    return response


@app.route("/full_screen_preview", methods=["POST"])
def full_screen():
    data = {"boo": True}
    response = make_response(json.dumps(data))
    return response


# @app.route('/quit_full_screen', methods=['POST'])
# def quit_full_screen():
#     pass
