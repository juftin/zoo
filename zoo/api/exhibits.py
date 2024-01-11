"""
Exhibits Router app
"""

import logging
from typing import List, Optional, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from zoo.api.utils import check_model
from zoo.db import get_async_session
from zoo.models.animals import Animals
from zoo.models.exhibits import Exhibits
from zoo.models.staff import Staff
from zoo.schemas.animals import AnimalsRead
from zoo.schemas.exhibits import ExhibitsCreate, ExhibitsRead, ExhibitsUpdate
from zoo.schemas.staff import StaffRead

logger = logging.getLogger(__name__)

exhibits_router = APIRouter(tags=["exhibits"])


@exhibits_router.get("/exhibits", response_model=List[ExhibitsRead])
async def get_exhibits(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> List[ExhibitsRead]:
    """
    Get exhibits from the database
    """
    result = await session.execute(
        select(Exhibits)
        .where(Exhibits.deleted_at.is_(None))
        .order_by(Exhibits.id)
        .offset(offset)
        .limit(limit)
    )
    exhibits: Sequence[Exhibits] = result.scalars().all()
    exhibit_models = [ExhibitsRead.model_validate(exhibit) for exhibit in exhibits]
    return exhibit_models


@exhibits_router.post("/exhibits", response_model=ExhibitsRead)
async def create_exhibit(
    exhibit: ExhibitsCreate, session: AsyncSession = Depends(get_async_session)
) -> ExhibitsRead:
    """
    Create a new exhibit in the database
    """
    new_exhibit = Exhibits(**exhibit.model_dump(exclude_unset=True))
    session.add(new_exhibit)
    await session.commit()
    await session.refresh(new_exhibit)
    exhibit_model = ExhibitsRead.model_validate(new_exhibit)
    return exhibit_model


@exhibits_router.get("/exhibits/{exhibit_id}", response_model=ExhibitsRead)
async def get_exhibit(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> ExhibitsRead:
    """
    Get exhibit from the database
    """
    exhibit: Optional[Exhibits] = await session.get(Exhibits, exhibit_id)
    exhibit = check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    exhibit_model = ExhibitsRead.model_validate(exhibit)
    return exhibit_model


@exhibits_router.delete("/exhibits/{exhibit_id}", response_model=ExhibitsRead)
async def delete_exhibit(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> ExhibitsRead:
    """
    Delete exhibit from the database
    """
    exhibit: Optional[Exhibits] = await session.get(Exhibits, exhibit_id)
    exhibit = check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    exhibit.deleted_at = func.current_timestamp()
    session.add(exhibit)
    await session.commit()
    await session.refresh(exhibit)
    exhibit_model = ExhibitsRead.model_validate(exhibit)
    return exhibit_model


@exhibits_router.patch("/exhibits/{exhibit_id}", response_model=ExhibitsRead)
async def update_exhibit(
    exhibit_id: int,
    exhibit: ExhibitsUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> ExhibitsRead:
    """
    Update exhibit from the database
    """
    db_exhibit: Optional[Exhibits] = await session.get(Exhibits, exhibit_id)
    db_exhibit = check_model(
        model_instance=db_exhibit, model_class=Exhibits, id=exhibit_id
    )
    for field, value in exhibit.model_dump(exclude_unset=True).items():
        setattr(db_exhibit, field, value)
    session.add(db_exhibit)
    await session.commit()
    await session.refresh(db_exhibit)
    exhibit_model = ExhibitsRead.model_validate(db_exhibit)
    return exhibit_model


@exhibits_router.get("/exhibits/{exhibit_id}/animals", response_model=List[AnimalsRead])
async def get_exhibit_animals(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> List[AnimalsRead]:
    """
    List animals in an exhibit
    """
    exhibit: Optional[Exhibits] = await session.get(
        entity=Exhibits,
        ident=exhibit_id,
        options=[
            joinedload(
                Exhibits.animals
            )  # explicit load of relationship supports async session
        ],
    )
    exhibit = check_model(model_instance=exhibit, model_class=Exhibits, id=exhibit_id)
    animals: List[Animals] = exhibit.animals
    animals_models = [AnimalsRead.model_validate(animal) for animal in animals]
    return animals_models


@exhibits_router.get("/exhibits/{exhibit_id}/staff", response_model=List[StaffRead])
async def get_exhibit_staff(
    exhibit_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> List[StaffRead]:
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
    staff_models = [StaffRead.model_validate(staff) for staff in staff]
    return staff_models
