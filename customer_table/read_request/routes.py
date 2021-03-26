from flask import Blueprint

read_request = Blueprint('read_request', __name__)

@read_request.route("/getCustomer", methods=['GET'])
def get_customer_by_id():
    return "200"
