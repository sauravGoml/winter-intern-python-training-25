from fastapi import FastAPI
from api.v1.router import api_router
from core.config import get_settings
from core.logging import setup_logging
import logging


from contextlib import asynccontextmanager
from db_manager.session import Base, engine


settings = get_settings()
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    logger.info("starting up application....")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    yield
    logger.info("Shutting down application...")
    # Close engine
    await engine.dispose()


app = FastAPI(title="Personal Assistance API", version="1.0.0", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)