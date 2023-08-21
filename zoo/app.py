"""
zoo app
"""

import uvicorn
from fastapi import FastAPI

from zoo._version import __application__, __markdown_description__, __version__
from zoo.api.animals import animals_router
from zoo.api.exhibits import exhibits_router
from zoo.api.staff import staff_router
from zoo.api.utils import utils_router
from zoo.config import app_config
from zoo.models.users import bootstrap_fastapi_users

if not app_config.DOCKER:
    app_config.rich_logging(
        loggers=[
            "uvicorn",
            "uvicorn.access",
        ]
    )


class ZooFastAPI(FastAPI):
    """
    Zoo FastAPI
    """


app = ZooFastAPI(
    title=__application__,
    description=__markdown_description__,
    version=__version__,
    debug=False,
    docs_url=None,  # Custom Swagger UI @ utils_router
    redoc_url=None,
    generate_unique_id_function=app_config.custom_generate_unique_id,
)
# Routers
app_routers = [
    utils_router,
    animals_router,
    exhibits_router,
    staff_router,
]
for router in app_routers:
    app.include_router(router)
# FastAPI Users Setup
bootstrap_fastapi_users(app=app)


if __name__ == "__main__":
    uvicorn.run(app)
