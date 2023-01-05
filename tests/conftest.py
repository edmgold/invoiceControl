import os
import pytest
import sqlalchemy

DATABASE_URL = 'sqlite:///:memory'
os.environ['DATABASE_URL'] = DATABASE_URL

from typing import Generator
from fastapi.testclient import TestClient

from main import create_application, startup, shutdown
from db import BaseMeta, database

@pytest.fixture
def db_conf():
    engine = sqlalchemy.create_engine(DATABASE_URL)
    BaseMeta.metadata.drop_all(bind=engine)
    BaseMeta.metadata.create_all(bind=engine)
    yield
    BaseMeta.metadata.drop_all(bind=engine)


@pytest.fixture
def app_with_db(db_conf):
    app = create_application(database=db_conf)
    app.on_startup = [startup]
    app.on_shutdown = [shutdown]
    yield app


@pytest.fixture
def client(app_with_db):
    yield TestClient(app=app_with_db, base_url="http://test")