from datetime import datetime
import json


import flask
import sqlalchemy
from flask import Blueprint, request, make_response
from flask_jwt_extended import jwt_required


from project.database import db
from project.model import Customers

customer_api = Blueprint('customer_api', __name__)


@customer_api.route("/customers", methods=['GET'])
@jwt_required()
def customer_get_controller():
    if flask.request.method == 'GET':
        # number n allows users to specify the number of youngest customers
        n_string = request.args.get('number')

        # return all by default, when n is not specified
        if n_string is None:
            return _customer_get_all()

        # ensures that n can be converted into an integer
        try:
            n = int(n_string)
        except ValueError:
            reply_string = json.dumps("Please try again with a different argument n. n should be an integer")
            return make_response(reply_string, 400)
        # ensure n is int and bigger than 0, if it isn't inform the user
        try:
            assert (n >= 0)
        except AssertionError:
            # user enters wrong n argument, return an error message
            reply_string = json.dumps("Please try again with a different argument n. n should be an integer larger "
                                      "than 0")
            return make_response(reply_string, 400)

        # return n youngest customers
        return _customer_get(n)

    else:
        # user enters wrong n argument, return an error message
        return make_response("Only get requests are allowed", 405)


def _customer_get(n):
    try:
        customers = Customers.query.order_by(Customers.dob.desc()).limit(n).all()
    except Exception:
        return make_response(json.dumps("Error in retrieving customers, contact admin for assistance"), 500)

    # populate response lists
    customer_list = []
    for customer in customers:
        customer_map = {
            "id": customer.id,
            "name": customer.name,
            "dob": str(customer.dob),
            "updated_at": customer.updated_at.strftime('%m/%d/%Y, %H:%M:%S'),
        }
        customer_list.append(customer_map)

    response_body = {
        "number": len(customer_list),
        "customers": customer_list
    }

    return make_response(json.dumps(response_body), 200)


def _customer_get_all():
    try:
        customers = Customers.query.all()
    except Exception:
        return make_response(json.dumps("Error in retrieving customers, contact admin for assistance"), 500)

    # populate response lists
    customer_list = []
    for customer in customers:
        customer_map = {
            "id": customer.id,
            "name": customer.name,
            "dob": str(customer.dob),
            "updated_at": customer.updated_at.strftime('%m/%d/%Y, %H:%M:%S'),
        }
        customer_list.append(customer_map)

    response_body = {
        "number": len(customer_list),
        "customers": customer_list
    }

    return make_response(json.dumps(response_body), 200)


@customer_api.route("/customers/create", methods=['POST'])
@jwt_required()
def customer_create_controller():
    try:
        data_obj = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        reply_string = json.dumps(
            "Please ensure you have sent JSON in to correct format, see developer's guide for more information")
        return make_response(reply_string, 400)

    # converting dob string to date object (YYYY-MM-DD) as specified in doc
    try:
        customer_dob_string = data_obj["dob"]
        customer_name = data_obj["name"]
        customer_dob_date = datetime.strptime(customer_dob_string, '%Y-%m-%d').date()
    except KeyError:
        reply_string = json.dumps(
            "Please ensure you have included name and dob of customer, see developer's guide for more information")
        return make_response(reply_string, 400)
    except ValueError:
        reply_string = json.dumps(
            "Please ensure you have provided valid dob of customer, see developer's guide for more information")
        return make_response(reply_string, 400)

    # get the last updated time (now)
    time_now = datetime.now()

    # create a customer ORM object
    entry = Customers(customer_name, customer_dob_date, time_now)
    db.session.add(entry)
    db.session.commit()
    return make_response(
        json.dumps(f"You have added {customer_name} who is born on {customer_dob_string}, updated at {time_now}"), 200)


@customer_api.route("/customers/update", methods=['POST'])
@jwt_required()
def customerUpdateController():
    try:
        data_obj = json.loads(request.data)
    except json.decoder.JSONDecodeError:
        reply_string = json.dumps(
            "Please ensure you have sent JSON in to correct format, see developer's guide for more information")
        return make_response(reply_string, 400)

    # converting dob string to date object (YYYY-MM-DD) as specified in doc
    try:
        customer_id = int(data_obj["id"])
        customer_dob_string = data_obj["dob"]
        customer_name = data_obj["name"]
        customer_dob_date = datetime.strptime(customer_dob_string, '%Y-%m-%d').date()
    except KeyError:
        reply_string = json.dumps(
            "Please ensure you have included id, new name and dob of customer, see developer's guide for more information")
        return make_response(reply_string, 400)
    except ValueError:
        reply_string = json.dumps(
            "Please ensure you have included id, new name and dob of customer, see developer's guide for more information")
        return make_response(reply_string, 400)

    # get the last updated time (now)
    time_now = datetime.now()

    # locate the customer to be updated
    try:
        update_customer = Customers.query.filter(Customers.id == customer_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        reply_string = json.dumps("Please ensure you have provided valid customer id")
        return make_response(reply_string, 400)

    update_customer.dob = customer_dob_date
    update_customer.name = customer_name
    update_customer.updated_at = time_now
    db.session.commit()
    return make_response(json.dumps(f"You have updated customer whose id is {customer_id}"), 200)


@customer_api.route("/customers/delete", methods=['DELETE'])
@jwt_required()
def _customer_delete():
    # get the id of the customer to be deleted
    try:
        customer_id = int(request.args.get('id'))
    except ValueError:
        reply_string = "Please ensure you have provided valid customer id"
        response_body = json.dumps(reply_string)
        return make_response(response_body, 400)

    # locate the customer to be deleted
    try:
        delete_customer = Customers.query.filter(Customers.id == customer_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        reply_string = "This customer does not exist"
        response_body = json.dumps(reply_string)
        return make_response(response_body, 400)

    db.session.delete(delete_customer)
    db.session.commit()
    return make_response(f"You have deleted customer whose id is {customer_id}", 200)
