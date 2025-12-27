from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Entry:
    def __init__(
        self,
        dictionary_id: UUID,
        original_text: str,
        translated_text: str,
        usage_example: Optional[str] = None,
        notes: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.dictionary_id = dictionary_id
        self.original_text = self._validate_text(original_text, "Original text")
        self.translated_text = self._validate_text(translated_text, "Translated text")
        self.usage_example = usage_example
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @staticmethod
    def _validate_text(text: str, field_name: str) -> str:
        if not text or not text.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return text.strip()

    def __repr__(self) -> str:
        return f"Entry(id={self.id}, original='{self.original_text}')"
