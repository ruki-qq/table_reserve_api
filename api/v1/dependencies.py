from typing import Annotated, Type

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from api.v1 import crud, models


async def get_one_by_id(
    obj_id: int,
    model: Type[models.Table | models.Reservation],
    session: AsyncSession,
) -> models.Table | models.Reservation:
    obj = await crud.get_one(session=session, model=model, obj_id=obj_id)
    return obj


async def get_table_by_id(
    obj_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Table:
    return await get_one_by_id(obj_id=obj_id, model=models.Table, session=session)


async def get_reservation_by_id(
    obj_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> models.Reservation:
    return await get_one_by_id(obj_id=obj_id, model=models.Reservation, session=session)
