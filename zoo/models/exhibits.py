"""
Exhibits Database Model
"""

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from zoo.models.base import Base, CreatedUpdatedMixin, DeletedAtMixin, IDMixin

if TYPE_CHECKING:  # pragma: no cover
    from zoo.models.animals import Animals
    from zoo.models.staff import Staff


class Exhibits(IDMixin, CreatedUpdatedMixin, DeletedAtMixin, Base):
    """
    Exhibits Database Model
    """

    __tablename__ = "exhibits"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    location: Mapped[str] = mapped_column(default=None, nullable=True)

    animals: Mapped[List["Animals"]] = relationship(back_populates="exhibit")
    staff: Mapped[List["Staff"]] = relationship(back_populates="exhibit")
