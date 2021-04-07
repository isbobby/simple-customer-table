from datetime import date, datetime
import json

from flask import Flask, jsonify
import sqlalchemy
from flask import Blueprint, request, Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from project.database import db
from .model import User

auth_api = Blueprint('auth_api', __name__)

@auth_api.route("/login", methods=["POST"])
def login():
    # Retrieve the user info from post request
    try:
        data_obj = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        reply_string = json.dumps("Please ensure you have sent JSON in to correct format, see developer's guide for more information")
        return make_response(400, reply_string)
        
    try:
        attempt_username = data_obj["username"]
        attempt_password = data_obj["password"]
    except KeyError:
        reply_string = json.dumps("Please ensure you have provided both username and password see developer's guide for more information")
        return make_response(400, reply_string)
    except ValueError:
        reply_string = json.dumps("Please ensure you have provided both username and password, see developer's guide for more information")
        return make_response(400, reply_string)

    # locate the customer to be updated
    try:
        attempt_user = User.query.filter(User.username==attempt_username).one()
    except sqlalchemy.orm.exc.NoResultFound:
        reply_string = json.dumps("No user found for given username")
        return make_response(400, reply_string)

    # check password match
    if (attempt_user.check_password(attempt_password)):
        access_token = create_access_token(identity="test")
        return jsonify(access_token=access_token)
    
    reply_string = json.dumps("Wrong password")
    return make_response(400, reply_string)
