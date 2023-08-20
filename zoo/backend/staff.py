"""
Staff backend
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from zoo.backend.utils import check_model
from zoo.db import get_async_session
from zoo.models.staff import Staff, StaffCreate, StaffRead, StaffUpdate

logger = logging.getLogger(__name__)

staff_router = APIRouter(tags=["staff"])


@staff_router.get("/staff", response_model=List[StaffRead])
async def get_staff_members(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> List[Staff]:
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
    staff: List[Staff] = result.scalars().all()
    return staff


@staff_router.get("/staff/{staff_id}", response_model=StaffRead)
async def get_staff(staff_id: int, session: AsyncSession = Depends(get_async_session)) -> Staff:
    """
    Get a staff from the database
    """
    staff: Optional[Staff] = await session.get(Staff, staff_id)
    staff = check_model(model_instance=staff, model_class=Staff, id=staff_id)
    return staff


@staff_router.post("/staff", response_model=StaffRead)
async def create_staff(
    staff: StaffCreate, session: AsyncSession = Depends(get_async_session)
) -> Staff:
    """
    Create a new staff in the database
    """
    new_staff = Staff.from_orm(staff)
    session.add(new_staff)
    await session.commit()
    await session.refresh(new_staff)
    return new_staff


@staff_router.delete("/staff/{staff_id}", response_model=StaffRead)
async def delete_staff(staff_id: int, session: AsyncSession = Depends(get_async_session)) -> Staff:
    """
    Delete a staff in the database
    """
    db_staff: Optional[Staff] = await session.get(Staff, staff_id)
    db_staff = check_model(model_instance=db_staff, model_class=Staff, id=staff_id)
    db_staff.deleted_at = func.CURRENT_TIMESTAMP()  # type: ignore[assignment, union-attr]
    session.add(db_staff)
    await session.commit()
    await session.refresh(db_staff)
    return db_staff


@staff_router.patch("/staff/{staff_id}", response_model=StaffRead)
async def update_staff(
    staff_id: int, staff: StaffUpdate, session: AsyncSession = Depends(get_async_session)
) -> Staff:
    """
    Update a staff in the database
    """
    db_staff: Optional[Staff] = await session.get(Staff, staff_id)
    db_staff = check_model(model_instance=db_staff, model_class=Staff, id=staff_id)
    update_data = staff.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_staff, field, value)
    session.add(db_staff)
    await session.commit()
    await session.refresh(db_staff)
    return db_staff
