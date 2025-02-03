# /services/api/app/main.py

from fastapi import FastAPI
from .endpoints import router
import uvicorn

app = FastAPI(
    title="DataHarvester API",
    description="API for managing data harvesting events",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)