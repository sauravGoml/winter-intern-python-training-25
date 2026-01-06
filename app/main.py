from fastapi import FastAPI
from api.v1.router import api_router
from core.config import get_settings


settings = get_settings()


app = FastAPI(title="Personal Assistance API", version="1.0.0")
app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)