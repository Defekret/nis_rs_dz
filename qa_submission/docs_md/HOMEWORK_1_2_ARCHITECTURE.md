# Задание 1-2: Архитектура системы

Personal Dictionary Library

---

## 1. Концепция продукта

**Идея:** Простое приложение для создания персональных словарей.

**MVP функционал:**
- Создание словарей (название, языки)
- Добавление слов с переводом
- Просмотр и управление

---

## 2. DDD Bounded Contexts

### Dictionary Context
**Сущность:** Dictionary
- id, name, description
- source_language, target_language

**Правила:**
- Название обязательно
- При удалении словаря удаляются все записи

### Entry Context
**Сущность:** Entry
- id, dictionary_id
- original_text, translated_text
- usage_example, notes

**Правила:**
- Принадлежит существующему словарю
- Оригинал и перевод обязательны

---

## 3. Архитектура

### Clean Architecture (4 слоя)

**API Layer** - HTTP endpoints
- FastAPI роутеры
- Pydantic схемы

**Service Layer** - бизнес-логика
- DictionaryService
- EntryService

**Domain Layer** - доменные модели
- Dictionary
- Entry

**Infrastructure Layer** - персистентность
- Database (SQLAlchemy)
- Repositories (CRUD)

---

## 4. Компоненты

### API Layer
- DictionaryRouter - 3 эндпоинта
- EntryRouter - 3 эндпоинта

### Service Layer
- DictionaryService
- EntryService

### Infrastructure
- DictionaryRepository
- EntryRepository
- DictionaryORM, EntryORM

### Database
```sql
-- dictionaries
id, name, description, source_language, target_language

-- entries (связь с dictionaries через FK)
id, dictionary_id, original_text, translated_text
```

---

## 5. Data Flow

**Создание словаря:**
```
User → POST /dictionaries/
  → Router → Service → Repository → Database
```

**Получение записей:**
```
User → GET /dictionaries/{id}/entries
  → Router → Service → Repository
  → Convert ORM → Domain → DTO
```

---

## 6. Принципы

- **Separation of Concerns** - каждый слой имеет свою роль
- **Dependency Inversion** - зависимости к центру
- **Clean Architecture** - Domain не зависит от фреймворков
- **DDD** - бизнес-правила в доменных моделях

---

## 7. Путь к микросервисам

При росте можно выделить:
- Dictionary Service
- Entry Service
- Statistics Service
- Learning Service

---

## 8. Диаграммы

См. `qa_submission/diagrams/`
- Container Diagram
- Component Diagram
