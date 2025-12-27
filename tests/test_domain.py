from datetime import datetime
from uuid import UUID

import pytest

from app.domain import Dictionary


class TestDictionary:
    def test_create_dictionary_with_valid_data(self):
        dictionary = Dictionary(
            name="English Idioms",
            description="Collection of English idioms",
            source_language="en",
            target_language="ru",
        )

        assert dictionary.name == "English Idioms"
        assert dictionary.description == "Collection of English idioms"
        assert dictionary.source_language == "en"
        assert dictionary.target_language == "ru"
        assert isinstance(dictionary.id, UUID)
        assert isinstance(dictionary.created_at, datetime)
        assert isinstance(dictionary.updated_at, datetime)

    def test_create_dictionary_with_empty_name_raises_error(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Dictionary(name="", source_language="en", target_language="ru")

    def test_create_dictionary_with_whitespace_name_raises_error(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Dictionary(name="   ", source_language="en", target_language="ru")

    def test_create_dictionary_with_invalid_language_raises_error(self):
        with pytest.raises(
            ValueError, match="Language code must be at least 2 characters"
        ):
            Dictionary(
                name="Test Dictionary",
                source_language="e",
                target_language="ru",
            )

    def test_name_is_trimmed(self):
        dictionary = Dictionary(
            name="  English Idioms  ", source_language="en", target_language="ru"
        )

        assert dictionary.name == "English Idioms"

    def test_language_codes_are_lowercase(self):
        dictionary = Dictionary(name="Test", source_language="EN", target_language="RU")

        assert dictionary.source_language == "en"
        assert dictionary.target_language == "ru"

    def test_update_dictionary(self):
        dictionary = Dictionary(
            name="Old Name", source_language="en", target_language="ru"
        )
        old_updated_at = dictionary.updated_at

        dictionary.update(name="New Name", description="New Description")

        assert dictionary.name == "New Name"
        assert dictionary.description == "New Description"
        assert dictionary.updated_at > old_updated_at

    def test_update_with_empty_name_raises_error(self):
        dictionary = Dictionary(name="Test", source_language="en", target_language="ru")

        with pytest.raises(ValueError, match="name cannot be empty"):
            dictionary.update(name="")

    def test_repr(self):
        dictionary = Dictionary(
            name="Test Dictionary", source_language="en", target_language="ru"
        )

        repr_str = repr(dictionary)
        assert "Dictionary" in repr_str
        assert "Test Dictionary" in repr_str
        assert str(dictionary.id) in repr_str
