from models import db, Item, List, ListItems, Store, Purchase
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
from flask_restful import Api
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'grocery.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

from routes import register_routes
register_routes(app)

if __name__ == "__main__":
    app.run(port=5555, debug=True)
