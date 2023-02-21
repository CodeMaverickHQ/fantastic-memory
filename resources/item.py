import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items

blp = Blueprint("Items", __name__, description="Operations on Items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="item not found")
    
    def put(self, item_id):
        item_data = request.get_json()
        print(item_data)
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="ensure all data is provided (price, name)")
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item deleted"}
        except KeyError:
            abort(404, message="item not found")

@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}
    
    def post(self):
        item_data = request.get_json()
        if(
            "price" not in item_data
            or "store_id" not in item_data
            or "name" not in item_data
        ):
            abort(
                400,
                message=" bad request, ensure price, store_id and name are included in the JSON payload"
            )
        for item in items.values():
            if (
                item_data['name'] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="item already exists")

        if item_data["store_id"] not in stores:
            abort(404, message="store not found")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] =item
        return item, 201 
