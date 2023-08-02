"""
Animal models
"""

from typing import Any, ClassVar, Dict, Optional

from sqlmodel import Field, SQLModel

from zoo.models.base import OptionalIdMixin, RequiredIdMixin

_animal_example = {"name": "Lion", "description": "Ferocious kitty", "species": "Panthera leo"}


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


class Animals(OptionalIdMixin, AnimalsBase, table=True):
    """
    Animals model: database table
    """


class AnimalsRead(RequiredIdMixin, AnimalsBase):
    """
    Animals model: read
    """

    class Config:
        """
        Config for AnimalRead
        """

        schema_extra: ClassVar[Dict[str, Any]] = {"examples": [{"id": 1, **_animal_example}]}


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
