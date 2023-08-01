"""
zoo app
"""

from fastapi import FastAPI

from zoo._version import __application__, __description__, __version__
from zoo.application.animals import animals_router
from zoo.application.utils import utils_router
from zoo.db import init_db

app = FastAPI(
    title=__application__,
    description=__description__,
    version=__version__,
    debug=True,
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
