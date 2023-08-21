"""
Base Inheritance Models
"""

import datetime
from typing import Any, ClassVar, Dict, Optional, TypeVar

from pydantic import BaseModel, Field


class ZooModel(BaseModel):
    """
    Base model for all zoo models
    """

    __example__: ClassVar[Dict[str, Any]] = {}

    __openapi_db_fields__: ClassVar[Dict[str, Any]] = {
        "id": 1,
        "created_at": "2021-01-01T00:00:00.000000",
        "modified_at": "2021-01-02T09:12:34.567890",
        "deleted_at": None,
    }

    @classmethod
    def get_openapi_read_example(cls) -> Dict[str, Any]:
        """
        Get the openapi read example
        """
        if not cls.__example__:
            error_msg = "Example not implemented"
            raise NotImplementedError(error_msg)
        return {
            "examples": [
                {
                    **cls.__example__,
                    **cls.__openapi_db_fields__,
                }
            ]
        }

    @classmethod
    def get_openapi_create_example(cls) -> Dict[str, Any]:
        """
        Get the openapi create example
        """
        if not cls.__example__:
            error_msg = "Example not implemented"
            raise NotImplementedError(error_msg)
        return {"examples": [cls.__example__]}

    @classmethod
    def get_openapi_update_example(cls) -> Dict[str, Any]:
        """
        Get the openapi update example
        """
        if not cls.__example__:
            error_msg = "Example not implemented"
            raise NotImplementedError(error_msg)
        half_example_keys = list(cls.__example__.keys())[: len(cls.__example__) // 2]
        half_example = {key: cls.__example__[key] for key in half_example_keys}
        return {"examples": [half_example]}

    @classmethod
    def get_openapi_delete_example(cls) -> Dict[str, Any]:
        """
        Get the openapi delete example
        """
        read_example = cls.get_openapi_read_example()
        read_example["deleted_at"] = "2021-01-02T09:12:34.567890"
        return read_example


class OptionalIdMixin(ZooModel):
    """
    Id mixin, id is optional

    This is used for create table models
    """

    id: Optional[int] = Field(  # noqa: A003
        default=None, description="The unique identifier for the table"
    )


class RequiredIdMixin(ZooModel):
    """
    Id mixin with required id
    """

    id: int = Field(description="The unique identifier for the table")  # noqa: A003


class CreatedModifiedMixin(ZooModel):
    """
    Created and modified mixin
    """

    created_at: datetime.datetime = Field(
        description="The date and time the record was created",
    )
    updated_at: datetime.datetime = Field(
        description="The date and time the record was last modified",
    )


class DeletedMixin(ZooModel):
    """
    Deleted mixin
    """

    deleted_at: Optional[datetime.datetime] = Field(
        default=None,
        description="The date and time the record was deleted",
    )


ZooModelType = TypeVar("ZooModelType", bound=ZooModel)
HasDeletedField = TypeVar("HasDeletedField", bound=DeletedMixin)
