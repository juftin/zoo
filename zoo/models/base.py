"""
Base Inheritance Models
"""


from typing import Optional

from sqlmodel import Field, SQLModel


class OptionalIdMixin(SQLModel):
    """
    Id mixin, id is optional

    This is used for create table models
    """

    id: Optional[int] = Field(  # noqa: A003
        default=None, primary_key=True, description="The unique identifier for the table"
    )


class RequiredIdMixin(SQLModel):
    """
    Id mixin with required id
    """

    id: int = Field(primary_key=True, description="The unique identifier for the table")  # noqa: A003
