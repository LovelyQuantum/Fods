from flask import jsonify, request
from flask.views import MethodView
from server.extensions import db
from server.models import Device, FodRecord, FodCfg, BddCfg, VirtualGpu, DeviceLocation
from datetime import datetime, timedelta, timezone
from pymemcache.client.base import Client
from pymemcache import serde
from sqlalchemy import or_, and_
import numpy as np
import os
import psutil


hls_server_url = os.getenv("HLS_SERVER_URL", "localhost")

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
                "sourcePath": f"http://{hls_server_url}"
                f":8082/hls/device{device.id}.m3u8",
                "deviceName": device.name,
            }
            for device in Device.query.order_by(Device.id).all()
        ]
        response["deviceNum"] = len(response["deviceList"])
        if response["deviceList"]:
            response["status"] = "success"
        return jsonify(response)


class FodRecordAPI(MethodView):
    def post(self):
        result_perpage = 12
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
                / result_perpage
            )
            if response["totalPages"] > 9999:
                response["totalPages"] = 9999
            response["records"] = [
                {
                    "id": record.id,
                    "timestamp": record.timestamp.astimezone(timezone(timedelta(hours=8))).strftime(r"%Y-%m-%d %H:%M"),
                    "deviceName": Device.query.filter_by(id=record.device_id)
                    .first()
                    .name,
                    "location": DeviceLocation.query.filter_by(
                        device_id=record.device_id
                    )
                    .first()
                    .location,
                    "status": record.status,
                }
                for Id, record in enumerate(
                    FodRecord.query.filter(
                        FodRecord.timestamp.between(date_range_begin, date_range_end)
                    ).order_by(FodRecord.timestamp.desc())[
                        current_page
                        * result_perpage : (current_page + 1)
                        * result_perpage
                    ]
                )
            ]
        return jsonify(response)


class FodDeviceRecordAPI(MethodView):
    def post(self):
        result_perpage = 12
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
                    and_(
                        FodRecord.timestamp.between(date_range_begin, date_range_end),
                        FodRecord.device_id == data["dataDeviceId"],
                    )
                ).count()
                / result_perpage
            )
            if response["totalPages"] > 9999:
                response["totalPages"] = 9999
            response["records"] = [
                {
                    "id": record.id,
                    "timestamp": record.timestamp.strftime(r"%Y-%m-%d %H:%M"),
                    "deviceName": Device.query.filter_by(id=record.device_id)
                    .first()
                    .name,
                    "location": DeviceLocation.query.filter_by(
                        device_id=record.device_id
                    )
                    .first()
                    .location,
                    "status": record.status,
                }
                for Id, record in enumerate(
                    FodRecord.query.filter(
                        and_(
                            FodRecord.timestamp.between(
                                date_range_begin, date_range_end
                            ),
                            FodRecord.device_id == data["dataDeviceId"],
                        )
                    ).order_by(FodRecord.timestamp.desc())[
                        current_page
                        * result_perpage : (current_page + 1)
                        * result_perpage
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
            date_range_begin = datetime.now() - timedelta(days=10)
            date_range_end = datetime.now()

        if FodRecord.query.count():
            response["status"] = "success"
            date_length = (date_range_end - date_range_begin).days
            time_scale = date_length if date_length < 10 else 10
            date_periods = np.histogram(
                np.arange(date_length, dtype=int), bins=time_scale
            )[1].astype("int32")
            response["recordSeries"] = [
                {
                    "name": "丈八采区预警次数",
                    "data": [
                        {
                            "x": (
                                date_range_begin
                                + timedelta(days=int(date_periods[i]) + 1)
                            ).strftime(r"%Y/%m/%d"),
                            "y": FodRecord.query.filter(
                                FodRecord.timestamp.between(
                                    date_range_begin
                                    + timedelta(days=int(date_periods[i])),
                                    date_range_begin
                                    + timedelta(
                                        days=int(date_periods[i + 1])
                                        if i < len(date_periods) - 1
                                        else int(date_periods[i]) + 2
                                    ),
                                )
                            )
                            .filter(FodRecord.location == "丈八采区")
                            .count(),
                        }
                        for i in range(len(date_periods))
                    ],
                },
                {
                    "name": "十四采区预警次数",
                    "data": [
                        {
                            "x": (
                                date_range_begin
                                + timedelta(days=int(date_periods[i]) + 1)
                            ).strftime(r"%Y/%m/%d"),
                            "y": FodRecord.query.filter(
                                FodRecord.timestamp.between(
                                    date_range_begin
                                    + timedelta(days=int(date_periods[i])),
                                    date_range_begin
                                    + timedelta(
                                        days=int(date_periods[i + 1])
                                        if i < len(date_periods) - 1
                                        else int(date_periods[i]) + 2
                                    ),
                                )
                            )
                            .filter(FodRecord.location == "十四采区")
                            .count(),
                        }
                        for i in range(len(date_periods))
                    ],
                },
            ]

        return jsonify(response)


class FodDeviceRecordReportAPI(MethodView):
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
            date_range_begin = datetime.now() - timedelta(days=10)
            date_range_end = datetime.now()

        if FodRecord.query.count():
            response["status"] = "success"
            date_length = (date_range_end - date_range_begin).days
            time_scale = date_length if date_length < 10 else 10
            date_periods = np.histogram(
                np.arange(date_length, dtype=int), bins=time_scale
            )[1].astype("int32")
            response["recordSeries"] = [
                {
                    "name": "预警次数",
                    "data": [
                        {
                            "x": (
                                date_range_begin
                                + timedelta(days=int(date_periods[i]) + 1)
                            ).strftime(r"%Y/%m/%d"),
                            "y": FodRecord.query.filter(
                                FodRecord.timestamp.between(
                                    date_range_begin
                                    + timedelta(days=int(date_periods[i])),
                                    date_range_begin
                                    + timedelta(
                                        days=int(date_periods[i + 1])
                                        if i < len(date_periods) - 1
                                        else int(date_periods[i]) + 2
                                    ),
                                )
                            )
                            .filter(FodRecord.device_id == data["dataDeviceId"])
                            .count(),
                        }
                        for i in range(len(date_periods))
                    ],
                }
            ]

        return jsonify(response)


class DeviceSettingAPI(MethodView):
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
        location = DeviceLocation.query.filter_by(
            device_id=int(request.args.get("device_name")[-2:])
        ).first()
        response["device"] = {
            "sourcePath": f"http://{hls_server_url}:8082/hls/device{device.id}.m3u8",
            "name": device.name,
            "ip": device.ip,
            "username": device.username,
            "password": device.password,
            "location": location.location,
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
            location = DeviceLocation.query.filter_by(
                device_id=int(data["device"]["id"][-2:])
            ).first()
            device.name = data["device"]["name"]
            device.username = data["device"]["username"]
            device.ip = data["device"]["ip"]
            device.password = data["device"]["password"]
            location.location = data["device"]["location"]

        if "fod" in data["func"]:
            nThreshold = int(data["fodCfg"]["nWarningThreshold"])
            exThreshold = int(data["fodCfg"]["exWarningThreshold"])
            if nThreshold > exThreshold - 100:
                nThreshold = exThreshold - 100
            if not FodCfg.query.filter_by(
                device_id=int(data["device"]["id"][-2:])
            ).scalar():
                virtual_gpu = VirtualGpu.query.filter_by(used=False).first()
                if virtual_gpu:
                    virtual_gpu.used = True
                    status_register.set(f"{device.id}_fod", "changed")
                    fodcfg = FodCfg(
                        device_id=data["device"]["id"][-2:],
                        n_warning_threshold=nThreshold,
                        ex_warning_threshold=exThreshold,
                        virtual_gpu_id=virtual_gpu.id,
                    )
                    db.session.add(fodcfg)
                else:
                    # FIXME not fully support
                    response["status"] = "error"
                    response["error"] = "检测数量达到上限"
                    return jsonify(response)
            else:
                fodcfg = FodCfg.query.filter_by(
                    device_id=int(data["device"]["id"][-2:])
                ).first()
                fodcfg.n_warning_threshold = nThreshold
                fodcfg.ex_warning_threshold = exThreshold
            status_register.set(
                f"fod_pipeline_{fodcfg.virtual_gpu_id}_nThreshold", nThreshold
            )
            status_register.set(
                f"fod_pipeline_{fodcfg.virtual_gpu_id}_exThreshold", exThreshold
            )

        else:
            if FodCfg.query.filter_by(
                device_id=int(data["device"]["id"][-2:])
            ).scalar():
                status_register.set(f"{device.id}_fod", "changed")
                fod_cfg = FodCfg.query.filter_by(
                    device_id=int(data["device"]["id"][-2:])
                ).first()
                virtual_gpu = VirtualGpu.query.filter_by(
                    id=fod_cfg.virtual_gpu_id
                ).first()
                virtual_gpu.used = False
                db.session.delete(fod_cfg)

        if "bdd" in data["func"]:
            if not BddCfg.query.filter_by(
                device_id=int(data["device"]["id"][-2:])
            ).scalar():
                bddcfg = BddCfg(
                    device_id=data["device"]["id"][-2:],
                    offset_distance=int(data["bddCfg"]["offsetDistance"]),
                )
                db.session.add(bddcfg)
            else:
                bddcfg = BddCfg.query.filter_by(
                    device_id=int(data["device"]["id"][-2:])
                ).first()
                bddcfg.offset_distance = (int(data["bddCfg"]["offsetDistance"]),)
        else:
            if BddCfg.query.filter_by(
                device_id=int(data["device"]["id"][-2:])
            ).scalar():
                bdd_cfg = BddCfg.query.filter_by(
                    device_id=int(data["device"]["id"][-2:])
                ).first()
                db.session.delete(bdd_cfg)
        db.session.commit()
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
            # FIXME conditions are redundant
            or_(
                FodRecord.status == "严重预警！",
                FodRecord.status == "severe",
                FodRecord.status == "严重预警",
            )
        ).count()
        response["devices"] = [
            {"id": device.id, "deviceName": device.name}
            for device in Device.query.order_by(Device.id).all()
        ]
        return jsonify(response)
