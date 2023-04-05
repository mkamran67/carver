from fastapi import FastAPI
from .routers import handler

app = FastAPI()

# Routers
app.include_router(handler.router)
