from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config import PORT
from src.database.db import DBManager
from src.routes.router import router
from src.handlers.exception_handlers import register_exception_handlers
from src.middleware.cors import configure_cors


@asynccontextmanager
async def lifespan(app: FastAPI):
    DBManager.start_mongo()
    await DBManager.config_beanie()
    DBManager.start_redis()

    yield

    await DBManager.close()


def configure_app() -> FastAPI:
    app = FastAPI(
        title="API Projeto Acadêmico",
        lifespan=lifespan
    )

    configure_cors(app)
    register_exception_handlers(app)

    app.include_router(router)

    return app


app = configure_app()


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )