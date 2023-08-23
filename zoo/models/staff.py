"""
Staff Database Model
"""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from zoo.models.base import Base, CreatedUpdatedMixin, DeletedAtMixin, IDMixin

if TYPE_CHECKING:  # pragma: no cover
    from zoo.models.exhibits import Exhibits


class Staff(Base, IDMixin, DeletedAtMixin, CreatedUpdatedMixin):
    """
    Staff Database Model
    """

    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003
    name: Mapped[str]
    job_title: Mapped[str] = mapped_column(default=None, nullable=True)
    email: Mapped[str] = mapped_column(default=None, nullable=True)
    phone: Mapped[str] = mapped_column(default=None, nullable=True)
    notes: Mapped[str] = mapped_column(default=None, nullable=True)
    exhibit_id: Mapped[int] = mapped_column(ForeignKey("exhibits.id"), nullable=True, default=None)

    exhibit: Mapped["Exhibits"] = relationship(back_populates="staff")
