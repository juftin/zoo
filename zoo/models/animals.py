"""
Animal models
"""

from typing import Any, ClassVar, Dict, Optional

from sqlalchemy import Table
from sqlalchemy.future import Connection
from sqlmodel import Field, SQLModel

from zoo.models.base import CreatedModifiedMixin, OptionalIdMixin, RequiredIdMixin

_animal_example = {
    "name": "Lion",
    "description": "Ferocious kitty",
    "species": "Panthera leo",
    "created": "2021-01-01T00:00:00.000000",
    "modified": "2021-01-02T09:12:34.567890",
}


class AnimalsBase(SQLModel):
    """
    Animals model base
    """

    name: str = Field(description="The name of the animal")
    description: Optional[str] = Field(default=None, description="The description of the animal")
    species: Optional[str] = Field(default=None, description="The species of the animal")


class AnimalsCreate(AnimalsBase):
    """
    Animals model: create
    """

    class Config:
        """
        Config for AnimalCreate
        """

        schema_extra: ClassVar[Dict[str, Any]] = {"examples": [_animal_example]}


class AnimalsRead(AnimalsBase, RequiredIdMixin, CreatedModifiedMixin):
    """
    Animals model: read
    """

    class Config:
        """
        Config for AnimalRead
        """

        schema_extra: ClassVar[Dict[str, Any]] = {"examples": [{"id": 1, **_animal_example}]}


class Animals(AnimalsBase, CreatedModifiedMixin, OptionalIdMixin, table=True):
    """
    Animals model: database table
    """

    @classmethod
    def create_seed_data(cls, target: Table, connection: Connection) -> None:
        """
        Seed the Animals table with initial data
        """
        animals = [
            AnimalsCreate(name="Lion", description="Ferocious kitty with mane", species="Panthera leo"),
            AnimalsCreate(name="Tiger", description="Ferocious kitty with stripes", species="Panthera tigris"),
            AnimalsCreate(name="Bear", description="Ferocious doggy kinda thing", species="Ursus arctos"),
            AnimalsCreate(name="Wolf", description="Ferocious doggy", species="Canis lupus"),
            AnimalsCreate(name="Cheetah", description="Ferocious fast kitty", species="Acinonyx jubatus"),
            AnimalsCreate(name="Leopard", description="Ferocious spotted kitty", species="Panthera pardus"),
            AnimalsCreate(name="Cougar", description="Ferocious mountain kitty", species="Puma concolor"),
        ]
        connection.execute(target.insert(), [animal.dict() for animal in animals])
        connection.commit()


class AnimalsUpdate(SQLModel):
    """
    Animals model: update
    """

    name: Optional[str] = Field(default=None, description="The name of the animal")
    description: Optional[str] = Field(default=None, description="The description of the animal")
    species: Optional[str] = Field(default=None, description="The species of the animal")

    class Config:
        """
        Config for AnimalUpdate
        """

        schema_extra: ClassVar[Dict[str, Any]] = {"examples": [{"description": "Ferocious kitty with a mane"}]}
