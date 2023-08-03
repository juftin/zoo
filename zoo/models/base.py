"""
Base Inheritance Models
"""

import datetime
from typing import Optional

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel, func


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


class CreatedModifiedMixin(SQLModel):
    """
    Created and modified mixin
    """

    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        description="The date and time the record was created",
        sa_column=Column(DateTime(timezone=True), server_default=func.CURRENT_TIMESTAMP()),
    )
    modified_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
        nullable=False,
        description="The date and time the record was last modified",
        sa_column=Column(
            DateTime(timezone=True), server_default=func.CURRENT_TIMESTAMP(), onupdate=func.CURRENT_TIMESTAMP()
        ),
    )


class DeletedMixin(SQLModel):
    """
    Deleted mixin
    """

    deleted_at: Optional[datetime.datetime] = Field(
        default=None,
        nullable=True,
        description="The date and time the record was deleted",
        sa_column=Column(DateTime(timezone=True), default=None, nullable=True),
    )
