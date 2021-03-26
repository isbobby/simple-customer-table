from flask import Flask
from customer_table.create_request.routes import create_request
from customer_table.read_request.routes import read_request

def create_app():
    app = Flask(__name__)
    app.register_blueprint(create_request)
    app.register_blueprint(read_request)
    return app
