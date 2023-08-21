"""
FastAPI Users
"""

import logging
import uuid

from fastapi_users import schemas

from zoo.schemas.base import CreatedModifiedMixin

logger = logging.getLogger(__name__)


class UserRead(schemas.BaseUser[uuid.UUID], CreatedModifiedMixin):
    """
    FastAPI Users - User Read Model
    """


class UserCreate(schemas.BaseUserCreate):
    """
    FastAPI Users - User Create Model
    """


class UserUpdate(schemas.BaseUserUpdate):
    """
    FastAPI Users - User Update Model
    """
