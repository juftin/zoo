"""
Exhibits models
"""

from typing import Any, ClassVar, Dict, Optional

from pydantic import ConfigDict, Field

from zoo.schemas.base import (
    CreatedModifiedMixin,
    DeletedMixin,
    RequiredIdMixin,
    ZooModel,
)


class ExhibitsBase(ZooModel):
    """
    Exhibits model base
    """

    name: str = Field(description="The name of the exhibit")
    description: Optional[str] = Field(default=None, description="The description of the exhibit")
    location: Optional[str] = Field(default=None, description="The location of the exhibit")

    __example__: ClassVar[Dict[str, Any]] = {
        "name": "Big Cat Exhibit",
        "description": "A big cat exhibit",
        "location": "North America",
    }


class ExhibitsCreate(ExhibitsBase):
    """
    Exhibits model: create
    """

    model_config = ConfigDict(json_schema_extra=ExhibitsBase.get_openapi_create_example())


class ExhibitsRead(
    DeletedMixin,
    CreatedModifiedMixin,
    ExhibitsBase,
    RequiredIdMixin,
):
    """
    Exhibits model: read
    """

    model_config = ConfigDict(
        from_attributes=True, json_schema_extra=ExhibitsBase.get_openapi_read_example()
    )


class ExhibitsUpdate(ZooModel):
    """
    Exhibits model: update
    """

    name: Optional[str] = Field(default=None, description="The name of the exhibit")
    description: Optional[str] = Field(default=None, description="The description of the exhibit")
    location: Optional[str] = Field(default=None, description="The location of the exhibit")

    model_config = ConfigDict(json_schema_extra=ExhibitsBase.get_openapi_update_example())
