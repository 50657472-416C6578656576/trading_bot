from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session

from trading_bot import Trader
from web_app.config import ApplicationConfig
from web_app.db import db, User, TASKS, TraderTask


app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/profile")
def get_current_user():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        "id": user.id,
        "email": user.email,
        "api_key": user.api_key,
        "secret": user.secret
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
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(force=True)
    user = User.query.filter_by(id=user_id).first()
    api_key, secret = user.api_key, user.secret
    strategy, symbol, timeframe = data['strategy'], data['symbol'], data['timeframe']
    trading_balance = data.get('amount')
    task = TraderTask(api_key, secret, strategy, symbol, timeframe, trading_balance)
    task.run()
    return jsonify({
        'thread': f'{task.thread.name}',
    })


@app.route('/stop_trading', methods=['POST'])
def stop_trading():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401
    if (task := TASKS.get(user_id)) and task.is_running:
        task.stop()
        assert not task.is_running, 'Task was not stopped'
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'no running tasks'}), 404


@app.route('/balance', methods=['GET'])
def get_balance():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify({"error": "Unauthorized"}), 401

    if task := TASKS.get(user_id):
        balance = task.trader.get_balance()
        return jsonify({'balance': f'{balance}'})

    user = User.query.filter_by(id=user_id).first()
    api_key, secret = user.api_key, user.secret
    symbol = request.args.get('symbol')
    balance = Trader(api_key, secret, None, symbol, None).get_balance()
    return jsonify({'balance': f'{balance}'})
