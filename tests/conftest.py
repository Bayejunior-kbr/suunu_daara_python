"""
Fixtures pytest partagées. Utilise la base PostgreSQL de test
(TestingConfig -> TEST_DATABASE_URL), conformément à l'énoncé
("PostgreSQL uniquement").
"""
import pytest
from app import create_app
from app.extension import db as _db


@pytest.fixture()
def app():
    application = create_app("testing")

    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db
