from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure import get_db
from app.infrastructure.entry_repository import EntryRepository
from app.services.entry_service import EntryService

from .entry_schemas import EntryCreate, EntryListResponse, EntryResponse

router = APIRouter(prefix="/api/v1", tags=["entries"])


def get_entry_service(db: Session = Depends(get_db)) -> EntryService:
    repository = EntryRepository(db)
    return EntryService(repository)


@router.post(
    "/dictionaries/{dictionary_id}/entries",
    response_model=EntryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить запись в словарь",
    description="Создание новой записи (слова/выражения) в указанном словаре",
)
async def create_entry(
    dictionary_id: UUID,
    entry_data: EntryCreate,
    service: EntryService = Depends(get_entry_service),
) -> EntryResponse:
    try:
        entry = service.create_entry(
            dictionary_id=dictionary_id,
            original_text=entry_data.original_text,
            translated_text=entry_data.translated_text,
            usage_example=entry_data.usage_example,
            notes=entry_data.notes,
        )
        return EntryResponse.from_domain(entry)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/dictionaries/{dictionary_id}/entries",
    response_model=EntryListResponse,
    summary="Получить записи словаря",
    description="Получение всех записей указанного словаря",
)
async def get_dictionary_entries(
    dictionary_id: UUID,
    skip: int = 0,
    limit: int = 100,
    service: EntryService = Depends(get_entry_service),
) -> EntryListResponse:
    entries = service.get_dictionary_entries(dictionary_id, skip=skip, limit=limit)

    return EntryListResponse(
        entries=[EntryResponse.from_domain(e) for e in entries], total=len(entries)
    )


@router.get(
    "/entries/{entry_id}",
    response_model=EntryResponse,
    summary="Получить запись",
    description="Получение записи по её ID",
)
async def get_entry(
    entry_id: UUID, service: EntryService = Depends(get_entry_service)
) -> EntryResponse:
    entry = service.get_entry(entry_id)

    if entry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry with id {entry_id} not found",
        )

    return EntryResponse.from_domain(entry)
