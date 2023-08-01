"""
zoo app
"""

from __future__ import annotations

from fastapi import FastAPI

from zoo import __version__
from zoo.application.animals import animals_router
from zoo.application.utils import utils_router
from zoo.db import init_db

app = FastAPI(
    title="zoo",
    description="An asynchronous zoo API, powered by FastAPI and SQLModel",
    version=__version__,
    debug=True,
)


@app.on_event("startup")
async def on_startup():
    """
    Initialize the database on startup
    """
    await init_db()


app.include_router(utils_router)
app.include_router(animals_router)
