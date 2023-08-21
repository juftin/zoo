"""
Staff backend
"""

import logging
from typing import List, Optional, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from zoo.api.utils import check_model
from zoo.db import get_async_session
from zoo.models.staff import Staff
from zoo.schemas.staff import StaffCreate, StaffRead, StaffUpdate

logger = logging.getLogger(__name__)

staff_router = APIRouter(tags=["staff"])


@staff_router.get("/staff", response_model=List[StaffRead])
async def get_staff_members(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> List[StaffRead]:
    """
    Get staff from the database
    """
    result = await session.execute(
        select(Staff)
        .where(Staff.deleted_at.is_(None))  # type: ignore[union-attr]
        .order_by(Staff.id)
        .offset(offset)
        .limit(limit)
    )
    staff: Sequence[Staff] = result.scalars().all()
    staff_models = [StaffRead.model_validate(staff_member) for staff_member in staff]
    return staff_models


@staff_router.get("/staff/{staff_id}", response_model=StaffRead)
async def get_staff(staff_id: int, session: AsyncSession = Depends(get_async_session)) -> StaffRead:
    """
    Get a staff from the database
    """
    staff: Optional[Staff] = await session.get(Staff, staff_id)
    staff = check_model(model_instance=staff, model_class=Staff, id=staff_id)
    staff_model = StaffRead.model_validate(staff)
    return staff_model


@staff_router.post("/staff", response_model=StaffRead)
async def create_staff(
    staff: StaffCreate, session: AsyncSession = Depends(get_async_session)
) -> StaffRead:
    """
    Create a new staff in the database
    """
    new_staff = Staff(**staff.model_dump(exclude_unset=True))
    session.add(new_staff)
    await session.commit()
    await session.refresh(new_staff)
    staff_model = StaffRead.model_validate(new_staff)
    return staff_model


@staff_router.delete("/staff/{staff_id}", response_model=StaffRead)
async def delete_staff(
    staff_id: int, session: AsyncSession = Depends(get_async_session)
) -> StaffRead:
    """
    Delete a staff in the database
    """
    db_staff: Optional[Staff] = await session.get(Staff, staff_id)
    db_staff = check_model(model_instance=db_staff, model_class=Staff, id=staff_id)
    db_staff.deleted_at = func.current_timestamp()
    session.add(db_staff)
    await session.commit()
    await session.refresh(db_staff)
    staff_model = StaffRead.model_validate(db_staff)
    return staff_model


@staff_router.patch("/staff/{staff_id}", response_model=StaffRead)
async def update_staff(
    staff_id: int, staff: StaffUpdate, session: AsyncSession = Depends(get_async_session)
) -> StaffRead:
    """
    Update a staff in the database
    """
    db_staff: Optional[Staff] = await session.get(Staff, staff_id)
    db_staff = check_model(model_instance=db_staff, model_class=Staff, id=staff_id)
    update_data = staff.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_staff, field, value)
    session.add(db_staff)
    await session.commit()
    await session.refresh(db_staff)
    staff_model = StaffRead.model_validate(db_staff)
    return staff_model
