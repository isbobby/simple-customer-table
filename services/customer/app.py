from datetime import datetime 

from flask.cli import FlaskGroup

from project import app, db
from project.customer_api.model import User, Customers

cli = FlaskGroup(app)


@cli.command("create_db_demo")
def create_db():
    db.drop_all()
    db.create_all()
    ### Create a test user and some dummy data
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


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("DB created")


if __name__ == '__main__':
    cli()
