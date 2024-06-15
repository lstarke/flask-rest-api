import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("Stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):

    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")

@blp.route("/store")
class StoreList(MethodView):

    def get(self):
        return {"stores": list(stores.values())}
    
    def post(self):
        store_data = request.get_json()

        # validação do payload
        if "name" not in store_data:
            abort(400, message="Bad request. Ensure 'name' is included in the JSON payload.")
        
        # validação se store já existe
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message="Store already exists.")

        store_id = uuid.uuid4().hex # gera um identificador único universal (UUID) 
        store = {**store_data, "id": store_id} # O operador ** é usado para desempacotar todos os pares chave-valor do dicionário store_data e inseri-los no novo dicionário.
        stores[store_id] = store
        return store, 201
