from typing import Optional
from uuid import UUID

from app.domain import Entry
from app.infrastructure.entry_repository import EntryRepository


class EntryService:
    def __init__(self, repository: EntryRepository):
        self.repository = repository

    def create_entry(
        self,
        dictionary_id: UUID,
        original_text: str,
        translated_text: str,
        usage_example: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Entry:
        entry = Entry(
            dictionary_id=dictionary_id,
            original_text=original_text,
            translated_text=translated_text,
            usage_example=usage_example,
            notes=notes,
        )

        created = self.repository.create(entry)
        return created

    def get_entry(self, entry_id: UUID) -> Optional[Entry]:
        result = self.repository.get_by_id(entry_id)
        return result

    def get_dictionary_entries(
        self, dictionary_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Entry]:
        if skip < 0:
            skip = 0
        if limit <= 0:
            limit = 100

        entries = self.repository.get_by_dictionary(
            dictionary_id, skip=skip, limit=limit
        )
        return entries
