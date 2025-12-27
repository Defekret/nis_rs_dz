class TestDatabaseConnection:
    def test_get_db_generator(self):
        from app.infrastructure.database import get_db

        db_gen = get_db()
        assert db_gen is not None

        try:
            session = next(db_gen)
            assert session is not None
        finally:
            try:
                next(db_gen)
            except StopIteration:
                pass


class TestAPIRoutersErrorHandling:
    def test_dictionary_validation_error(self):
        from fastapi.testclient import TestClient

        from app.main import app

        client = TestClient(app)

        response = client.post(
            "/api/v1/dictionaries/",
            json={
                "name": "   ",
                "source_language": "en",
                "target_language": "ru",
            },
        )

        assert response.status_code in [400, 422]
