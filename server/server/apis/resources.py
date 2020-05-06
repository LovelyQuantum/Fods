from flask import jsonify, request
from flask.views import MethodView
from server.extensions import db
from server.models import Device, FodRecord, FodCfg, BddCfg, VirtualGpu
from datetime import datetime, timedelta
from pymemcache.client.base import Client
from pymemcache import serde
from sqlalchemy import or_
import numpy as np
import os
import psutil


status_register = Client(
    ("status_register", 12001),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer,
)


class TestAPI(MethodView):
    def get(self):
        return jsonify(
            {
                "api_version": "1.0",
                "current_url": "http://example.com/apis/test",
                "status": "success",
            }
        )


class DeviceInfoAPI(MethodView):
    def get(self):
        response = {"status": "device not found"}
        response["deviceList"] = [
            {
                "id": device.id,
                "name": f"camera{str(device.id).zfill(2)}",
                "path": f"http://192.168.43.69:8082/hls/device{device.id}.m3u8",
            }
            for device in Device.query.order_by(Device.id).all()
        ]
        response["deviceNum"] = len(response["deviceList"])
        if response["deviceList"]:
            response["status"] = "success"
        return jsonify(response)


class FodRecordAPI(MethodView):
    def post(self):
        response = {"status": "record not found"}
        data = request.get_json()
        current_page = data["Page"]

        if data["dateRange"]["dateRangeBegin"]:
            date_range_begin = datetime.strptime(
                data["dateRange"]["dateRangeBegin"][:10], r"%Y-%m-%d"
            )
            date_range_end = datetime.strptime(
                data["dateRange"]["dateRangeEnd"][:10], r"%Y-%m-%d"
            )
            if date_range_begin > date_range_end:
                date_range_begin, date_range_end = date_range_end, date_range_begin
        else:
            date_range_begin = datetime.now() - timedelta(days=365)
            date_range_end = datetime.now()

        # TODO add fix id feature
        if FodRecord.query.count():
            response["status"] = "success"
            response["totalPages"] = int(
                FodRecord.query.filter(
                    FodRecord.timestamp.between(date_range_begin, date_range_end)
                ).count()
                / 7
            )
            if response["totalPages"] > 9999:
                response["totalPages"] = 9999
            response["records"] = [
                {
                    "id": record.id,
                    "timestamp": record.timestamp,
                    "deviceName": Device.query.filter_by(id=record.device_id)
                    .first()
                    .name,
                    "status": record.status,
                }
                for Id, record in enumerate(
                    FodRecord.query.filter(
                        FodRecord.timestamp.between(date_range_begin, date_range_end)
                    ).order_by(FodRecord.timestamp.desc())[
                        current_page * 7:(current_page + 1) * 7
                    ]
                )
            ]
        return jsonify(response)


# get preview prcture of selected record
class FodRecordPreview(MethodView):
    # FIXME handle error when picture is removed
    def post(self):
        response = {"status": "preview not found"}
        data = request.get_json()
        if FodRecord.query.filter_by(id=data["recordId"]):
            response = {"status": "success"}
            response["previewSrc"] = (
                FodRecord.query.filter_by(id=data["recordId"]).first().storage_path
            )
        return jsonify(response)


class FodRecordReportAPI(MethodView):
    def post(self):
        response = {"status": "Report not found"}
        data = request.get_json()
        if data["dateRange"]["dateRangeBegin"]:
            date_range_begin = datetime.strptime(
                data["dateRange"]["dateRangeBegin"][:10], r"%Y-%m-%d"
            )
            date_range_end = datetime.strptime(
                data["dateRange"]["dateRangeEnd"][:10], r"%Y-%m-%d"
            )
            if date_range_begin > date_range_end:
                date_range_begin, date_range_end = date_range_end, date_range_begin
        else:
            date_range_begin = datetime.now() - timedelta(days=365)
            date_range_end = datetime.now()
        if FodRecord.query.count():
            response["status"] = "success"
            date_length = (date_range_end - date_range_begin).days
            time_scale = date_length if date_length < 30 else 30
            date_periods = np.histogram(
                np.arange(date_length, dtype=int), bins=time_scale
            )[1].astype("int32")
            response["recordSeries"] = [
                {
                    "name": "预警次数",
                    "data": [
                        {
                            "x": (
                                date_range_begin + timedelta(days=int(date_periods[i]))
                            ).strftime(r"%Y/%m/%d"),
                            "y": FodRecord.query.filter(
                                FodRecord.timestamp.between(
                                    date_range_begin
                                    + timedelta(days=int(date_periods[i])),
                                    date_range_begin
                                    + timedelta(days=int(date_periods[i + 1])),
                                )
                            ).count(),
                        }
                        for i in range(len(date_periods) - 1)
                    ],
                },
                {
                    "name": "严重预警次数",
                    "data": [
                        {
                            "x": (
                                date_range_begin + timedelta(days=int(date_periods[i]))
                            ).strftime(r"%Y/%m/%d"),
                            "y": FodRecord.query.filter(
                                FodRecord.timestamp.between(
                                    date_range_begin
                                    + timedelta(days=int(date_periods[i])),
                                    date_range_begin
                                    + timedelta(days=int(date_periods[i + 1])),
                                )
                            )
                            .filter(
                                or_(
                                    FodRecord.status == "严重",
                                    FodRecord.status == "severe",
                                )
                            )
                            .count(),
                        }
                        for i in range(len(date_periods) - 1)
                    ],
                },
            ]

        return jsonify(response)


class DeviceSettingAPI(MethodView):
    # FIXME get device id from backend not from url
    def get(self):
        response = {"status": "success"}
        device = Device.query.filter_by(
            id=int(request.args.get("device_name")[-2:])
        ).first()
        fodcfg = FodCfg.query.filter_by(
            device_id=int(request.args.get("device_name")[-2:])
        ).first()
        bddcfg = BddCfg.query.filter_by(
            device_id=int(request.args.get("device_name")[-2:])
        ).first()
        response["device"] = {
            "path": (
                f"rtsp://{device.username}:{device.password}"
                f"@{device.ip}:554/Streaming/Channels/1"
            ),
            "name": device.name,
            "ip": device.ip,
            "username": device.username,
            "password": device.password,
        }
        if fodcfg:
            response["fodCfg"] = {
                "nWarningThreshold": fodcfg.n_warning_threshold,
                "exWarningThreshold": fodcfg.ex_warning_threshold,
            }
        if bddcfg:
            response["bddCfg"] = {"offsetDistance": bddcfg.offset_distance}

        return jsonify(response)

    def post(self):
        response = {"status": "success"}
        data = request.get_json()
        if not Device.query.filter_by(id=int(data["device"]["id"][-2:])).scalar():
            response = {"status": "fail"}
            return jsonify(response)
        else:
            device = Device.query.filter_by(id=int(data["device"]["id"][-2:])).first()
            device.name = data["device"]["name"]
            device.username = data["device"]["username"]
            device.ip = data["device"]["ip"]
            device.password = data["device"]["password"]

        if "fod" in data["func"]:
            if not FodCfg.query.filter_by(
                device_id=int(data["device"]["id"][-2:])
            ).scalar():
                virtual_gpu = VirtualGpu.query.filter_by(used=False).first()
                if virtual_gpu:
                    virtual_gpu.used = True
                    db.session.add(virtual_gpu)
                    fodcfg = FodCfg(
                        device_id=data["device"]["id"][-2:],
                        n_warning_threshold=int(data["fodCfg"]["nWarningThreshold"]),
                        ex_warning_threshold=int(data["fodCfg"]["exWarningThreshold"]),
                        virtual_gpu_id=virtual_gpu.id,
                    )
                else:
                    response["status"] = "error"
                    response["error"] = "检测数量达到上限"
                    return jsonify(response)

            else:
                fodcfg = FodCfg.query.filter_by(
                    device_id=int(data["device"]["id"][-2:])
                ).first()
                fodcfg.n_warning_threshold = (int(data["fodCfg"]["nWarningThreshold"]),)
                fodcfg.ex_warning_threshold = (
                    int(data["fodCfg"]["exWarningThreshold"]),
                )
            db.session.add(fodcfg)

        if "bdd" in data["func"]:
            if not BddCfg.query.filter_by(
                device_id=int(data["device"]["id"][-2:])
            ).scalar():
                bddcfg = BddCfg(
                    device_id=data["device"]["id"][-2:],
                    offset_distance=int(data["bddCfg"]["offsetDistance"]),
                )
            else:
                bddcfg = BddCfg.query.filter_by(
                    device_id=int(data["device"]["id"][-2:])
                ).first()
                bddcfg.offset_distance = (int(data["bddCfg"]["offsetDistance"]),)
            db.session.add(bddcfg)
        db.session.commit()
        status_register.set(f"{device.id}", "changed")
        return jsonify(response)


class SystemInfoAPI(MethodView):
    def get(self):
        response = {"status": "success"}
        response["systemUpDay"] = (
            datetime.now()
            - datetime.fromtimestamp(psutil.Process(os.getpid()).create_time())
        ).days
        response["warmingTimes"] = FodRecord.query.count()
        response["exWarmingTimes"] = FodRecord.query.filter(
            or_(FodRecord.status == "严重", FodRecord.status == "severe",)
        ).count()
        return jsonify(response)
