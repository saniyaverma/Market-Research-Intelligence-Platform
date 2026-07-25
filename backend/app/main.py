from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings

import os

app = FastAPI(
    title="ARIP",
    version="0.1.0"
)

app.include_router(router)


@app.get("/")
def health():
    return {
        "status": "running",
        "project": "ARIP"
    }