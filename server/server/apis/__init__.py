from flask import Blueprint
from flask_cors import CORS
from server.apis import resources


apis = Blueprint("apis", __name__)
CORS(apis)
apis.add_url_rule("/test", view_func=resources.TestAPI.as_view("test"), methods=["GET"])
apis.add_url_rule(
    "/get_device_info",
    view_func=resources.DeviceInfoAPI.as_view("device_info"),
    methods=["GET"],
)
apis.add_url_rule(
    "/fod_record",
    view_func=resources.FodRecordAPI.as_view("fod_record"),
    methods=["POST"],
)
apis.add_url_rule(
    # FIXME change method into GET
    "/fod_record_preview",
    view_func=resources.FodRecordPreview.as_view("fod_record_preview"),
    methods=["POST"],
)
apis.add_url_rule(
    "/fod_record_report",
    view_func=resources.FodRecordReportAPI.as_view("fod_record_report"),
    methods=["POST"],
)
apis.add_url_rule(
    "/device_setting",
    view_func=resources.DeviceSettingAPI.as_view("device_setting"),
    methods=["GET", "POST"],
)
apis.add_url_rule(
    "/system_info",
    view_func=resources.SystemInfoAPI.as_view("system_info"),
    methods=["GET", "POST"],
)
apis.add_url_rule(
    "/fod_device_record_report",
    view_func=resources.FodDeviceRecordReportAPI.as_view("fod_device_record_report"),
    methods=["GET", "POST"],
)
apis.add_url_rule(
    "/fod_device_record",
    view_func=resources.FodDeviceRecordAPI.as_view("fod_device_record"),
    methods=["GET", "POST"],
)
