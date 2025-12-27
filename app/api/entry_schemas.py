from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class EntryCreate(BaseModel):
    original_text: str = Field(
        ..., min_length=1, description="Оригинальный текст (слово/выражение)"
    )
    translated_text: str = Field(..., min_length=1, description="Перевод")
    usage_example: Optional[str] = Field(None, description="Пример использования")
    notes: Optional[str] = Field(None, description="Личные заметки")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "original_text": "break the ice",
                    "translated_text": "сломать лёд, разрядить обстановку",
                    "usage_example": "He told a joke to break the ice at the meeting.",
                    "notes": "Часто используется в деловом общении",
                }
            ]
        }
    }


class EntryResponse(BaseModel):
    id: UUID
    dictionary_id: UUID
    original_text: str
    translated_text: str
    usage_example: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_domain(cls, entry) -> "EntryResponse":
        return cls(
            id=entry.id,
            dictionary_id=entry.dictionary_id,
            original_text=entry.original_text,
            translated_text=entry.translated_text,
            usage_example=entry.usage_example,
            notes=entry.notes,
            created_at=entry.created_at,
            updated_at=entry.updated_at,
        )


class EntryListResponse(BaseModel):
    entries: list[EntryResponse]
    total: int
