"""Seed Data

Revision ID: 5ff3a5bf3a14
Revises: 9c5764f1931c
Create Date: 2023-08-13 00:25:20.348243

"""

from typing import List, Sequence, Union

from alembic import op
from pydantic import EmailStr

from zoo.models import Animals
from zoo.models.animals import AnimalsCreate
from zoo.models.exhibits import Exhibits, ExhibitsCreate
from zoo.models.staff import Staff, StaffCreate

revision: str = "5ff3a5bf3a14"
down_revision: Union[str, None] = "9c5764f1931c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

exhibits = [
    ExhibitsCreate(
        name="Big Cat Exhibit", description="A big cat exhibit", location="North America"
    ),
    ExhibitsCreate(name="Bird Exhibit", description="A bird exhibit", location="North America"),
    ExhibitsCreate(
        name="Reptile Exhibit", description="A reptile exhibit", location="North America"
    ),
    ExhibitsCreate(
        name="Aquatic Exhibit", description="An aquatic exhibit", location="North America"
    ),
]

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

animals = [
    AnimalsCreate(
        name="Lion",
        description="Ferocious kitty with mane",
        species="Panthera leo",
        exhibit_id=1,
    ),
    AnimalsCreate(
        name="Tiger",
        description="Ferocious kitty with stripes",
        species="Panthera tigris",
        exhibit_id=1,
    ),
    AnimalsCreate(
        name="Cheetah",
        description="Ferocious fast kitty",
        species="Acinonyx jubatus",
        exhibit_id=1,
    ),
    AnimalsCreate(
        name="Leopard",
        description="Ferocious spotted kitty",
        species="Panthera pardus",
        exhibit_id=1,
    ),
    AnimalsCreate(
        name="Cougar",
        description="Ferocious mountain kitty",
        species="Puma concolor",
        exhibit_id=1,
    ),
]


def upgrade() -> None:
    """
    Seed the database with initial data.
    """
    op.bulk_insert(
        table=Exhibits.__table__,
        rows=[exhibit.dict(exclude_unset=True) for exhibit in exhibits],
    )
    op.bulk_insert(
        table=Staff.__table__,
        rows=[staff_member.dict(exclude_unset=True) for staff_member in staff_members],
    )
    op.bulk_insert(
        table=Animals.__table__,
        rows=[animal.dict(exclude_unset=True) for animal in animals],
    )


def downgrade() -> None:
    """
    Remove the initial data from the database.
    """
    animal_delete = Animals.__table__.delete(
        Animals.name.in_([animal.name for animal in animals])  # type: ignore[attr-defined]
    )
    staff_delete = Staff.__table__.delete(
        Staff.name.in_([staff_member.name for staff_member in staff_members])  # type: ignore[attr-defined]
    )
    exhibit_delete = Exhibits.__table__.delete(
        Exhibits.name.in_([exhibit.name for exhibit in exhibits])  # type: ignore[attr-defined]
    )
    op.execute(animal_delete)  # type: ignore[arg-type]
    op.execute(staff_delete)  # type: ignore[arg-type]
    op.execute(exhibit_delete)  # type: ignore[arg-type]
