from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import crud, dependencies, models, schemas
from core import db_helper

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("", response_model=list[models.Table])
async def get_tables(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
):
    return await crud.get_list(session, models.Table)


@router.get("/{table_id}")
async def get_table(
    table: Annotated[
        models.Table,
        Depends(dependencies.get_one_by_id),
    ],
):
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    report: Annotated[models.Table, Depends(dependencies.get_one_by_id)],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> None:
    await crud.delete_one(session=session, obj=table)
