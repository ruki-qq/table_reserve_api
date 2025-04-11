from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import crud, dependencies, models, schemas
from core import db_helper

table_router = APIRouter(prefix="/tables", tags=["tables"])


@table_router.get("/", response_model=list[schemas.Table])
async def get_tables(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> list[schemas.Table]:
    return await crud.get_list(session, models.Table)


@table_router.get("/{table_id}/")
async def get_table(
    table: Annotated[
        models.Table,
        Depends(dependencies.get_one_by_id),
    ],
) -> schemas.Table:
    return table


@table_router.delete("/{table_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table: Annotated[models.Table, Depends(dependencies.get_one_by_id)],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> None:
    await crud.delete_one(session=session, obj=table)


reservation_router = APIRouter(prefix="/reservations", tags=["reservations"])


@reservation_router.get("/", response_model=list[schemas.Reservation])
async def get_reservations(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> list[schemas.Reservation]:
    return await crud.get_list(session, models.Reservation)


@reservation_router.get("/{reservation_id}/")
async def get_reservation(
    reservation: Annotated[
        models.Reservation,
        Depends(dependencies.get_one_by_id),
    ],
) -> schemas.Reservation:
    return reservation


@reservation_router.delete("/{reservation_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation: Annotated[models.Reservation, Depends(dependencies.get_one_by_id)],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> None:
    await crud.delete_one(session=session, obj=reservation)
