import os
import tempfile
from datetime import datetime


import pytest


from project import app, db
from ..model import User, Customers


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Create a test user and some dummy data
            test_user = User("klinify", "klinify")

            now = datetime.now()

            test_customer_1 = Customers("Alice", "1997-05-09", now)
            test_customer_2 = Customers("Charlie", "1996-09-27", now)
            test_customer_3 = Customers("Bobby", "2000-03-01", now)
            test_customer_4 = Customers("Duke", "1997-01-02", now)

            db.session.add(test_user)
            db.session.add(test_customer_1)
            db.session.add(test_customer_2)
            db.session.add(test_customer_3)
            db.session.add(test_customer_4)
            db.session.commit()
            print("DB created and populated with dummy data")
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_login(client):
    response = client.post('/login', data=dict(
        username='klinify',
        password='klinify'
    ), follow_redirects=True)

    # assert response.status, 200


def test_login_missing_attribute(client):
    response = client.post('/login', data=dict(
        username='klinify',
    ), follow_redirects=True)

    # assert response.status, 400
    # assert response.data, "Please ensure you have provided both username and password see developer's guide for more information"


def test_get_customers_without_login(client):
    response = client.get('/login', follow_redirects=True)
    # assert response.status, 401

def test_get_customers(client):
    client.post('/login', data=dict(
            username='klinify',
            password='klinify'
        ), follow_redirects=True)

    # response = client.get('/login', follow_redirects=True)
    # assert (response.status == 400)
