"""
Exhibits models
"""

from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional

from pydantic import EmailStr
from sqlalchemy import Table
from sqlalchemy.event import listens_for
from sqlalchemy.future import Connection
from sqlmodel import Field, Relationship

from zoo.models.base import (
    CreatedModifiedMixin,
    DeletedMixin,
    OptionalIdMixin,
    RequiredIdMixin,
    ZooModel,
)

if TYPE_CHECKING:
    from zoo.models.exhibits import Exhibits


class StaffBase(ZooModel):
    """
    Staff model base
    """

    name: str = Field(description="The name of the staff", index=True, unique=True)
    job_title: Optional[str] = Field(default=None, description="The job title of the staff")
    email: Optional[EmailStr] = Field(default=None, description="The email of the staff")
    phone: Optional[str] = Field(default=None, description="The phone number of the staff")
    notes: Optional[str] = Field(
        default=None, description="Optional notes regarding the staff member"
    )
    exhibit_id: Optional[int] = Field(
        description="The id of the exhibit", foreign_key="exhibits.id", nullable=True, default=None
    )

    __example__: ClassVar[Dict[str, Any]] = {
        "name": "John Doe",
        "job_title": "Zookeeper",
        "email": "big.cat.lover@gmail.com",
        "phone": "555-555-5555",
        "notes": "John Doe is a great zookeeper and loves cats!",
        "exhibit_id": 1,
    }


class StaffCreate(StaffBase):
    """
    Staff model: create
    """

    class Config:
        """
        Config for StaffCreate
        """

        schema_extra: ClassVar[Dict[str, Any]] = StaffBase.get_openapi_create_example()


class StaffRead(
    DeletedMixin,
    CreatedModifiedMixin,
    StaffBase,
    RequiredIdMixin,
):
    """
    Staff model: read
    """

    class Config:
        """
        Config for StaffRead
        """

        schema_extra: ClassVar[Dict[str, Any]] = StaffBase.get_openapi_read_example()


class Staff(
    DeletedMixin,
    CreatedModifiedMixin,
    StaffBase,
    OptionalIdMixin,
    table=True,
):
    """
    Staff model: database table
    """

    exhibit: Optional["Exhibits"] = Relationship(back_populates="staff")


class StaffUpdate(ZooModel):
    """
    Staff model: update
    """

    name: Optional[str] = Field(description="The name of the staff")
    job_title: Optional[str] = Field(default=None, description="The job title of the staff")
    email: Optional[EmailStr] = Field(default=None, description="The email of the staff")
    phone: Optional[str] = Field(default=None, description="The phone number of the staff")
    notes: Optional[str] = Field(
        default=None, description="Optional notes regarding the staff member"
    )
    exhibit_id: Optional[int] = Field(
        description="The id of the exhibit", foreign_key="exhibits.id", nullable=True, default=None
    )

    class Config:
        """
        Config for StaffUpdate
        """

        schema_extra: ClassVar[Dict[str, Any]] = StaffBase.get_openapi_update_example()


@listens_for(Staff.__table__, "after_create")  # type: ignore[attr-defined]
def seed_exhibits_table(target: Table, connection: Connection, **kwargs) -> None:
    """
    Seed the Animals table with initial data
    """
    staff_members: List[StaffCreate] = [
        StaffCreate(
            name="John Doe",
            job_title="Zookeeper",
            email=EmailStr("john-does-loves-kitties@gmail.com"),
            phone="555-555-5555",
            notes="John Doe is a great zookeeper and loves cats!",
            exhibit_id=1,
        ),
        StaffCreate(
            name="Jane Doe",
            job_title="Zookeeper",
            email=EmailStr("jane-doe@yahoo.com"),
            phone="555-444-6666",
            notes="Jane Doe is a highly skilled bird keeper!",
            exhibit_id=3,
        ),
    ]
    connection.execute(
        target.insert(), [exhibit.dict(exclude_unset=True) for exhibit in staff_members]
    )
