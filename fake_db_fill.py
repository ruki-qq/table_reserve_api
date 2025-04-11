import asyncio
from datetime import datetime, timedelta
from random import randint

from faker import Faker
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.models import Reservation, Table
from core import db_helper

fake = Faker()


async def generate_tables(session: AsyncSession, num_tables: int = 50) -> list[Table]:
    """Generate random tables."""

    tables: list[Table] = []
    for _ in range(num_tables):

        table = Table(
            name=fake.color(),
            seats=randint(1, 100),
            location=fake.city(),
        )

        tables.append(table)
        session.add(table)
    await session.commit()
    return tables


async def generate_reservations(
    session: AsyncSession,
) -> list[Reservation]:
    """Generate random reservations."""

    reservations: list[Reservation] = []
    tables_select = await session.execute(select(Table).order_by(func.random()))

    random_tables_id: list[int] = [table[0].id for table in tables_select]
    print(random_tables_id)
    for id in random_tables_id:
        reservation_time = fake.date_time_between(
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30, hours=24, minutes=60),
        )

        duration_minutes = randint(60, 3600)
        reservation_end = reservation_time + timedelta(minutes=duration_minutes)
        reservation_period = (reservation_time, reservation_end)
        reservation = Reservation(
            customer_name=fake.name(),
            reservation_time=reservation_time,
            duration_minutes=duration_minutes,
            reservation_period=reservation_period,
            table_id=id,
        )
        reservations.append(reservation)
        session.add(reservation)

    await session.commit()
    reservation_time = datetime(2025, 5, 2, 2)
    duration_minutes = 900
    reservation_end = reservation_time + timedelta(minutes=duration_minutes)
    reservation_period = (reservation_time, reservation_end)
    reservation = Reservation(
        customer_name=fake.name(),
        reservation_time=reservation_time,
        duration_minutes=duration_minutes,
        reservation_period=reservation_period,
        table_id=229,
    )

    session.add(reservation)
    try:
        await session.commit()
        return reservations
    except IntegrityError:
        await session.rollback()
        print("The selected time slot is already booked for this table.")


async def main() -> None:
    await generate_tables(db_helper.get_scoped_session())
    await generate_reservations(db_helper.get_scoped_session())


if __name__ == "__main__":
    asyncio.run(main())
