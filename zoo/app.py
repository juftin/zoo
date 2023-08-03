"""
zoo app
"""

import logging

import uvicorn
from fastapi import FastAPI

from zoo._version import __application__, __description__, __version__
from zoo.backend.animals import animals_router
from zoo.backend.utils import utils_router
from zoo.config import config
from zoo.db import init_db

if not config.PRODUCTION:
    config.debug_logging()


app = FastAPI(
    title=__application__,
    description=__description__,
    version=__version__,
    debug=False,
    docs_url="/",
)


@app.on_event("startup")
async def on_startup():
    """
    Initialize the database on startup
    """
    await init_db()


app.include_router(utils_router)
app.include_router(animals_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=logging.INFO)  # noqa: S104
