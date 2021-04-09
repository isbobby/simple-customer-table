from werkzeug.security import generate_password_hash, check_password_hash

from project.database import db


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
