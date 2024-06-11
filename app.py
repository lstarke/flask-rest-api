import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

@app.get("/store") # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
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

@app.post("/item")
def create_item():
    item_data = request.get_json()

    # validação do payload
    if(
        "price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data
    ):
        print("passou")
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

@app.get("/item") # http://127.0.0.1:5000/item
def get_all_items():
    return {"items": list(items.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Store not found")

    