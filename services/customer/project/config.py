import os
from datetime import timedelta

# timeout value
ACCESS_EXPIRES = timedelta(hours=1)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://leipetushood:1234567890@localhost:5432/customer_table"
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
