from flask.cli import FlaskGroup

from project import app, db

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("DB created")


if __name__ == '__main__':
    cli()
