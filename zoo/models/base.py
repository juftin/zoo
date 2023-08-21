"""
SQLAlchemy Base Model
"""

import datetime
from typing import TypeVar

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    SQLAlchemy Base Model
    """


class IDMixin:
    """
    ID Mixin
    """

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003


class CreatedAtMixin:
    """
    Created Updated Mixin
    """

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UpdatedAtMixin:
    """
    Created Updated Mixin
    """

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CreatedUpdatedMixin(CreatedAtMixin, UpdatedAtMixin):
    """
    Created Updated Mixin
    """


class DeletedAtMixin:
    """
    Deleted At Mixin
    """

    deleted_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=None, nullable=True
    )


DatabaseType = TypeVar("DatabaseType", bound=Base)
DatabaseTypeDeletedAt = TypeVar("DatabaseTypeDeletedAt", bound=DeletedAtMixin)
