# QA Setup

Инструкция по запуску QA инструментов.

---

## Установка
```bash
pip install -r requirements.txt
```

---

## Pytest + Allure
```bash
# Запуск тестов
pytest tests/ -v

# Генерация Allure отчёта
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

---

## Coverage
```bash
# Запуск с покрытием
pytest tests/ --cov=app --cov-report=html

# Открыть отчёт
open htmlcov/index.html
```

---

## Линтеры
```bash
# Проверка
ruff check app/ tests/
black --check app/ tests/

# Автофикс
ruff check app/ tests/ --fix
black app/ tests/
```

---

## Pre-commit
```bash
# Установка
pre-commit install

# Проверка
pre-commit run --all-files
```

---

## Mypy
```bash
mypy app/
```

---

## Всё одной командой
```bash
pytest tests/ -v --cov=app && ruff check app/ tests/ && black --check app/ tests/ && mypy app/
```
