"""
zoo app
"""

import json
import pathlib

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
app_routers = [
    utils_router,
    animals_router,
]

for router in app_routers:
    app.include_router(router)


@app.on_event("startup")
async def on_startup():
    """
    Initialize the database on startup
    """
    await init_db()


if __name__ == "__main__":
    openapi_body = app.openapi()
    json_file = pathlib.Path(__file__).parent.parent / "docs" / "openapi.json"
    json_file.write_text(json.dumps(openapi_body, indent=2))
    uvicorn.run(app)
