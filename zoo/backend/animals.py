"""
Animals Router app
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from zoo.backend.utils import check_model
from zoo.db import get_session
from zoo.models.animals import Animals, AnimalsCreate, AnimalsRead, AnimalsUpdate

logger = logging.getLogger(__name__)

animals_router = APIRouter(tags=["animals"])


@animals_router.get("/animals", response_model=List[AnimalsRead])
async def get_animals(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_session),
) -> List[Animals]:
    """
    Get animals from the database
    """
    result = await session.execute(
        select(Animals)
        .where(Animals.deleted_at.is_(None))  # type: ignore[union-attr]
        .order_by(Animals.id)
        .offset(offset)
        .limit(limit)
    )
    animals: List[Animals] = result.scalars().all()
    return animals


@animals_router.post("/animals", response_model=AnimalsRead)
async def create_animal(
    animal: AnimalsCreate, session: AsyncSession = Depends(get_session)
) -> Animals:
    """
    Create a new animal in the database
    """
    new_animal = Animals(**animal.dict())
    session.add(new_animal)
    await session.commit()
    await session.refresh(new_animal)
    return new_animal


@animals_router.get("/animals/{animal_id}", response_model=AnimalsRead)
async def get_animal(animal_id: int, session: AsyncSession = Depends(get_session)) -> Animals:
    """
    Get an animal from the database
    """
    animal: Optional[Animals] = await session.get(Animals, animal_id)
    animal = check_model(model_instance=animal, model_class=Animals, id=animal_id)
    return animal


@animals_router.delete("/animals/{animal_id}", response_model=AnimalsRead)
async def delete_animal(animal_id: int, session: AsyncSession = Depends(get_session)) -> Animals:
    """
    Delete an animal from the database
    """
    animal: Optional[Animals] = await session.get(Animals, animal_id)
    animal = check_model(model_instance=animal, model_class=Animals, id=animal_id)
    animal.deleted_at = func.CURRENT_TIMESTAMP()  # type: ignore[assignment, union-attr]
    session.add(animal)
    await session.commit()
    await session.refresh(animal)
    return animal


@animals_router.patch("/animals/{animal_id}", response_model=AnimalsRead)
async def update_animal(
    animal_id: int, animal: AnimalsUpdate, session: AsyncSession = Depends(get_session)
) -> Animals:
    """
    Update an animal in the database
    """
    db_animal: Optional[Animals] = await session.get(Animals, animal_id)
    db_animal = check_model(model_instance=db_animal, model_class=Animals, id=animal_id)
    for field, value in animal.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_animal, field, value)
    session.add(db_animal)
    await session.commit()
    await session.refresh(db_animal)
    return db_animal
