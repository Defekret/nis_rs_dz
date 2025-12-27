from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.domain import Entry

from .models import EntryORM


class EntryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, entry: Entry) -> Entry:
        db_entry = self._to_orm(entry)
        self.db.add(db_entry)
        self.db.commit()
        self.db.refresh(db_entry)
        return self._to_domain(db_entry)

    def get_by_id(self, entry_id: UUID) -> Optional[Entry]:
        db_entry = self.db.query(EntryORM).filter(EntryORM.id == str(entry_id)).first()

        if db_entry is None:
            return None

        return self._to_domain(db_entry)

    def get_by_dictionary(
        self, dictionary_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Entry]:
        db_entries = (
            self.db.query(EntryORM)
            .filter(EntryORM.dictionary_id == str(dictionary_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return [self._to_domain(db_entry) for db_entry in db_entries]

    @staticmethod
    def _to_domain(orm_model: EntryORM) -> Entry:
        from uuid import UUID

        return Entry(
            id=UUID(orm_model.id) if isinstance(orm_model.id, str) else orm_model.id,  # type: ignore
            dictionary_id=UUID(orm_model.dictionary_id) if isinstance(orm_model.dictionary_id, str) else orm_model.dictionary_id,  # type: ignore
            original_text=orm_model.original_text,  # type: ignore
            translated_text=orm_model.translated_text,  # type: ignore
            usage_example=orm_model.usage_example,  # type: ignore
            notes=orm_model.notes,  # type: ignore
            created_at=orm_model.created_at,  # type: ignore
            updated_at=orm_model.updated_at,  # type: ignore
        )

    @staticmethod
    def _to_orm(domain_model: Entry) -> EntryORM:
        return EntryORM(
            id=str(domain_model.id),
            dictionary_id=str(domain_model.dictionary_id),
            original_text=domain_model.original_text,
            translated_text=domain_model.translated_text,
            usage_example=domain_model.usage_example,
            notes=domain_model.notes,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at,
        )
