from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import crud, dependencies, models, schemas
from core import db_helper

table_router = APIRouter(prefix="/tables", tags=["tables"])
reservation_router = APIRouter(prefix="/reservations", tags=["reservations"])


@table_router.get("/", response_model=list[schemas.Table])
async def get_tables(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> list[schemas.Table]:
    return await crud.get_list(session, models.Table)


@table_router.get("/{obj_id}/")
async def get_table(
    table: Annotated[
        models.Table,
        Depends(dependencies.get_table_by_id),
    ],
) -> schemas.Table:
    return table


@table_router.post(
    "/",
    response_model=schemas.Table,
    status_code=status.HTTP_201_CREATED,
)
async def create_table(
    table_in: schemas.TableCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> schemas.Table:
    return await crud.create_one(session=session, model=models.Table, model_in=table_in)


@table_router.delete("/{obj_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(
    table: Annotated[models.Table, Depends(dependencies.get_table_by_id)],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> None:
    await crud.delete_one(session=session, obj=table)


@reservation_router.get("/", response_model=list[schemas.Reservation])
async def get_reservations(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> list[schemas.Reservation]:
    return await crud.get_list(session, models.Reservation)


@reservation_router.get("/{obj_id}/")
async def get_reservation(
    reservation: Annotated[
        models.Reservation,
        Depends(dependencies.get_reservation_by_id),
    ],
) -> schemas.Reservation:
    return reservation


@reservation_router.post(
    "/",
    response_model=schemas.Reservation,
    status_code=status.HTTP_201_CREATED,
)
async def create_reservation(
    reservation_in: schemas.ReservationCreate,
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> schemas.Reservation:
    reservation = await crud.create_one(
        session=session, model=models.Reservation, model_in=reservation_in
    )
    return await dependencies.get_reservation_by_id(
        obj_id=reservation.id, session=session
    )


@reservation_router.delete("/{obj_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation: Annotated[
        models.Reservation, Depends(dependencies.get_reservation_by_id)
    ],
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.scoped_session_dependency),
    ],
) -> None:
    await crud.delete_one(session=session, obj=reservation)
