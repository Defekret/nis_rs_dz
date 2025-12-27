# Personal Dictionary Library

Персональная библиотека словарей для создания и управления собственными тематическими словарями.

## Описание проекта

Personal Dictionary Library - Веб-приложение для создания персональных словарей и изучения языков.

### Основные возможности

- Создание словарей (например, "Английские идиомы")
- Управление записями: слова с переводами и примерами
- Простая статистика по словарям

## Технологии

Python3.9+ • FastAPI • SQLite • SQLAlchemy • Pytest

## Установка и запуск
```bash
pip install -r requirements.txt

# Если нужно установить проект в editable mode (для разработки)
# pip install -e .

# Запуск сервера
uvicorn app.main:app --reload

# Или через python модуль
# python3 -m uvicorn app.main:app --reload
```

В браузере: http://localhost:8000/docs

Запуск тестов:
```bash
# Все тесты
pytest tests/ -v

# С покрытием кода
pytest tests/ --cov=app --cov-report=html

# Allure отчет
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

## Архитектура

Проект следует принципам чистой архитектуры с разделением на слои:

- **API Layer**: FastAPI роутеры и Pydantic модели
- **Service Layer**: Бизнес-логика
- **Domain Layer**: Доменные модели
- **Infrastructure Layer**: Работа с базой данных

## Структура проекта

```
NIS_RS_DZ1_UPD/
├── app/                      # Исходный код
│   ├── api/                  # API endpoints и схемы
│   ├── domain/               # Доменные модели
│   ├── services/             # Бизнес-логика
│   ├── infrastructure/       # База данных и репозитории
│   └── main.py               # Точка входа
├── tests/                    # Тесты
├── qa_submission/            # Документация и отчеты
├── pyproject.toml            # Конфигурация инструментов
├── pytest.ini                # Настройки pytest
└── requirements.txt          # Зависимости
```

## Основные эндпоинты API

### Словари
- `POST /api/v1/dictionaries` - Создать словарь
- `GET /api/v1/dictionaries` - Получить список словарей
- `GET /api/v1/dictionaries/{id}` - Получить словарь по ID
- `PUT /api/v1/dictionaries/{id}` - Обновить словарь
- `DELETE /api/v1/dictionaries/{id}` - Удалить словарь

### Записи
- `POST /api/v1/dictionaries/{id}/entries` - Добавить запись в словарь
- `GET /api/v1/dictionaries/{id}/entries` - Получить записи словаря
- `GET /api/v1/entries/{id}` - Получить запись по ID
- `PUT /api/v1/entries/{id}` - Обновить запись
- `DELETE /api/v1/entries/{id}` - Удалить запись
