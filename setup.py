from setuptools import find_packages, setup

setup(
    name="personal-dictionary-library",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlalchemy==2.0.23",
        "pydantic==2.5.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-asyncio==0.21.1",
            "pytest-cov==4.1.0",
            "allure-pytest==2.13.2",
            "httpx==0.25.1",
            "ruff==0.1.6",
            "black==23.11.0",
            "isort==5.12.0",
            "mypy==1.7.1",
            "pre-commit==3.5.0",
        ]
    },
    python_requires=">=3.9",
)
