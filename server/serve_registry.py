from flask import Flask, request, make_response, send_file, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required
import json
import os
import sys
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

launch_error = False
try:
    REG_KEY=os.environ["WALDO_REG_KEY"]
except KeyError:
    logger.error("WALDO_REG_KEY secret not set. Use a secure random value!")
    launch_error = True

try:
    REG_PW=os.environ["WALDO_REG_PW"]
except KeyError:
    logger.error("WALDO_REG_PW not set")
    launch_error = True

try:
    REG_ADMIN_PW=os.environ["WALDO_REG_ADMIN_PW"]
except KeyError:
    logger.error("WALDO_REG_ADMIN_PW not set")
    launch_error = True

try:
    REG_NAME_LIMIT = int(os.environ["WALDO_REG_NAME_LIMIT"])
except KeyError:
    logger.warning("WALDO_REG_NAME_LIMIT not set. Using default of 5")
    REG_NAME_LIMIT = 5
except ValueError:
    logger.error(f"WALDO_REG_NAME_LIMIT set to a bad value of {os.environ['WALDO_REG_NAME_LIMIT']}. Must be an integer.")
    launch_error = True

if launch_error:
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
    def __init__(self, db_location = None) -> None:
        if db_location is None:
            db_location = SERVER_SRC_DIR / "reg_db.json"
        self.db_location = db_location

        try:
            with open(self.db_location, "r") as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {"items": {}, "users": {}, "name_suggestions": {}}

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

    def save(self) -> None:
        with open(self.db_location, "w") as f:
            json.dump(self.db, f)

    @property
    def users(self) -> dict[str, dict]:
        return self.db["users"]
    
    @property
    def items(self) -> dict[str, dict]:
        return dict(sorted(
            (x for x in self.db["items"].items() if not x[1]["deleted"]),
            key = lambda i: i[1]["numeric_quant"] is not None and i[1]["purchased"] == i[1]["numeric_quant"]
        ))

    @property
    def quantities(self) -> dict[str, str]:
        return {
            uuid: item["quantity"] for uuid, item in self.items.items()
        }
    
    @property
    def purchased(self) -> list[tuple]:
        return [
            (uuid, item["purchased"]) for uuid, item in self.items.items()
        ]
    
    def purchase_item(self, uuid:str, num_purchased:int) -> tuple[bool, str]:
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

    def get_user(self, user_id:str) -> "User":
        if user_id not in self.users:
            self.create_user(user_id)
        return User(user_id, self)

    def create_user(self, user_id:str) -> None:
        if user_id not in self.users:
            self.users[user_id] = {"purchased": {}}

    @property
    def user_purchases(self) -> dict:
        to_return = {}
        for user, purchase_dict in self.users.items():
            to_return[user] = {}
            for item, quantity in purchase_dict["purchased"].items():
                item_name = self.items[item]["label"]
                to_return[user][item_name] = quantity

        return to_return
    
    @property
    def name_suggestions(self) -> dict:
        return self.db["name_suggestions"]
    
    def reset_name_suggestions(self, user:str) -> None:
        self.db["name_suggestions"][user] = []

class User(UserMixin):
    def __init__(self, id:str, db:Database):
        self.id = id
        self.db = db

    @property
    def purchases(self):
        return self.db.users[self.id]["purchased"]

    def purchase_item(self, uuid:str, num_purchased:int) -> tuple[bool, str]:
        result = self.db.purchase_item(uuid, num_purchased)
        if result[0]:
            if uuid not in self.purchases:
                self.purchases[uuid] = num_purchased
            else:
                self.purchases[uuid] += num_purchased
            self.db.save()
        return result
    
    @property
    def name_suggestions(self):
        if self.id not in self.db.name_suggestions:
            self.db.name_suggestions[self.id] = []
            return []
        else:
            return self.db.name_suggestions[self.id]
    
    def suggest_name(self, name:str) -> tuple[bool, dict]:
        if len(self.name_suggestions) >= REG_NAME_LIMIT:
            return (False, {"error": f"You've already suggested {REG_NAME_LIMIT} names!"})

        if name in self.name_suggestions:
            return (False, {"error": f"You've already suggested {name}!"})

        self.name_suggestions.append(name)
        self.db.save()
        return (True, {"message": "Name submitted"})

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
            401
        )
    
    login_user(db.get_user(r["user_id"]), remember = True)
    return make_response(
        {
            "success": True,
            "user_id": current_user.id
        },
        200
    )

@app.route("/api/homepage-info/", methods = ["GET"])
@login_required
def homepage_info():
    return send_file("homepage-info.json")

@app.route("/api/calendar/<path>", methods = ["GET"])
@login_required
def calendar_info(path):
    return send_from_directory(SERVER_SRC_DIR / "calendar/", path, as_attachment = True)

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
    except KeyError:
        return make_response({"error": "missing key"}, 400)
    
    result = current_user.purchase_item(uuid, num_purchased)
    
    if result[0]:
        return make_response(
            {"new_purchased": result[1]},
            200
        )
    else:
        return make_response({"error": result[1]}, 400)

@app.route("/api/thank_you_cards/", methods = ["POST"])
def get_thank_yous():
    r = request.json
    if r.get("registry_pw", "") == REG_ADMIN_PW:
        return make_response(
            db.user_purchases,
            200
        )
    else:
        return make_response(
            {"error": "Failed authentication"},
            401
        )
    
@app.route("/api/name/", methods = ["GET"])
@login_required
def get_name_suggestions():
    return make_response(
        {
            "limit": REG_NAME_LIMIT,
            "current_suggestions": current_user.name_suggestions
        },
        200
    )
    
@app.route("/api/name/", methods = ["POST"])
@login_required
def suggest_name():
    r = request.json
    try:
        result = current_user.suggest_name(r["name"])
    except KeyError:
        return make_response(
            {"error": "No name submitted"},
            400
        )
    return make_response(
        result[1],
        200 if result[0] else 400
    )

@app.route("/api/name_list/", methods = ["POST"])
def get_name_list():
    r = request.json
    if r.get("registry_pw", "") == REG_ADMIN_PW:
        return make_response(
            db.name_suggestions,
            200
        )
    else:
        return make_response(
            {"error": "Failed authentication"},
            401
        )


@app.route("/api/reset_names/<user>/", methods = ["POST"])
def reset_names(user):
    r = request.json
    if r.get("registry_pw", "") == REG_ADMIN_PW:
        db.reset_name_suggestions(user)
        return make_response(
            {"result": "success"},
            200
        )
    else:
        return make_response(
            {"error": "Failed authentication"},
            401
        )
