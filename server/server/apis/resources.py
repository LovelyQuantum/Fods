from flask import jsonify, request
from flask.views import MethodView
from server.models import Device, FodRecord
from datetime import datetime, timedelta
from sqlalchemy import or_
import numpy as np


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
                "id": f"camera{str(device.id).zfill(2)}",
                "path": f"rtsp://{device.username}:{device.password}"
                f"@{device.ip}:554/Streaming/Channels/1",
            }
            for device in Device.query.order_by(Device.id).all()
        ]
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
                    "deviceName": Device.query.filter_by(id=record.device_id)[0].name,
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
