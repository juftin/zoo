"""
Animals Router app
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from zoo.db import get_session
from zoo.models.animals import Animals, AnimalsCreate, AnimalsRead

animals_router = APIRouter(tags=["animals"])


@animals_router.get("/animals", response_model=list[AnimalsRead])
async def get_animals(session: AsyncSession = Depends(get_session)) -> list[Animals]:
    """
    Get animals from the database
    """
    result = await session.execute(select(Animals))
    animals: list[Animals] = result.scalars().all()
    return animals


@animals_router.post("/animals", response_model=AnimalsRead)
async def create_animal(animal: AnimalsCreate, session: AsyncSession = Depends(get_session)) -> Animals:
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
    result = await session.execute(select(Animals).where(Animals.id == animal_id))
    animal: Animals | None = result.scalar_one_or_none()
    if animal is None:
        raise HTTPException(status_code=404, detail=f"Error: Animal not found - ID: {animal_id}")
    return animal


@animals_router.delete("/animals/{animal_id}", response_model=AnimalsRead)
async def delete_animal(animal_id: int, session: AsyncSession = Depends(get_session)) -> Animals:
    """
    Delete an animal from the database
    """
    result = await session.execute(select(Animals).where(Animals.id == animal_id))
    animal: Animals | None = result.scalar_one_or_none()
    if animal is None:
        raise HTTPException(status_code=404, detail=f"Error: Animal not found - ID # {animal_id}")
    await session.delete(animal)
    await session.commit()
    return animal
