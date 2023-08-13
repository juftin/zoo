"""
Data(base) Models
"""

from typing import List

from zoo.models.animals import Animals
from zoo.models.exhibits import Exhibits
from zoo.models.staff import Staff

__all_models__ = [
    Animals,
    Exhibits,
    Staff,
]

__all__: List[str] = [class_.__name__ for class_ in __all_models__]
