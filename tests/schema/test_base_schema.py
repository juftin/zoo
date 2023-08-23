"""
Test the base schema.
"""

from typing import Any, ClassVar, Dict, Type

import pytest

from zoo.schemas.base import ZooModel


@pytest.fixture
def base_with_example() -> Type[ZooModel]:
    """
    Return a base schema with an example.
    """

    class BaseSchema(ZooModel):
        """
        Base Schema
        """

        name: str
        value: int

        __example__: ClassVar[Dict[str, Any]] = {"name": "An Example", "value": 3}

    return BaseSchema


@pytest.fixture
def base_without_example() -> Type[ZooModel]:
    """
    Return a base schema without an example.
    """

    class BaseSchema(ZooModel):
        """
        Base Schema
        """

        name: str

    return BaseSchema


def test_read_example_with_example(base_with_example: Type[ZooModel]) -> None:
    """
    Test reading example from schema with example.
    """
    assert base_with_example.get_openapi_read_example() == {
        "examples": [
            {
                "name": "An Example",
                "value": 3,
                "id": 1,
                "created_at": "2021-01-01T00:00:00.000000",
                "updated_at": "2021-01-02T09:12:34.567890",
                "deleted_at": None,
            }
        ]
    }


def test_read_example_without_example(base_without_example: Type[ZooModel]) -> None:
    """
    Test reading example from schema without example.
    """
    with pytest.raises(NotImplementedError) as exception:
        base_without_example.get_openapi_read_example()
    assert exception.match("Example not implemented")


def test_create_example_with_example(base_with_example: Type[ZooModel]) -> None:
    """
    Test creating example from schema with example.
    """
    assert base_with_example.get_openapi_create_example() == {
        "examples": [
            {
                "name": "An Example",
                "value": 3,
            }
        ]
    }


def test_create_example_without_example(base_without_example: Type[ZooModel]) -> None:
    """
    Test creating example from schema without example.
    """
    with pytest.raises(NotImplementedError) as exception:
        base_without_example.get_openapi_create_example()
    assert exception.match("Example not implemented")


def test_update_example_with_example(base_with_example: Type[ZooModel]) -> None:
    """
    Test updating example from schema with example.
    """
    assert base_with_example.get_openapi_update_example() == {
        "examples": [
            {
                "name": "An Example",
            }
        ]
    }


def test_update_example_without_example(base_without_example: Type[ZooModel]) -> None:
    """
    Test updating example from schema without example.
    """
    with pytest.raises(NotImplementedError) as exception:
        base_without_example.get_openapi_update_example()
    assert exception.match("Example not implemented")


def test_delete_example_with_example(base_with_example: Type[ZooModel]) -> None:
    """
    Test deleting example from schema with example.
    """
    assert base_with_example.get_openapi_delete_example() == {
        "examples": [
            {
                "name": "An Example",
                "value": 3,
                "id": 1,
                "created_at": "2021-01-01T00:00:00.000000",
                "updated_at": "2021-01-02T09:12:34.567890",
                "deleted_at": "2021-01-02T09:12:34.567890",
            }
        ]
    }
