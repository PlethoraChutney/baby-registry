from flask import Flask, request, make_response
import json
import os
from pathlib import Path

SERVER_SRC = Path(__file__).parent

with open(SERVER_SRC.parent / "src" / "assets" / "items-info.json", "r") as f:
    registry_info = json.load(f)

def get_quantity_guess(quant:str) -> int|None:
    try:
        return int(quant)
    except ValueError:
        pass

    try:
        return int(quant.split(" ")[0])
    except ValueError:
        return None

class Database:
    def __init__(self, db_location = None):
        if db_location is None:
            db_location = SERVER_SRC / "reg_db.json"
        self.db_location = db_location

        try:
            with open(self.db_location, "r") as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {"items": {}}

        for uuid, item_info in registry_info.items():
            quantity = get_quantity_guess(item_info["quantity"])
            if uuid in self.db["items"]:
                self.db["items"][uuid]["numeric_quant"] = quantity
            else:
                item_info["numeric_quant"] = quantity
                self.db["items"][uuid] = item_info


        self.save()

    def save(self):
        with open(self.db_location, "w") as f:
            json.dump(self.db, f)

    @property
    def quantities(self):
        return {
            uuid: item["quantity"] for uuid, item in self.db["items"].items()
        }
    
    @property
    def purchased(self):
        return {
            uuid: item["purchased"] for uuid, item in self.db["items"].items()
        }
    
    @property
    def items(self):
        return self.db["items"]
    
    def purchase_item(self, uuid:str, num_purchased:int):
        try:
            num_purchased = int(num_purchased)
            if num_purchased < 1:
                raise ValueError
            old_info = self.db["items"][uuid]
            if (
                old_info["quantity"] is not None
                and old_info["purchased"] + num_purchased > old_info["quantity"]
            ):
                raise ValueError
            old_info["purchased"] += num_purchased
            self.db["items"][uuid] = old_info
            self.save()
            return (True, old_info["purchased"])
        except TypeError:
            return (False, "Bad request")
        except ValueError:
            return (False, "Too many items or negative quantity")


db = Database()

app = Flask(__name__)

@app.route("/api/items", methods = ["GET"])
def get_items():
    return make_response(
        db.items,
        200
    )

@app.route("/api/get_purchase_status", methods = ["GET"])
def get_purchase_status():
    return make_response(
        db.purchased,
        200
    )

@app.route("/api/purchase_item/", methods = ["POST"])
def purchase_item():
    r = request.json
    try:
        result = db.purchase_item(r["uuid"], r["num_purchased"])
    except KeyError:
        return make_response({"error": "missing key"}, 400)
    
    if result[0]:
        return make_response(
            json.dumps(result[1]),
            200
        )
    else:
        return make_response({"error": result[1]}, 400)
