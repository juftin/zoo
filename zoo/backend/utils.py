"""
Utilities APIRouter
"""

import datetime

from fastapi import APIRouter

from zoo.models.utils import Health

utils_router = APIRouter(tags=["utilities"])


@utils_router.get("/health", response_model=Health)
def health_check() -> Health:
    """
    Check the health of the application
    """
    return Health(
        status="OK",
        code=200,
        timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
    )
