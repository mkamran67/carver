from fastapi import FastAPI
from .routers import handler
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)

# Routers
app.include_router(handler.router)
