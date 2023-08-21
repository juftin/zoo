"""
Exhibits models
"""

from typing import Any, ClassVar, Dict, Optional

from pydantic import ConfigDict, EmailStr, Field

from zoo.schemas.base import (
    CreatedModifiedMixin,
    DeletedMixin,
    RequiredIdMixin,
    ZooModel,
)


class StaffBase(ZooModel):
    """
    Staff model base
    """

    name: str = Field(description="The name of the staff")
    job_title: Optional[str] = Field(default=None, description="The job title of the staff")
    email: Optional[EmailStr] = Field(default=None, description="The email of the staff")
    phone: Optional[str] = Field(default=None, description="The phone number of the staff")
    notes: Optional[str] = Field(
        default=None, description="Optional notes regarding the staff member"
    )
    exhibit_id: Optional[int] = Field(description="The id of the exhibit", default=None)

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

    model_config = ConfigDict(json_schema_extra=StaffBase.get_openapi_create_example())


class StaffRead(
    DeletedMixin,
    CreatedModifiedMixin,
    StaffBase,
    RequiredIdMixin,
):
    """
    Staff model: read
    """

    model_config = ConfigDict(
        json_schema_extra=StaffBase.get_openapi_read_example(), from_attributes=True
    )


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
    exhibit_id: Optional[int] = Field(description="The id of the exhibit", default=None)

    model_config = ConfigDict(json_schema_extra=StaffBase.get_openapi_update_example())
