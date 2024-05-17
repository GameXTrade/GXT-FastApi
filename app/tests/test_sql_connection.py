from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.db import Base, get_db
from app.main import app


POSTGRESQL_ACCESS_URL = "postgresql://"

engine = create_engine(
    POSTGRESQL_ACCESS_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/user",
        json={"username": "Joe", "email": "name@mail.com", "password": "1", "image":""},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "Joe"
    assert "id" in data
