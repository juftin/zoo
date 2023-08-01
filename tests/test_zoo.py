"""
Zoo tests
"""

import pytest
from pydantic import ValidationError

from zoo.models.animals import AnimalsBase


def test_animal_base_success():
    """
    AnimalBase - successful validation
    """
    animal = AnimalsBase(name="test", description="test", species="test")
    assert animal.name == "test"
    assert animal.description == "test"
    assert animal.species == "test"


def test_animal_base_failure():
    """
    AnimalBase - Validation error
    """
    with pytest.raises(ValidationError):
        AnimalsBase()
