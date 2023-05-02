from fastapi import FastAPI
from .routers import handler
import logging
import uvicorn

app = FastAPI()

logging.basicConfig(level=logging.INFO)

# Routers
app.include_router(handler.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4333, log_level="info")
