"""
Animals Router app
"""

import logging
from typing import List, Optional, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from zoo.api.utils import check_model
from zoo.db import get_async_session
from zoo.models.animals import Animals
from zoo.schemas.animals import AnimalsCreate, AnimalsRead, AnimalsUpdate

logger = logging.getLogger(__name__)

animals_router = APIRouter(tags=["animals"])


@animals_router.get("/animals", response_model=List[AnimalsRead])
async def get_animals(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: AsyncSession = Depends(get_async_session),
) -> List[AnimalsRead]:
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
    animals: Sequence[Animals] = result.scalars().all()
    animals_models = [AnimalsRead.model_validate(animal) for animal in animals]
    return animals_models


@animals_router.post("/animals", response_model=AnimalsRead)
async def create_animal(
    animal: AnimalsCreate, session: AsyncSession = Depends(get_async_session)
) -> AnimalsRead:
    """
    Create a new animal in the database
    """
    new_animal = Animals(**animal.model_dump(exclude_unset=True))
    session.add(new_animal)
    await session.commit()
    await session.refresh(new_animal)
    new_animal_model = AnimalsRead.model_validate(new_animal)
    return new_animal_model


@animals_router.get("/animals/{animal_id}", response_model=AnimalsRead)
async def get_animal(
    animal_id: int, session: AsyncSession = Depends(get_async_session)
) -> AnimalsRead:
    """
    Get an animal from the database
    """
    animal: Optional[Animals] = await session.get(Animals, animal_id)
    animal = check_model(model_instance=animal, model_class=Animals, id=animal_id)
    animal_model = AnimalsRead.model_validate(animal)
    return animal_model


@animals_router.delete("/animals/{animal_id}", response_model=AnimalsRead)
async def delete_animal(
    animal_id: int, session: AsyncSession = Depends(get_async_session)
) -> AnimalsRead:
    """
    Delete an animal from the database
    """
    animal: Optional[Animals] = await session.get(Animals, animal_id)
    animal = check_model(model_instance=animal, model_class=Animals, id=animal_id)
    animal.deleted_at = func.current_timestamp()
    session.add(animal)
    await session.commit()
    await session.refresh(animal)
    animal_model = AnimalsRead.model_validate(animal)
    return animal_model


@animals_router.patch("/animals/{animal_id}", response_model=AnimalsRead)
async def update_animal(
    animal_id: int, animal: AnimalsUpdate, session: AsyncSession = Depends(get_async_session)
) -> AnimalsRead:
    """
    Update an animal in the database
    """
    db_animal: Optional[Animals] = await session.get(Animals, animal_id)
    db_animal = check_model(model_instance=db_animal, model_class=Animals, id=animal_id)
    for field, value in animal.model_dump(exclude_unset=True).items():
        setattr(db_animal, field, value)
    session.add(db_animal)
    await session.commit()
    await session.refresh(db_animal)
    animal_model = AnimalsRead.model_validate(db_animal)
    return animal_model
