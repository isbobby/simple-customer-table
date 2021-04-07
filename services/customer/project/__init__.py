from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from project.customer_api.controller import customer_api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    access_token = create_access_token(identity="test")
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, email, password):
        self.username = username
        self.password = password


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
