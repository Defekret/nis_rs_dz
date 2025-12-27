from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure import DictionaryRepository, get_db
from app.services import DictionaryService

from .schemas import DictionaryCreate, DictionaryListResponse, DictionaryResponse

router = APIRouter(prefix="/api/v1/dictionaries", tags=["dictionaries"])


def get_dictionary_service(db: Session = Depends(get_db)) -> DictionaryService:
    repository = DictionaryRepository(db)
    return DictionaryService(repository)


@router.post(
    "/",
    response_model=DictionaryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать словарь",
    description="Создание нового словаря с указанием названия и языков",
)
async def create_dictionary(
    dictionary_data: DictionaryCreate,
    service: DictionaryService = Depends(get_dictionary_service),
) -> DictionaryResponse:
    try:
        dictionary = service.create_dictionary(
            name=dictionary_data.name,
            description=dictionary_data.description,
            source_language=dictionary_data.source_language,
            target_language=dictionary_data.target_language,
        )
        return DictionaryResponse.from_domain(dictionary)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create dictionary",
        ) from e


@router.get(
    "/{dictionary_id}",
    response_model=DictionaryResponse,
    summary="Получить словарь",
    description="Получение словаря по его ID",
)
async def get_dictionary(
    dictionary_id: UUID, service: DictionaryService = Depends(get_dictionary_service)
) -> DictionaryResponse:
    dictionary = service.get_dictionary(dictionary_id)

    if dictionary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dictionary with id {dictionary_id} not found",
        )

    return DictionaryResponse.from_domain(dictionary)


@router.get(
    "/",
    response_model=DictionaryListResponse,
    summary="Получить список словарей",
    description="Получение списка всех словарей с пагинацией",
)
async def get_dictionaries(
    skip: int = 0,
    limit: int = 100,
    service: DictionaryService = Depends(get_dictionary_service),
) -> DictionaryListResponse:
    dictionaries = service.get_all_dictionaries(skip=skip, limit=limit)

    return DictionaryListResponse(
        dictionaries=[DictionaryResponse.from_domain(d) for d in dictionaries],
        total=len(dictionaries),
    )
