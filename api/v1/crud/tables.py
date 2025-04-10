from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1 import models, schemas


async def get_tables(session: AsyncSession) -> list[schemas.Table]:
    stmt = select(models.Table).order_by(models.Table.id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_table(session: AsyncSession, table_id: int) -> schemas.Table | None:
    stmt = select(models.Table).filter(models.Table.id == table_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_table(
    session: AsyncSession, table_in: schemas.TableCreate
) -> schemas.Table:
    candidate = models.Table(**table_in.model_dump())
    session.add(candidate)
    await session.commit()
    return candidate
