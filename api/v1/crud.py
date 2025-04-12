from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import models, schemas


async def get_list(
    session: AsyncSession, model: models.Table | models.Reservation
) -> list[schemas.Table | schemas.Reservation]:
    stmt = select(model).order_by(model.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_one(
    session: AsyncSession, model: models.Table | models.Reservation, obj_id: int
) -> schemas.Table | schemas.Reservation | None:
    stmt = select(model).filter(model.id == obj_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_one(
    session: AsyncSession,
    model: models.Table | models.Reservation,
    model_in: schemas.TableCreate,
) -> schemas.Table | None:
    if model == models.Reservation:
        reservation_end = model.reservation_time + timedelta(
            minutes=model.duration_minutes
        )
        reservation_period = (model.reservation_time, reservation_end)
        obj = model(**model_in.model_dump(), reservation_period=reservation_period)
    else:

        obj = model(**model_in.model_dump())
    try:
        session.add(obj)
        await session.commit()
        return obj
    except IntegrityError:
        await session.rollback()
        print("The selected time slot is already booked for this table.")


async def delete_one(
    session: AsyncSession, obj: models.Table | models.Reservation
) -> None:
    await session.delete(obj)
    await session.commit()
