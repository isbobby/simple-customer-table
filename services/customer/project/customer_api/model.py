from project.database import db

# Create models
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
