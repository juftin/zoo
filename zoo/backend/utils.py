"""
Utilities APIRouter
"""

import datetime
from typing import Optional, Type

from fastapi import APIRouter, HTTPException

from zoo.models.base import HasDeletedField
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


def check_model(
    model_instance: Optional[HasDeletedField],
    model_class: Type[HasDeletedField],
    id: int,  # noqa: A002
) -> HasDeletedField:
    """
    Handle a missing model

    Parameters
    ----------
    model_instance : Optional[HasDeletedField]
        The model instance to check
    model_class : Type[HasDeletedField]
        The model class to check
    id : int
        The ID of the model instance

    Returns
    -------
    HasDeletedField
        The model instance (if it exists)

    Raises
    ------
    HTTPException
        If the model instance is None or has been deleted
    """
    error_msg = f"Error: `{model_class.__name__}` data not found or deleted - ID: {id}"
    if model_instance is None or model_instance.deleted_at is not None:
        raise HTTPException(status_code=404, detail=error_msg)
    return model_instance
