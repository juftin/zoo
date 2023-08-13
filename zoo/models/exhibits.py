"""
Exhibits models
"""

from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional

from sqlmodel import Field, Relationship

from zoo.models.base import (
    CreatedModifiedMixin,
    DeletedMixin,
    OptionalIdMixin,
    RequiredIdMixin,
    ZooModel,
)

if TYPE_CHECKING:
    from zoo.models.animals import Animals
    from zoo.models.staff import Staff


class ExhibitsBase(ZooModel):
    """
    Exhibits model base
    """

    name: str = Field(description="The name of the exhibit", index=True, unique=True)
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

    class Config:
        """
        Config for ExhibitCreate
        """

        schema_extra: ClassVar[Dict[str, Any]] = ExhibitsBase.get_openapi_create_example()


class ExhibitsRead(
    DeletedMixin,
    CreatedModifiedMixin,
    ExhibitsBase,
    RequiredIdMixin,
):
    """
    Exhibits model: read
    """

    class Config:
        """
        Config for ExhibitRead
        """

        schema_extra: ClassVar[Dict[str, Any]] = ExhibitsBase.get_openapi_read_example()


class Exhibits(
    DeletedMixin,
    CreatedModifiedMixin,
    ExhibitsBase,
    OptionalIdMixin,
    table=True,
):
    """
    Exhibits model: table
    """

    animals: List["Animals"] = Relationship(back_populates="exhibit")
    staff: List["Staff"] = Relationship(back_populates="exhibit")


class ExhibitsUpdate(ZooModel):
    """
    Exhibits model: update
    """

    name: Optional[str] = Field(default=None, description="The name of the exhibit", index=True)
    description: Optional[str] = Field(default=None, description="The description of the exhibit")
    location: Optional[str] = Field(default=None, description="The location of the exhibit")

    class Config:
        """
        Config for ExhibitUpdate
        """

        schema_extra: ClassVar[Dict[str, Any]] = ExhibitsBase.get_openapi_update_example()
