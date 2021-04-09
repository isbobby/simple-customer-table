import json


from flask import jsonify
import sqlalchemy
from flask import Blueprint, request, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt


from project.config import ACCESS_EXPIRES
from .model import User
from project.utils import key_generator
from project.myRedis import jwt_redis_block_list, redis_session_list

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/login", methods=["POST"])
def login():
    # Retrieve the user info from post request
    try:
        data_obj = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        reply_string = json.dumps("Please ensure you have sent JSON in to correct format, see developer's guide for "
                                  "more information")
        return make_response(reply_string, 400)

    try:
        attempt_username = data_obj["username"]
        attempt_password = data_obj["password"]
    except KeyError:
        reply_string = json.dumps("Please ensure you have provided both username and password see developer's guide "
                                  "for more information")
        return make_response(reply_string, 400)
    except ValueError:
        reply_string = json.dumps("Please ensure you have provided both username and password, see developer's guide "
                                  "for more information")
        return make_response(reply_string, 400)

    # locate the customer to be updated
    try:
        attempt_user = User.query.filter(User.username == attempt_username).one()
    except sqlalchemy.orm.exc.NoResultFound:
        reply_string = json.dumps("No user found for given username")
        return make_response(reply_string, 400)

    # check password match
    if attempt_user.check_password(attempt_password):
        access_token = create_access_token(identity="test")

        # make a session cookie to store at client side but also
        # store this in the server side
        response = make_response(
            jsonify(access_token=access_token),
            200,
        )
        session_id = key_generator(126)
        response.set_cookie('session', session_id)

        # tag the access_token to this session, so only one session is
        # allowed
        redis_session_list.set(access_token, session_id)
        return response

    reply_string = json.dumps("Wrong password")
    return make_response(reply_string, 400)


@auth_api.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    header_string = request.headers.get("Authorization")
    access_token = header_string.split()[1]

    jti = get_jwt()["jti"]
    jwt_redis_block_list.set(jti, "", ex=ACCESS_EXPIRES)

    # get the session id to be removed
    redis_session_list.delete(access_token)
    return jsonify(msg="Access token revoked")


@auth_api.route("/session_cookie_experiment", methods=["GET"])
def session_cookie_matching():
    session_id = request.cookies.get("session")

    header_string = request.headers.get("Authorization")
    access_token = header_string.split()[1]
    server_session_id = redis_session_list.get(access_token)

    if session_id == server_session_id:
        return '200'
    else:
        response = make_response(
            jsonify("You have stole the access token from someone!"),
            400
        )
        return response
