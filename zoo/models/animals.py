"""
Animal models
"""

from __future__ import annotations

from typing import Any, ClassVar

from sqlmodel import Field, SQLModel

from zoo.models.base import OptionalIdMixin, RequiredIdMixin

_animal_example = {"name": "Lion", "description": "Ferocious kitty", "species": "Panthera leo"}


class AnimalsBase(SQLModel):
    """
    Animals model base
    """

    name: str = Field(description="The name of the animal")
    description: str | None = Field(default=None, description="The description of the animal")
    species: str | None = Field(default=None, description="The species of the animal")


class AnimalsCreate(AnimalsBase):
    """
    Animals model: create
    """

    class Config:
        """
        Config for AnimalCreate
        """

        schema_extra: ClassVar[dict[str, Any]] = {"examples": [_animal_example]}


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

        schema_extra: ClassVar[dict[str, Any]] = {"examples": [{"id": 1, **_animal_example}]}
