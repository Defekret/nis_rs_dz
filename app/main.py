from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import dictionary_router
from app.api.entry_routers import router as entry_router
from app.infrastructure import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Dictionary Library",
    description="API для управления персональными словарями",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(dictionary_router)
app.include_router(entry_router)


@app.get("/", tags=["health"])
async def root():
    return {
        "status": "healthy",
        "service": "Personal Dictionary Library",
        "version": "1.0.0",
    }


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "database": "connected", "uptime": "running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
