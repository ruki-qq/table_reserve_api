from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from core import Base


class Table(Base):
    name: Mapped[str] = mapped_column(String(64), unique=True)
    seats: Mapped[int] = mapped_column(SmallInteger)
    location: Mapped[str] = mapped_column(String(64))


class Reservation(Base):
    customer_name: Mapped[str] = mapped_column(String(128))
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id"))
    reservation_time: Mapped[datetime] = mapped_column(DateTime)
    duration_minutes: Mapped[int] = mapped_column(SmallInteger)
