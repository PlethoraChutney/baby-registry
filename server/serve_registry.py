from flask import Flask, request, make_response
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
import json
import os
import sys
from pathlib import Path

try:
    REG_KEY=os.environ["WALDO_REG_KEY"]
except KeyError:
    print("Set WALDO_REG_KEY variable")
    sys.exit(1)

try:
    REG_PW=os.environ["WALDO_REG_PW"]
except KeyError:
    print("Set WALDO_REG_PW variable")
    sys.exit(1)

SERVER_SRC_DIR = Path(__file__).parent
with open(SERVER_SRC_DIR.parent / "src" / "assets" / "items-info.json", "r") as f:
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
    def __init__(self, db_location = None, homepage_location = None):
        if db_location is None:
            db_location = SERVER_SRC_DIR / "reg_db.json"
        self.db_location = db_location

        try:
            with open(self.db_location, "r") as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {"items": {}, "users": {}}

        for uuid, item_info in registry_info.items():
            quantity = get_quantity_guess(item_info["quantity"])
            if uuid in self.db["items"]:
                # always update in case we change the desired quantity
                self.db["items"][uuid]["numeric_quant"] = quantity
            else:
                item_info.update({
                    "numeric_quant": quantity,
                    "purchased": 0
                })
                self.db["items"][uuid] = item_info

        self.save()

        if homepage_location is None:
            homepage_location = SERVER_SRC_DIR / "homepage-info.json"
        self.homepage_location = homepage_location
        self.reload_homepage()

    def save(self):
        with open(self.db_location, "w") as f:
            json.dump(self.db, f)

    @property
    def users(self):
        return self.db["users"]

    @property
    def quantities(self):
        return {
            uuid: item["quantity"] for uuid, item in self.db["items"].items()
        }
    
    @property
    def purchased(self):
        return [
            (uuid, item["purchased"]) for uuid, item in self.db["items"].items()
        ]
    
    @property
    def items(self):
        return dict(sorted(
            self.db["items"].items(),
            key = lambda i: i[1]["numeric_quant"] is not None and i[1]["purchased"] == i[1]["numeric_quant"]
        ))
    
    def purchase_item(self, uuid:str, num_purchased:int):
        try:
            num_purchased = int(num_purchased)
            if num_purchased < 1:
                raise ValueError

            old_info = self.db["items"][uuid]
            if (
                old_info["quantity"] is not None
                and old_info["purchased"] + num_purchased > old_info["numeric_quant"]
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
        
    def reload_homepage(self):
        try:
            with open(self.homepage_location, "r") as f:
                self.homepage = json.load(f)
        except FileNotFoundError:
            self.homepage = {}

    def get_user(self, user_id):
        if user_id not in self.users:
            self.create_user(user_id)
        return User(user_id, self)

    def create_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {"purchased": {}}

    @property
    def user_purchases(self):
        to_return = {}
        for user, purchase_dict in self.users.items():
            to_return[user] = {}
            for item, quantity in purchase_dict["purchased"].items():
                item_name = self.items[item]["label"]
                to_return[user][item_name] = quantity

        return to_return

class User(UserMixin):
    def __init__(self, id:str, db:Database):
        self.id = id
        self.db = db

    def purchase_item(self, uuid, num_purchased):
        result = self.db.purchase_item(uuid, num_purchased)
        if result[0]:
            if uuid not in self.db.users[self.id]["purchased"]:
                self.db.users[self.id]["purchased"][uuid] = num_purchased
            else:
                self.db.users[self.id]["purchased"][uuid] += num_purchased
            self.db.save()
        return result


db = Database()

app = Flask(__name__)
app.secret_key = REG_KEY
app.json.sort_keys = False

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_user(user_id)

@app.route("/api/login/", methods = ["GET"])
def check_auth():
    return make_response(
        {
            "is_authenticated": current_user.is_authenticated,
        },
        200
    )

@app.route("/api/login/", methods = ["POST"])
def login():
    r = request.json
    if any(x not in r for x in ["user_id", "password"]):
        return make_response(
            {
                "success": False,
                "error": "Missing username or password."
            },
            400
        )
    
    if (r["password"] != REG_PW):
        return make_response(
            {
                "success": False,
                "error": "Wrong password."
            },
            400
        )
    
    login_user(db.get_user(r["user_id"]), remember = True)
    return make_response(
        {
            "success": True,
            "user_id": current_user.id
        },
        200
    )

@app.route("/api/items/", methods = ["GET"])
@login_required
def get_items():
    return make_response(
        db.items,
        200
    )

@app.route("/api/purchased/", methods = ["GET"])
@login_required
def get_purchase_status():
    return make_response(
        db.purchased,
        200
    )

@app.route("/api/purchase_item/", methods = ["POST"])
@login_required
def purchase_item():
    r = request.json
    try:
        uuid = r["uuid"]
        num_purchased = r["num_purchased"]
    except KeyError as e:
        return make_response({"error": "missing key"}, 400)
    
    result = current_user.purchase_item(uuid, num_purchased)
    
    if result[0]:
        return make_response(
            {"new_purchased": result[1]},
            200
        )
    else:
        return make_response({"error": result[1]}, 400)
    
@app.route("/api/homepage_info/", methods = ["GET"])
@login_required
def get_homepage_info():
    return make_response(
        db.homepage,
        200
    )

@app.route("/api/reload_homepage/", methods = ["GET"])
def reload_homepage_info():
    db.reload_homepage()
    return make_response(
        {"result": "success"},
        200
    )

@app.route("/api/thank_you_cards/", methods = ["POST"])
def get_thank_yous():
    r = request.json
    if current_user.is_authenticated or r.get("registry_pw", "") == REG_PW:
        return make_response(
            db.user_purchases,
            200
        )
    else:
        return make_response(
            {"error": "Failed authentication"},
            401
        )