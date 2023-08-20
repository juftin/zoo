"""
zoo app
"""

import argparse
import json
import pathlib
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI

from zoo._version import __application__, __markdown_description__, __version__
from zoo.backend.animals import animals_router
from zoo.backend.exhibits import exhibits_router
from zoo.backend.staff import staff_router
from zoo.backend.utils import utils_router
from zoo.config import config
from zoo.models.user import bootstrap_fastapi_users

if not config.DOCKER:
    config.rich_logging(
        loggers=[
            "uvicorn",
            "uvicorn.access",
        ]
    )


class ZooFastAPI(FastAPI):
    """
    Zoo FastAPI
    """

    def openapi(self) -> Dict[str, Any]:
        """
        OpenAPI
        """
        # if not self.openapi_schema:
        raise ValueError(self.openapi_schema)
        return self.openapi_schema


app = ZooFastAPI(
    title=__application__,
    description=__markdown_description__,
    version=__version__,
    debug=False,
    docs_url=None,  # Custom Swagger UI @ utils_router
    redoc_url=None,
    generate_unique_id_function=config.custom_generate_unique_id,
)
app_routers = [
    utils_router,
    animals_router,
    exhibits_router,
    staff_router,
]

for router in app_routers:
    app.include_router(router)
# FastAPI Users - add routers
bootstrap_fastapi_users(app=app)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--openapi", action="store_true", help="Generate openapi.json", default=False
    )
    args = parser.parse_args()
    if args.openapi is True:
        openapi_body = app.openapi()
        json_file = pathlib.Path(__file__).parent.parent / "docs" / "openapi.json"
        json_file.write_text(json.dumps(openapi_body, indent=2))
    else:
        uvicorn.run(app)
