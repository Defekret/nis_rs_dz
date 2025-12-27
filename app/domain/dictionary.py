from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


class Dictionary:
    def __init__(
        self,
        name: str,
        source_language: str,
        target_language: str,
        description: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.name = self._validate_name(name)
        self.description = description
        self.source_language = self._validate_language(source_language)
        self.target_language = self._validate_language(target_language)
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @staticmethod
    def _validate_name(name: str) -> str:
        if not name or not name.strip():
            raise ValueError("Dictionary name is required")
        return name.strip()

    @staticmethod
    def _validate_language(language: str) -> str:
        if not language or len(language) < 2:
            raise ValueError("Language code must be at least 2 characters")
        return language.lower()

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
    ) -> None:
        if name is not None:
            self.name = self._validate_name(name)
        if description is not None:
            self.description = description
        if source_language is not None:
            self.source_language = self._validate_language(source_language)
        if target_language is not None:
            self.target_language = self._validate_language(target_language)
        self.updated_at = datetime.utcnow()

    def __repr__(self) -> str:
        return f"Dictionary(id={self.id}, name='{self.name}')"
