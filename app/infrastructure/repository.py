from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.domain import Dictionary

from .models import DictionaryORM


class DictionaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, dictionary: Dictionary) -> Dictionary:
        db_dictionary = self._to_orm(dictionary)
        self.db.add(db_dictionary)
        self.db.commit()
        self.db.refresh(db_dictionary)
        return self._to_domain(db_dictionary)

    def get_by_id(self, dictionary_id: UUID) -> Optional[Dictionary]:
        db_dictionary = (
            self.db.query(DictionaryORM)
            .filter(DictionaryORM.id == str(dictionary_id))
            .first()
        )

        if db_dictionary is None:
            return None

        return self._to_domain(db_dictionary)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Dictionary]:
        db_dictionaries = self.db.query(DictionaryORM).offset(skip).limit(limit).all()
        return [self._to_domain(db_dict) for db_dict in db_dictionaries]

    def update(self, dictionary: Dictionary) -> Dictionary:
        db_dictionary = (
            self.db.query(DictionaryORM)
            .filter(DictionaryORM.id == str(dictionary.id))
            .first()
        )

        if db_dictionary is None:
            raise ValueError(f"Dictionary with id {dictionary.id} not found")

        db_dictionary.name = dictionary.name  # type: ignore
        db_dictionary.description = dictionary.description  # type: ignore
        db_dictionary.source_language = dictionary.source_language  # type: ignore
        db_dictionary.target_language = dictionary.target_language  # type: ignore
        db_dictionary.updated_at = dictionary.updated_at  # type: ignore

        self.db.commit()
        self.db.refresh(db_dictionary)
        return self._to_domain(db_dictionary)

    def delete(self, dictionary_id: UUID) -> bool:
        result = (
            self.db.query(DictionaryORM)
            .filter(DictionaryORM.id == str(dictionary_id))
            .delete()
        )
        self.db.commit()
        return result > 0

    @staticmethod
    def _to_domain(orm_model: DictionaryORM) -> Dictionary:
        from uuid import UUID

        return Dictionary(
            id=UUID(orm_model.id) if isinstance(orm_model.id, str) else orm_model.id,  # type: ignore
            name=orm_model.name,  # type: ignore
            description=orm_model.description,  # type: ignore
            source_language=orm_model.source_language,  # type: ignore
            target_language=orm_model.target_language,  # type: ignore
            created_at=orm_model.created_at,  # type: ignore
            updated_at=orm_model.updated_at,  # type: ignore
        )

    @staticmethod
    def _to_orm(domain_model: Dictionary) -> DictionaryORM:
        return DictionaryORM(
            id=str(domain_model.id),
            name=domain_model.name,
            description=domain_model.description,
            source_language=domain_model.source_language,
            target_language=domain_model.target_language,
            created_at=domain_model.created_at,
            updated_at=domain_model.updated_at,
        )
