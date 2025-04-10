from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper

from . import crud
from .models import Table, Reservation


async def get_one_by_id(
    obj_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Table | Reservation:
    obj = await crud.get_one(session=session, obj_id=obj_id)
    if obj is not None:
        return obj

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Object with id:{id} not found!",
    )
