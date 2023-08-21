"""
Animals Database Model
"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from zoo.models.base import Base, CreatedUpdatedMixin, DeletedAtMixin, IDMixin

if TYPE_CHECKING:
    from zoo.models.exhibits import Exhibits


class Animals(IDMixin, CreatedUpdatedMixin, DeletedAtMixin, Base):
    """
    Animals Database Model
    """

    __tablename__ = "animals"

    name: Mapped[str]
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    species: Mapped[str] = mapped_column(default=None, nullable=True)
    exhibit_id: Mapped[int] = mapped_column(ForeignKey("exhibits.id"), nullable=True, default=None)

    exhibit: Mapped["Exhibits"] = relationship(back_populates="animals")
