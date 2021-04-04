from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from project.customer_api.controller import customer_api

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, email):
        self.email = email

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
