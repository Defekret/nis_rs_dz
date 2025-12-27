from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DictionaryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Название словаря")
    description: Optional[str] = Field(
        None, max_length=1000, description="Описание словаря"
    )
    source_language: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="Язык оригинала (например, 'en', 'ru')",
    )
    target_language: str = Field(
        ...,
        min_length=2,
        max_length=10,
        description="Язык перевода (например, 'ru', 'en')",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Английские идиомы",
                    "description": "Коллекция популярных английских идиом",
                    "source_language": "en",
                    "target_language": "ru",
                }
            ]
        }
    }


class DictionaryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    source_language: Optional[str] = Field(None, min_length=2, max_length=10)
    target_language: Optional[str] = Field(None, min_length=2, max_length=10)


class DictionaryResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    source_language: str
    target_language: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,  # Позволяет создавать из объектов (не только dict)
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Английские идиомы",
                    "description": "Коллекция популярных английских идиом",
                    "source_language": "en",
                    "target_language": "ru",
                    "created_at": "2024-01-01T12:00:00",
                    "updated_at": "2024-01-01T12:00:00",
                }
            ]
        },
    }

    @classmethod
    def from_domain(cls, dictionary) -> "DictionaryResponse":
        return cls(
            id=dictionary.id,
            name=dictionary.name,
            description=dictionary.description,
            source_language=dictionary.source_language,
            target_language=dictionary.target_language,
            created_at=dictionary.created_at,
            updated_at=dictionary.updated_at,
        )


class DictionaryListResponse(BaseModel):
    dictionaries: list[DictionaryResponse]
    total: int
