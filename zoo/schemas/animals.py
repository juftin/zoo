"""
Animal models
"""

from typing import Any, ClassVar, Dict, Optional

from pydantic import ConfigDict, Field

from zoo.schemas.base import (
    CreatedModifiedMixin,
    DeletedMixin,
    RequiredIdMixin,
    ZooModel,
)


class AnimalsBase(ZooModel):
    """
    Animals model base
    """

    name: str = Field(description="The name of the animal")
    description: Optional[str] = Field(default=None, description="The description of the animal")
    species: Optional[str] = Field(default=None, description="The species of the animal")

    exhibit_id: Optional[int] = Field(description="The id of the exhibit", default=None)

    __example__: ClassVar[Dict[str, Any]] = {
        "name": "Lion",
        "description": "Ferocious kitty",
        "species": "Panthera leo",
        "exhibit_id": 1,
    }


class AnimalsCreate(AnimalsBase):
    """
    Animals model: create
    """

    model_config = ConfigDict(json_schema_extra=AnimalsBase.get_openapi_create_example())


class AnimalsRead(
    DeletedMixin,
    CreatedModifiedMixin,
    AnimalsBase,
    RequiredIdMixin,
):
    """
    Animals model: read
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=AnimalsBase.get_openapi_read_example(),
    )


class AnimalsUpdate(ZooModel):
    """
    Animals model: update
    """

    name: Optional[str] = Field(default=None, description="The name of the animal")
    description: Optional[str] = Field(default=None, description="The description of the animal")
    species: Optional[str] = Field(default=None, description="The species of the animal")
    exhibit_id: Optional[int] = Field(description="The id of the exhibit", default=None)

    model_config = ConfigDict(json_schema_extra=AnimalsBase.get_openapi_update_example())
