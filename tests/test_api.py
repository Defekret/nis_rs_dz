import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure import Base, get_db
from app.main import app

# Создаём тестовую БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestDictionaryAPI:
    def test_create_dictionary(self):
        dictionary_data = {
            "name": "English Idioms",
            "description": "Collection of idioms",
            "source_language": "en",
            "target_language": "ru",
        }

        response = client.post("/api/v1/dictionaries/", json=dictionary_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "English Idioms"
        assert data["description"] == "Collection of idioms"
        assert data["source_language"] == "en"
        assert data["target_language"] == "ru"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_dictionary_with_invalid_data(self):
        invalid_data = {
            "name": "",
            "source_language": "en",
            "target_language": "ru",
        }

        response = client.post("/api/v1/dictionaries/", json=invalid_data)

        assert response.status_code == 422

    def test_get_dictionary_by_id(self):
        create_response = client.post(
            "/api/v1/dictionaries/",
            json={
                "name": "Test Dictionary",
                "source_language": "en",
                "target_language": "ru",
            },
        )
        dictionary_id = create_response.json()["id"]

        response = client.get(f"/api/v1/dictionaries/{dictionary_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == dictionary_id
        assert data["name"] == "Test Dictionary"

    def test_get_nonexistent_dictionary(self):
        fake_id = "123e4567-e89b-12d3-a456-426614174000"

        response = client.get(f"/api/v1/dictionaries/{fake_id}")

        assert response.status_code == 404

    def test_get_all_dictionaries(self):
        client.post(
            "/api/v1/dictionaries/",
            json={
                "name": "Dictionary 1",
                "source_language": "en",
                "target_language": "ru",
            },
        )
        client.post(
            "/api/v1/dictionaries/",
            json={
                "name": "Dictionary 2",
                "source_language": "fr",
                "target_language": "ru",
            },
        )

        response = client.get("/api/v1/dictionaries/")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["dictionaries"]) == 2

    def test_get_dictionaries_with_pagination(self):
        for i in range(5):
            client.post(
                "/api/v1/dictionaries/",
                json={
                    "name": f"Dictionary {i}",
                    "source_language": "en",
                    "target_language": "ru",
                },
            )

        response = client.get("/api/v1/dictionaries/?skip=2&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data["dictionaries"]) == 2

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
