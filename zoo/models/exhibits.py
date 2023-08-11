"""
Exhibits models
"""

from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional

from sqlalchemy import Table
from sqlalchemy.event import listens_for
from sqlalchemy.future import Connection
from sqlmodel import Field

from zoo.models.base import (
    CreatedModifiedMixin,
    DeletedMixin,
    OptionalIdMixin,
    RequiredIdMixin,
    ZooModel,
)

if TYPE_CHECKING:
    pass


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
        "animal_id": 1,
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


@listens_for(Exhibits.__table__, "after_create")  # type: ignore[attr-defined]
def seed_exhibits_table(target: Table, connection: Connection, **kwargs) -> None:  # noqa: ARG001
    """
    Seed the Animals table with initial data
    """
    exhibits = [
        Exhibits(name="Big Cat Exhibit", description="A big cat exhibit", location="North America"),
        Exhibits(name="Bird Exhibit", description="A bird exhibit", location="North America"),
        Exhibits(name="Reptile Exhibit", description="A reptile exhibit", location="North America"),
        Exhibits(
            name="Aquatic Exhibit", description="An aquatic exhibit", location="North America"
        ),
    ]
    connection.execute(target.insert(), [exhibit.dict() for exhibit in exhibits])
