"""Seed Data

Revision ID: e69c9264375d
Revises: e5fccc3522ce
Create Date: 2023-08-20 17:30:29.527566

"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import delete
from sqlalchemy.orm import Session

from zoo.models.animals import Animals
from zoo.models.exhibits import Exhibits
from zoo.models.staff import Staff

revision: str = "e69c9264375d"
down_revision: Union[str, None] = "e5fccc3522ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


exhibits = [
    Exhibits(name="Big Cat Exhibit", description="A big cat exhibit", location="North America"),
    Exhibits(name="Bird Exhibit", description="A bird exhibit", location="North America"),
    Exhibits(name="Reptile Exhibit", description="A reptile exhibit", location="North America"),
    Exhibits(name="Aquatic Exhibit", description="An aquatic exhibit", location="North America"),
]

staff_members = [
    Staff(
        name="John Doe",
        job_title="Zookeeper",
        email="john-does-loves-kitties@gmail.com",
        phone="555-555-5555",
        notes="John Doe is a great zookeeper and loves cats!",
        exhibit_id=1,
    ),
    Staff(
        name="Jane Doe",
        job_title="Zookeeper",
        email="jane-doe@yahoo.com",
        phone="555-444-6666",
        notes="Jane Doe is a highly skilled bird keeper!",
        exhibit_id=3,
    ),
]

animals = [
    Animals(
        name="Lion",
        description="Ferocious kitty with mane",
        species="Panthera leo",
        exhibit_id=1,
    ),
    Animals(
        name="Tiger",
        description="Ferocious kitty with stripes",
        species="Panthera tigris",
        exhibit_id=1,
    ),
    Animals(
        name="Cheetah",
        description="Ferocious fast kitty",
        species="Acinonyx jubatus",
        exhibit_id=1,
    ),
    Animals(
        name="Leopard",
        description="Ferocious spotted kitty",
        species="Panthera pardus",
        exhibit_id=1,
    ),
    Animals(
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
    connection = op.get_bind()
    session = Session(bind=connection)
    with session.begin():
        for exhibit in exhibits:
            session.add(exhibit)
        for staff_member in staff_members:
            session.add(staff_member)
        for animal in animals:
            session.add(animal)
    session.commit()


def downgrade() -> None:
    """
    Rollback the database upgrade
    """
    animal_delete = delete(Animals).where(Animals.name.in_([animal.name for animal in animals]))
    staff_delete = delete(Staff).where(
        Staff.name.in_([staff_member.name for staff_member in staff_members])
    )
    exhibit_delete = delete(Exhibits).where(
        Exhibits.name.in_([exhibit.name for exhibit in exhibits])
    )
    op.execute(animal_delete)  # type: ignore[arg-type]
    op.execute(staff_delete)  # type: ignore[arg-type]
    op.execute(exhibit_delete)  # type: ignore[arg-type]
