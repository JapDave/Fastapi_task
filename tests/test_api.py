import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app import app
from app.database import get_db
from app.models import Base, User


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    def database():
        with sessions() as db:
            yield db
    app.dependency_overrides[get_db] = database
    with TestClient(app) as client:
        yield client, sessions
    app.dependency_overrides.clear()
    engine.dispose()


def signup(client, email):
    response = client.post("/auth/signup", json={"email": email, "password": "StrongP@ss1!"})
    assert response.status_code == 201
    return response.json()["token"]


def test_authentication_and_hashed_password(client):
    api, sessions = client
    token = signup(api, "one@example.com")
    with sessions() as db:
        assert db.query(User).first().password.startswith("scrypt$")
    assert api.post("/auth/signup", json={"email": "one@example.com", "password": "StrongP@ss1!"}).status_code == 409
    assert api.post("/auth/login", json={"email": "one@example.com", "password": "wrong"}).status_code == 401
    response = api.post("/auth/login", json={"email": "one@example.com", "password": "StrongP@ss1!"})
    assert response.status_code == 200
    assert response.json()["token"] != token
    assert api.get("/posts", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    assert api.get("/posts").status_code == 401


def test_post_ownership_and_fresh_reads(client):
    api, _ = client
    owner = {"Authorization": f"Bearer {signup(api, 'owner@example.com')}"}
    other = {"Authorization": f"Bearer {signup(api, 'other@example.com')}"}
    assert api.get("/posts", headers=owner).json() == []
    response = api.post("/posts", headers=owner, json={"text": "Hello"})
    assert response.status_code == 201
    post_id = response.json()["postID"]
    assert api.get("/posts", headers=owner).json() == [{"postID": post_id, "text": "Hello"}]
    assert api.get("/posts", headers=other).json() == []
    assert api.delete(f"/posts/{post_id}", headers=other).status_code == 404
    assert api.delete(f"/posts/{post_id}", headers=owner).status_code == 200
    assert api.get("/posts", headers=owner).json() == []
    assert api.delete(f"/posts/{post_id}", headers=owner).status_code == 404
