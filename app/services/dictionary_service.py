from typing import Optional
from uuid import UUID

from app.domain import Dictionary
from app.infrastructure.repository import DictionaryRepository


class DictionaryService:
    def __init__(self, repository: DictionaryRepository):
        self.repository = repository

    def create_dictionary(
        self,
        name: str,
        source_language: str,
        target_language: str,
        description: Optional[str] = None,
    ) -> Dictionary:
        dictionary = Dictionary(
            name=name,
            description=description,
            source_language=source_language,
            target_language=target_language,
        )

        created = self.repository.create(dictionary)
        return created

    def get_dictionary(self, dictionary_id: UUID) -> Optional[Dictionary]:
        result = self.repository.get_by_id(dictionary_id)
        return result

    def get_all_dictionaries(self, skip: int = 0, limit: int = 100) -> list[Dictionary]:
        if skip < 0:
            skip = 0
        if limit <= 0:
            limit = 100

        dictionaries = self.repository.get_all(skip=skip, limit=limit)
        return dictionaries

    def update_dictionary(
        self,
        dictionary_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
    ) -> Optional[Dictionary]:
        dictionary = self.repository.get_by_id(dictionary_id)

        if dictionary is None:
            return None

        dictionary.update(
            name=name,
            description=description,
            source_language=source_language,
            target_language=target_language,
        )

        updated = self.repository.update(dictionary)
        return updated

    def delete_dictionary(self, dictionary_id: UUID) -> bool:
        result = self.repository.delete(dictionary_id)
        return result
