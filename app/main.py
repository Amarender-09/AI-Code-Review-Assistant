import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.api.webhooks import router as webhook_router
from app.core.config import APP_NAME
from app.core.logging_config import setup_logging


setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title=APP_NAME)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-code-review-assistant-1-887o.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(webhook_router)


@app.get("/")
def home():
    logger.info("Home endpoint called")
    return {
        "message": "AI Code Review Assistant is running"
    }