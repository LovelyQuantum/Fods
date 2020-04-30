from flask import jsonify
from flask.views import MethodView


class IndexAPI(MethodView):
    def get(self):
        return jsonify(
            {
                "api_version": "1.0",
                "api_base_url": "http://example.com/api/v1",
                "current_user_url": "http://example.com/api/v1/user",
                "authentication_url": "http://example.com/api/v1/token",
                "item_url": "http://example.com/api/v1/items/{item_id }",
                "current_user_items_url": "http://example.com/api/v1/user/items"
                "{?page,per_page}",
                "current_user_active_items_url": "http://example.com/api/v1/user/items"
                "/active{?page,per_page}",
                "current_user_completed_items_url": "http://example.com/api/v1/user"
                "/items/completed{?page,per_page}",
            }
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
