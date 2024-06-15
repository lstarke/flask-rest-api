import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("Item", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):

    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete (self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
            item_data = request.get_json()
    
            if "price" not in item_data or "name" not in item_data:
                abort(400, message="Bad request. Ensure 'price', and 'name' are includes in the JSON payload.")

            try:
                item = items[item_id]
                # https://blog.teclado.com/python-dictionary-merge-update-operators/
                # a partir do Python 3.9 para atualizar um dicionário inplace
                item |= item_data
                return item
            except KeyError:
                abort(404, message="Item not found.")

@blp.route("/item")
class ItemList(MethodView):

    def get(self):
        return {"items": list(items.values())}
    
    def post(self):
            item_data = request.get_json()

            # validação do payload
            if(
                "price" not in item_data or
                "store_id" not in item_data or
                "name" not in item_data
            ):
                abort(400, message="Bad request. Ensure 'price', 'store_id' and 'name' are includes in the JSON payload.")
            # validação se item já existe
            for item in items.values():
                if (
                    item_data["name"] == item["name"] and
                    item_data["store_id"] == item["store_id"]
                ):
                    abort(400, message=f"Item already exist.")
            
            
            item_id = uuid.uuid4().hex # gera um identificador único universal (UUID) 
            item = {**item_data, "id": item_id} # O operador ** é usado para desempacotar todos os pares chave-valor do dicionário store_data e inseri-los no novo dicionário.
            items[item_id] = item
            
            return item, 201