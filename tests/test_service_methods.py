from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.database import Base
from app.infrastructure.entry_repository import EntryRepository
from app.infrastructure.repository import DictionaryRepository
from app.services.dictionary_service import DictionaryService
from app.services.entry_service import EntryService


class TestDictionaryServiceMethods:
    @pytest.fixture
    def db_session(self):  # Create in-memory database
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        yield session
        session.close()

    @pytest.fixture
    def service(self, db_session):
        repo = DictionaryRepository(db_session)
        return DictionaryService(repo)

    def test_update_dictionary_success(self, service):
        created = service.create_dictionary(
            name="Original Name",
            source_language="en",
            target_language="ru",
            description="Original description",
        )

        updated = service.update_dictionary(
            dictionary_id=created.id,
            name="Updated Name",
            description="Updated description",
        )

        assert updated is not None
        assert updated.name == "Updated Name"
        assert updated.description == "Updated description"

    def test_update_nonexistent_dictionary(self, service):
        fake_id = uuid4()

        result = service.update_dictionary(dictionary_id=fake_id, name="New Name")

        assert result is None

    def test_delete_dictionary_success(self, service):
        created = service.create_dictionary(
            name="To Delete", source_language="en", target_language="ru"
        )

        result = service.delete_dictionary(created.id)

        assert result is True

        retrieved = service.get_dictionary(created.id)
        assert retrieved is None

    def test_delete_nonexistent_dictionary(self, service):
        fake_id = uuid4()

        result = service.delete_dictionary(fake_id)

        assert result is False


class TestEntryServiceMethods:
    @pytest.fixture
    def db_session(self):  # Create in-memory database
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        yield session
        session.close()

    @pytest.fixture
    def dictionary(self, db_session):
        dict_repo = DictionaryRepository(db_session)
        dict_service = DictionaryService(dict_repo)

        return dict_service.create_dictionary(
            name="Test Dictionary", source_language="en", target_language="ru"
        )

    @pytest.fixture
    def service(self, db_session):
        repo = EntryRepository(db_session)
        return EntryService(repo)

    def test_create_entry_with_all_fields(self, service, dictionary):
        entry = service.create_entry(
            dictionary_id=dictionary.id,
            original_text="Hello",
            translated_text="Привет",
            usage_example="Hello, world!",
            notes="Common greeting",
        )

        assert entry.original_text == "Hello"
        assert entry.translated_text == "Привет"
        assert entry.usage_example == "Hello, world!"
        assert entry.notes == "Common greeting"

    def test_create_entry_minimal_fields(self, service, dictionary):
        entry = service.create_entry(
            dictionary_id=dictionary.id, original_text="Test", translated_text="Тест"
        )

        assert entry.original_text == "Test"
        assert entry.translated_text == "Тест"
        assert entry.usage_example is None
        assert entry.notes is None

    def test_get_entry_by_id(self, service, dictionary):
        created = service.create_entry(
            dictionary_id=dictionary.id, original_text="Word", translated_text="Слово"
        )

        retrieved = service.get_entry(created.id)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.original_text == "Word"

    def test_get_nonexistent_entry(self, service):
        fake_id = uuid4()

        result = service.get_entry(fake_id)

        assert result is None

    def test_get_dictionary_entries(
        self, service, dictionary
    ):  # Create multiple entries
        for i in range(3):
            service.create_entry(
                dictionary_id=dictionary.id,
                original_text=f"Word{i}",
                translated_text=f"Слово{i}",
            )

        entries = service.get_dictionary_entries(dictionary.id)

        assert len(entries) == 3
