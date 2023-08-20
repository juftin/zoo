"""
Exhibits Router app
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select

from zoo.backend.utils import check_model
from zoo.db import get_async_session
from zoo.models.animals import Animals, AnimalsRead
from zoo.models.exhibits import Exhibits, ExhibitsCreate, ExhibitsRead, ExhibitsUpdate
from zoo.models.staff import Staff, StaffRead

logger = logging.getLogger(__name__)

exhibits_router = APIRouter(tags=["exhibits"])


@exhibits_router.get("/exhibits", response_model=List[ExhibitsRead])
async def get_exhibits(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> List[Exhibits]:
    """
    Get exhibits from the database
    """
    result = await session.execute(
        select(Exhibits)
        .where(Exhibits.deleted_at.is_(None))  # type: ignore[union-attr]
        .order_by(Exhibits.id)
        .offset(offset)
        .limit(limit)
    )
    exhibits: List[Exhibits] = result.scalars().all()
    return exhibits


@exhibits_router.post("/exhibits", response_model=ExhibitsRead)
async def create_exhibit(
    exhibit: ExhibitsCreate, session: AsyncSession = Depends(get_async_session)
) -> Exhibits:
    """
    Create a new exhibit in the database
    """
    new_exhibit = Exhibits.from_orm(exhibit)
    session.add(new_exhibit)
    await session.commit()
    await session.refresh(new_exhibit)
    return new_exhibit


@exhibits_router.get("/exhibits/{exhibit_id}", response_model=ExhibitsRead)
async def get_exhibit(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Exhibits:
    """
    Get exhibit from the database
    """
    exhibit: Optional[Exhibits] = await session.get(Exhibits, exhibit_id)
    exhibit = check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    return exhibit


@exhibits_router.delete("/exhibits/{exhibit_id}", response_model=ExhibitsRead)
async def delete_exhibit(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Exhibits:
    """
    Delete exhibit from the database
    """
    exhibit: Optional[Exhibits] = await session.get(Exhibits, exhibit_id)
    exhibit = check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    exhibit.deleted_at = func.CURRENT_TIMESTAMP()  # type: ignore[assignment, union-attr]
    session.add(exhibit)
    await session.commit()
    await session.refresh(exhibit)
    return exhibit


@exhibits_router.patch("/exhibits/{exhibit_id}", response_model=ExhibitsRead)
async def update_exhibit(
    exhibit_id: int, exhibit: ExhibitsUpdate, session: AsyncSession = Depends(get_async_session)
) -> Exhibits:
    """
    Update exhibit from the database
    """
    db_exhibit: Optional[Exhibits] = await session.get(Exhibits, exhibit_id)
    db_exhibit = check_model(model_instance=db_exhibit, model_class=Exhibits, id=exhibit_id)
    for field, value in exhibit.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_exhibit, field, value)
    session.add(db_exhibit)
    await session.commit()
    await session.refresh(db_exhibit)
    return db_exhibit


@exhibits_router.get("/exhibits/{exhibit_id}/animals", response_model=List[AnimalsRead])
async def get_exhibit_animals(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> List[Animals]:
    """
    List animals in an exhibit
    """
    exhibit: Optional[Exhibits] = await session.get(
        entity=Exhibits,
        ident=exhibit_id,
        options=[
            joinedload(Exhibits.animals)  # explicit load of relationship supports async session
        ],
    )
    exhibit = check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    animals: List[Animals] = exhibit.animals
    return animals


@exhibits_router.get("/exhibits/{exhibit_id}/staff", response_model=List[StaffRead])
async def get_exhibit_staff(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> List[Staff]:
    """
    List staff in an exhibit
    """
    exhibit: Optional[Exhibits] = await session.get(
        entity=Exhibits,
        ident=exhibit_id,
        options=[
            joinedload(Exhibits.staff),
        ],
    )
    exhibit = check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    staff: List[Staff] = exhibit.staff
    return staff
