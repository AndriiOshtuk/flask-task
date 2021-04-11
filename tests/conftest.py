import pytest

from app import app as flask_application
from models import db as _db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_application.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite://"
    )  # SQLite :memory: database
    with flask_application.app_context():
        yield flask_application
        # _db.session.rollback()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(autouse=True)
def db(app):
    """
    Fixture is automatically used where DB state can be changed.
    """
    _db.create_all()
    _db.session.begin_nested()

    yield _db

    _db.drop_all()


@pytest.fixture(autouse=True)
def session(db):
    with db.engine.connect() as connection:
        transaction = connection.begin()

        db.session.begin_nested()

        yield db.session

        if transaction.is_active:
            transaction.rollback()
