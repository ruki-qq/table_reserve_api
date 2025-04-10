from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import models, schemas, Table
from core import Base


async def get_list(
    session: AsyncSession, model: Base
) -> list[schemas.Table | schemas.Reservation]:
    stmt = select(model).order_by(model.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_one(
    session: AsyncSession, model: Base, id: int
) -> schemas.Table | schemas.Reservation | None:
    stmt = select(model).filter(models.Table.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_one(
    session: AsyncSession, model: Base, model_in: schemas.TableCreate
) -> schemas.Table:
    candidate = model(**model_in.model_dump())
    session.add(candidate)
    await session.commit()
    return candidate


async def delete_one(session: AsyncSession, obj: Base) -> None:
    await session.delete(obj)
    await session.commit()
