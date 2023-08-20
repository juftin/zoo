"""
Data(base) Models
"""

from typing import List

from zoo.models.animals import Animals
from zoo.models.exhibits import Exhibits
from zoo.models.staff import Staff
from zoo.models.user import AccessToken, User

__all_models__ = [Animals, Exhibits, Staff, User, AccessToken]

__all__: List[str] = [class_.__name__ for class_ in __all_models__]
