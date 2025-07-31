import os
from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import models
from backend.app.database import Base
from backend.app.main import app
from backend.app.routers import predictions as pred_router


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[pred_router.get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


def create_sample_prediction(db):
    team_a = models.Team(name="Team A")
    team_b = models.Team(name="Team B")
    db.add_all([team_a, team_b])
    db.commit()

    match = models.Match(date=datetime.utcnow(), team_a=team_a, team_b=team_b)
    db.add(match)
    db.commit()

    odd = models.BookmakerOdd(match_id=match.id, outcome="A", odd=2.0)
    db.add(odd)
    db.commit()

    pred = models.Prediction(match_id=match.id, outcome="A", probability=0.6)
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred


def test_is_value_bet_true(db_session):
    pred = create_sample_prediction(db_session)
    assert pred_router._is_value_bet(pred, db_session) is True


def test_valuebets_endpoint(client, db_session):
    pred = create_sample_prediction(db_session)
    response = client.get("/predictions/valuebets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["id"] == pred.id and item["is_value_bet"] for item in data)
