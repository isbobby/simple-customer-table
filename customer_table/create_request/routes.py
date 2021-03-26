from flask import Blueprint

create_request = Blueprint('create_request', __name__)

@create_request.route("/createCustomer", methods=['POST'])
def create_customer():
    return 200
