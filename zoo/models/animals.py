"""
Animal models
"""

from typing import TYPE_CHECKING, Any, ClassVar, Dict, Optional

from sqlalchemy import Table
from sqlalchemy.event import listens_for
from sqlalchemy.future import Connection
from sqlmodel import Field, Relationship

from zoo.models.base import (
    CreatedModifiedMixin,
    DeletedMixin,
    OptionalIdMixin,
    RequiredIdMixin,
    ZooModel,
)

if TYPE_CHECKING:
    from zoo.models.exhibits import Exhibits


class AnimalsBase(ZooModel):
    """
    Animals model base
    """

    name: str = Field(description="The name of the animal", index=True)
    description: Optional[str] = Field(default=None, description="The description of the animal")
    species: Optional[str] = Field(default=None, description="The species of the animal")

    exhibit_id: Optional[int] = Field(
        description="The id of the exhibit", foreign_key="exhibits.id", nullable=True, default=None
    )

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

    class Config:
        """
        Config for AnimalCreate
        """

        schema_extra: ClassVar[Dict[str, Any]] = AnimalsBase.get_openapi_create_example()


class AnimalsRead(
    DeletedMixin,
    CreatedModifiedMixin,
    AnimalsBase,
    RequiredIdMixin,
):
    """
    Animals model: read
    """

    class Config:
        """
        Config for AnimalRead
        """

        schema_extra: ClassVar[Dict[str, Any]] = AnimalsBase.get_openapi_read_example()


class Animals(DeletedMixin, CreatedModifiedMixin, AnimalsBase, OptionalIdMixin, table=True):
    """
    Animals model: database table
    """

    exhibit: "Exhibits" = Relationship(back_populates="animals")


class AnimalsUpdate(ZooModel):
    """
    Animals model: update
    """

    name: Optional[str] = Field(
        default=None, description="The name of the animal", index=True, unique=True
    )
    description: Optional[str] = Field(default=None, description="The description of the animal")
    species: Optional[str] = Field(default=None, description="The species of the animal")
    exhibit_id: Optional[int] = Field(
        description="The id of the exhibit", foreign_key="exhibits.id", nullable=True, default=None
    )

    class Config:
        """
        Config for AnimalUpdate
        """

        schema_extra: ClassVar[Dict[str, Any]] = AnimalsBase.get_openapi_update_example()


@listens_for(Animals.__table__, "after_create")  # type: ignore[attr-defined]
def seed_animals_table(target: Table, connection: Connection, **kwargs) -> None:
    """
    Seed the Animals table with initial data
    """
    animals = [
        AnimalsCreate(
            name="Lion",
            description="Ferocious kitty with mane",
            species="Panthera leo",
            exhibit_id=1,
        ),
        AnimalsCreate(
            name="Tiger",
            description="Ferocious kitty with stripes",
            species="Panthera tigris",
            exhibit_id=1,
        ),
        AnimalsCreate(
            name="Cheetah",
            description="Ferocious fast kitty",
            species="Acinonyx jubatus",
            exhibit_id=1,
        ),
        AnimalsCreate(
            name="Leopard",
            description="Ferocious spotted kitty",
            species="Panthera pardus",
            exhibit_id=1,
        ),
        AnimalsCreate(
            name="Cougar",
            description="Ferocious mountain kitty",
            species="Puma concolor",
            exhibit_id=1,
        ),
    ]
    connection.execute(target.insert(), [animal.dict(exclude_unset=True) for animal in animals])
