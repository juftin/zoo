"""
Exhibits Router app
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from zoo.backend.utils import check_model
from zoo.db import get_session
from zoo.models.animals import Animals, AnimalsRead
from zoo.models.exhibits import Exhibits, ExhibitsCreate, ExhibitsRead, ExhibitsUpdate

logger = logging.getLogger(__name__)

exhibits_router = APIRouter(tags=["exhibits"])


@exhibits_router.get("/exhibits", response_model=List[ExhibitsRead])
async def get_exhibits(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_session),
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
    exhibit: ExhibitsCreate, session: AsyncSession = Depends(get_session)
) -> Exhibits:
    """
    Create a new exhibit in the database
    """
    new_exhibit = Exhibits(**exhibit.dict())
    session.add(new_exhibit)
    await session.commit()
    await session.refresh(new_exhibit)
    return new_exhibit


@exhibits_router.get("/exhibits/{exhibit_id}", response_model=ExhibitsRead)
async def get_exhibit(
    exhibit_id: int,
    session: AsyncSession = Depends(get_session),
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
    session: AsyncSession = Depends(get_session),
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
    exhibit_id: int, exhibit: ExhibitsUpdate, session: AsyncSession = Depends(get_session)
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
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_session),
) -> List[Animals]:
    """
    List animals in an exhibit
    """
    exhibit: Optional[Exhibits] = await session.get(Exhibits, exhibit_id)
    check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    animals = await session.execute(
        select(Animals)
        .where(Animals.exhibit_id == exhibit_id)
        .order_by(Animals.id)
        .offset(offset)
        .limit(limit)
    )
    return animals.scalars().all()
