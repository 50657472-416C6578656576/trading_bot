import json

from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
from flask_session import Session

from web_app.config import ApplicationConfig
from web_app.db import db, User
from trading_bot import Trader


app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/@me")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email
    })


@app.route("/register", methods=["POST"])
def register_user():
    email = request.json["email"]
    password = request.json["password"]

    user_exists = User.query.filter_by(email=email).first() is not None

    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(
        email=email, password=hashed_password, api_key=request.json['api_key'], secret=request.json['secret'],
    )
    db.session.add(new_user)
    db.session.commit()

    session["user_id"] = new_user.id

    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })


@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "email": user.email
    })


@app.route("/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"


@app.route('/start_trading', methods=['POST'])
def start_trading():
    data = request.get_json(force=True)
    api_key, secret, strategy, symbol, timeframe = \
        data['api_key'], data['secret'], data['strategy'], data['symbol'], data['timeframe']
    trader = Trader(api_key, secret, strategy, symbol, timeframe)
    thread = Thread(target=trader.start_trading)
    # thread.daemon = True
    thread.start()
    return json.dumps({
        'thread': f'{thread.getName()}',
        'data': data
    })
