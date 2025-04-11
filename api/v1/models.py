from datetime import datetime
from sqlalchemy import Column, Computed, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import TSRANGE, ExcludeConstraint
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

    reservation_period: Mapped[TSRANGE] = mapped_column(TSRANGE)

    __table_args__ = (
        ExcludeConstraint(
            ("table_id", "="),
            ("reservation_period", "&&"),
            name="no_overlapping_reservations",
            using="gist",
        ),
    )
