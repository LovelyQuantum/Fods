from flask import Blueprint
from flask_cors import CORS
from server.apis import resources


apis = Blueprint('apis', __name__)
CORS(apis)
apis.add_url_rule("/", view_func=resources.IndexAPI.as_view("index"), methods=["GET"])
apis.add_url_rule("/test", view_func=resources.TestAPI.as_view("test"), methods=["GET"])