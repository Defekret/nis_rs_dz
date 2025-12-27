import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text

from .database import Base


class DictionaryORM(Base):
    __tablename__ = "dictionaries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<DictionaryORM(id={self.id}, name='{self.name}')>"


class EntryORM(Base):
    __tablename__ = "entries"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    dictionary_id = Column(
        String(36), ForeignKey("dictionaries.id", ondelete="CASCADE"), nullable=False
    )
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    usage_example = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return f"<EntryORM(id={self.id}, original='{self.original_text}')>"
