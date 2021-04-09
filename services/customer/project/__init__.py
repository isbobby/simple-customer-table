import redis
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
from flask_jwt_extended import JWTManager


from project.customer_api.controller import customer_api
from project.auth_api.controller import auth_api

ACCESS_EXPIRES = timedelta(hours=1)

app = Flask(__name__)
app.config.from_object("project.config.Config")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
db = SQLAlchemy(app)

# create redis store
store = RedisStore(redis.StrictRedis())
KVSessionExtension(store, app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

# Create redis cache to store blocked tokens
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


# Create models
class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Customers(db.Model):
    __tablename__ = "customers"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, dob, updated_at):
        self.name = name
        self.dob = dob
        self.updated_at = updated_at


app.register_blueprint(customer_api)
app.register_blueprint(auth_api)
