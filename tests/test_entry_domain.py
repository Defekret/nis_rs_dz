from datetime import datetime
from uuid import uuid4

import pytest

from app.domain.entry import Entry


class TestEntry:
    def test_create_entry_with_valid_data(self):
        dictionary_id = uuid4()
        entry = Entry(
            dictionary_id=dictionary_id,
            original_text="Hello",
            translated_text="Привет",
            usage_example="Hello, world!",
            notes="Common greeting",
        )

        assert entry.dictionary_id == dictionary_id
        assert entry.original_text == "Hello"
        assert entry.translated_text == "Привет"
        assert entry.usage_example == "Hello, world!"
        assert entry.notes == "Common greeting"
        assert isinstance(entry.id, type(uuid4()))
        assert isinstance(entry.created_at, datetime)
        assert isinstance(entry.updated_at, datetime)

    def test_create_entry_without_optional_fields(self):
        dictionary_id = uuid4()
        entry = Entry(
            dictionary_id=dictionary_id, original_text="Test", translated_text="Тест"
        )

        assert entry.original_text == "Test"
        assert entry.translated_text == "Тест"
        assert entry.usage_example is None
        assert entry.notes is None

    def test_create_entry_with_empty_original_text_raises_error(self):
        with pytest.raises(ValueError, match="Original text cannot be empty"):
            Entry(dictionary_id=uuid4(), original_text="", translated_text="Test")

    def test_create_entry_with_whitespace_original_text_raises_error(self):
        with pytest.raises(ValueError, match="Original text cannot be empty"):
            Entry(dictionary_id=uuid4(), original_text="   ", translated_text="Test")

    def test_create_entry_with_empty_translated_text_raises_error(self):
        with pytest.raises(ValueError, match="Translated text cannot be empty"):
            Entry(dictionary_id=uuid4(), original_text="Test", translated_text="")

    def test_create_entry_with_whitespace_translated_text_raises_error(self):
        with pytest.raises(ValueError, match="Translated text cannot be empty"):
            Entry(dictionary_id=uuid4(), original_text="Test", translated_text="   ")

    def test_original_text_is_trimmed(self):
        entry = Entry(
            dictionary_id=uuid4(), original_text="  Hello  ", translated_text="Привет"
        )

        assert entry.original_text == "Hello"

    def test_translated_text_is_trimmed(self):
        entry = Entry(
            dictionary_id=uuid4(), original_text="Hello", translated_text="  Привет  "
        )

        assert entry.translated_text == "Привет"

    def test_repr(self):
        dictionary_id = uuid4()
        entry = Entry(
            dictionary_id=dictionary_id, original_text="Hello", translated_text="Привет"
        )

        repr_str = repr(entry)
        assert "Entry" in repr_str
        assert "Hello" in repr_str
