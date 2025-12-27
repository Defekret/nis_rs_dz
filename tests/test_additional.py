from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.dictionary import Dictionary
from app.domain.entry import Entry
from app.infrastructure.database import Base
from app.infrastructure.entry_repository import EntryRepository
from app.infrastructure.repository import DictionaryRepository


class TestDictionaryRepository:
    @pytest.fixture
    def db_session(self):  # Create in-memory database for testing
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        yield session
        session.close()

    def test_create_and_get_dictionary(self, db_session):
        repo = DictionaryRepository(db_session)

        dictionary = Dictionary(
            name="Test Dict", source_language="en", target_language="ru"
        )

        created = repo.create(dictionary)
        assert created.id == dictionary.id

        retrieved = repo.get_by_id(dictionary.id)
        assert retrieved is not None
        assert retrieved.name == "Test Dict"

    def test_get_all_dictionaries(self, db_session):
        repo = DictionaryRepository(db_session)

        dict1 = Dictionary(name="Dict1", source_language="en", target_language="ru")
        dict2 = Dictionary(name="Dict2", source_language="fr", target_language="es")

        repo.create(dict1)
        repo.create(dict2)

        all_dicts = repo.get_all()
        assert len(all_dicts) >= 2

    def test_update_dictionary(self, db_session):
        repo = DictionaryRepository(db_session)

        dictionary = Dictionary(
            name="Original", source_language="en", target_language="ru"
        )
        repo.create(dictionary)

        dictionary.update(name="Updated")
        updated = repo.update(dictionary)

        assert updated.name == "Updated"

    def test_delete_dictionary(self, db_session):
        repo = DictionaryRepository(db_session)

        dictionary = Dictionary(
            name="To Delete", source_language="en", target_language="ru"
        )
        repo.create(dictionary)

        result = repo.delete(dictionary.id)
        assert result is True

        deleted = repo.get_by_id(dictionary.id)
        assert deleted is None

    def test_delete_nonexistent_returns_false(self, db_session):
        repo = DictionaryRepository(db_session)

        result = repo.delete(uuid4())
        assert result is False

    def test_get_all_with_pagination(self, db_session):
        repo = DictionaryRepository(db_session)

        for i in range(5):
            dictionary = Dictionary(
                name=f"Dict{i}", source_language="en", target_language="ru"
            )
            repo.create(dictionary)

        result = repo.get_all(skip=2, limit=2)
        assert len(result) == 2


class TestEntryRepository:
    @pytest.fixture
    def db_session(self):  # Create in-memory database for testing
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(bind=engine)
        session = SessionLocal()
        yield session
        session.close()

    @pytest.fixture
    def sample_dictionary(self, db_session):
        from app.infrastructure.repository import DictionaryRepository

        repo = DictionaryRepository(db_session)

        dictionary = Dictionary(
            name="Test Dict", source_language="en", target_language="ru"
        )
        return repo.create(dictionary)

    def test_create_and_get_entry(self, db_session, sample_dictionary):
        repo = EntryRepository(db_session)

        entry = Entry(
            dictionary_id=sample_dictionary.id,
            original_text="Hello",
            translated_text="Привет",
        )

        created = repo.create(entry)
        assert created.id == entry.id

        retrieved = repo.get_by_id(entry.id)
        assert retrieved is not None
        assert retrieved.original_text == "Hello"

    def test_get_entries_by_dictionary(self, db_session, sample_dictionary):
        repo = EntryRepository(db_session)

        entry1 = Entry(
            dictionary_id=sample_dictionary.id,
            original_text="Hello",
            translated_text="Привет",
        )
        entry2 = Entry(
            dictionary_id=sample_dictionary.id,
            original_text="Goodbye",
            translated_text="Пока",
        )

        repo.create(entry1)
        repo.create(entry2)

        entries = repo.get_by_dictionary(sample_dictionary.id)
        assert len(entries) >= 2

    def test_get_by_id_nonexistent_returns_none(self, db_session):
        repo = EntryRepository(db_session)

        result = repo.get_by_id(uuid4())
        assert result is None

    def test_get_entries_with_pagination(self, db_session, sample_dictionary):
        repo = EntryRepository(db_session)

        for i in range(5):
            entry = Entry(
                dictionary_id=sample_dictionary.id,
                original_text=f"Word{i}",
                translated_text=f"Слово{i}",
            )
            repo.create(entry)

        result = repo.get_by_dictionary(sample_dictionary.id, skip=2, limit=2)
        assert len(result) == 2


class TestSchemas:
    def test_dictionary_create_schema(self):
        from app.api.schemas import DictionaryCreate

        data = DictionaryCreate(
            name="Test",
            source_language="en",
            target_language="ru",
            description="Test desc",
        )

        assert data.name == "Test"
        assert data.source_language == "en"
        assert data.target_language == "ru"
        assert data.description == "Test desc"

    def test_entry_create_schema(self):
        from app.api.entry_schemas import EntryCreate

        data = EntryCreate(
            dictionary_id=uuid4(),
            original_text="Hello",
            translated_text="Привет",
            usage_example="Hello world",
            notes="Test note",
        )

        assert data.original_text == "Hello"
        assert data.translated_text == "Привет"

    def test_dictionary_response_schema(self):
        from datetime import datetime

        from app.api.schemas import DictionaryResponse

        data = DictionaryResponse(
            id=uuid4(),
            name="Test",
            source_language="en",
            target_language="ru",
            description="Test",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert data.name == "Test"

    def test_entry_response_schema(self):
        from datetime import datetime

        from app.api.entry_schemas import EntryResponse

        data = EntryResponse(
            id=uuid4(),
            dictionary_id=uuid4(),
            original_text="Hello",
            translated_text="Привет",
            usage_example="Example",
            notes="Note",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        assert data.original_text == "Hello"


class TestModels:
    def test_dictionary_orm_repr(self):
        from app.infrastructure.models import DictionaryORM

        orm = DictionaryORM(
            id=str(uuid4()),
            name="Test",
            source_language="en",
            target_language="ru",
        )

        repr_str = repr(orm)
        assert "DictionaryORM" in repr_str
        assert "Test" in repr_str

    def test_entry_orm_repr(self):
        from app.infrastructure.models import EntryORM

        orm = EntryORM(
            id=str(uuid4()),
            dictionary_id=str(uuid4()),
            original_text="Hello",
            translated_text="Привет",
        )

        repr_str = repr(orm)
        assert "EntryORM" in repr_str
        assert "Hello" in repr_str
