from flask import Blueprint
from project.database import db

from .model import Customers, User

customer_api = Blueprint('customer_api', __name__)


@customer_api.route("/")
def mainHome():
    return "200"