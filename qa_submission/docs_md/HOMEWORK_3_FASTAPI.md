# Задание 3: Практика с FastAPI

---

## 1. Эндпоинты

### Dictionary Endpoints
- `POST /api/v1/dictionaries/` - создать словарь
- `GET /api/v1/dictionaries/{id}` - получить словарь
- `GET /api/v1/dictionaries/` - список словарей

### Entry Endpoints
- `POST /api/v1/entries/` - создать запись
- `GET /api/v1/entries/{id}` - получить запись
- `GET /api/v1/dictionaries/{id}/entries` - записи словаря

### Health
- `GET /` - root
- `GET /health` - health check

**Всего: 8 эндпоинтов**

---

## 2. Разделение по слоям

### API Layer
```
routers.py - FastAPI endpoints
schemas.py - Pydantic validation
entry_routers.py - Entry endpoints
entry_schemas.py - Entry schemas
```

### Service Layer
```
dictionary_service.py - бизнес-логика
entry_service.py - Entry логика
```

### Domain Layer
```
dictionary.py - Dictionary модель
entry.py - Entry модель
```

### Infrastructure Layer
```
database.py - DB config
models.py - ORM модели
repository.py - Dictionary CRUD
entry_repository.py - Entry CRUD
```

---

## 3. Конвертация моделей

**API → Domain:**
```python
DictionaryCreate(...) → Dictionary(...)
```

**Domain → ORM:**
```python
Dictionary(...) → DictionaryORM(...)
```

**Domain → API:**
```python
Dictionary(...) → DictionaryResponse.from_domain(...)
```

**Методы:**
- `_to_domain()` - ORM → Domain
- `_to_orm()` - Domain → ORM
- `.from_domain()` - Domain → DTO

---

## 4. Unit-тесты

### Domain Tests
- test_domain.py - 9 тестов для Dictionary
- test_entry_domain.py - 9 тестов для Entry

### API Tests
- test_api.py - 7 интеграционных тестов

### Repository Tests
- test_additional.py - 16 тестов

### Service Tests
- test_service_methods.py - 9 тестов

**Всего: 52 теста**

---

## 5. Observability

### Логирование
- API Layer - запросы/ответы
- Service Layer - бизнес-события
- Infrastructure - SQL запросы

### Метрики
- Количество словарей (counter)
- Время запросов (histogram)
- Количество ошибок (counter)

### Трейсинг
- HTTP endpoints - root span
- Service calls - child spans
- DB queries - database spans

---

## Технологии

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Pytest

---

## Запуск
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**API:** http://localhost:8000/docs

---

## Структура
```
app/
├── api/              # Endpoints + Schemas
├── domain/           # Business models
├── services/         # Business logic
├── infrastructure/   # DB + Repositories
└── main.py

tests/
├── test_domain.py
├── test_api.py
└── test_additional.py
```

---

## Принципы

✅ Clean Architecture
✅ DDD
✅ Dependency Injection
✅ Repository Pattern
✅ API Best Practices
