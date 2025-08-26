"""
Animal Tests
"""

import datetime

import pytest
from pydantic import ValidationError

from zoo.schemas.animals import AnimalsBase, AnimalsRead


def test_animal_base_success() -> None:
    """
    AnimalBase - successful validation
    """
    animal = AnimalsBase(name="test", description="test", species="test")
    assert animal.name == "test"
    assert animal.description == "test"
    assert animal.species == "test"


def test_animal_base_failure() -> None:
    """
    AnimalBase - Validation error
    """
    with pytest.raises(ValidationError):
        AnimalsBase()


def test_animal_base_validation() -> None:
    """
    AnimalBase - Validation error
    """
    with pytest.raises(ValidationError):
        AnimalsBase(name="test", description="test", species="test", exhibit_id="test")


def test_animal_read_success() -> None:
    """
    AnimalRead - successful validation
    """
    animal = AnimalsRead(
        name="test",
        description="test",
        species="test",
        id=1,
        exhibit_id=1,
        updated_at=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        created_at=datetime.datetime(2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
    )
    assert animal.name == "test"
    assert animal.description == "test"
    assert animal.species == "test"
    assert animal.exhibit_id == 1
    assert animal.updated_at == datetime.datetime(
        2021, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
    )


def test_animal_read_failure() -> None:
    """
    AnimalRead - Validation error
    """
    with pytest.raises(ValidationError):
        AnimalsRead(name="test", description="test", species="test")
