from datetime import datetime
from sqlalchemy import Column, Computed, DateTime, ForeignKey, SmallInteger, String
from sqlalchemy.dialects.postgresql import TSRANGE, ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


class Table(Base):
    name: Mapped[str] = mapped_column(String(64), unique=True)
    seats: Mapped[int] = mapped_column(SmallInteger)
    location: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(64))

    reservation = relationship(
        "Reservation",
        back_populates="table",
        cascade="all, delete",
        passive_deletes=True,
    )


class Reservation(Base):
    customer_name: Mapped[str] = mapped_column(String(128))
    table_id: Mapped[int] = mapped_column(ForeignKey("tables.id", ondelete="CASCADE"))
    reservation_time: Mapped[datetime] = mapped_column(DateTime)
    duration_minutes: Mapped[int] = mapped_column(SmallInteger)

    table = relationship("Table", back_populates="reservation")
    reservation_period: Mapped[TSRANGE] = mapped_column(TSRANGE)

    __table_args__ = (
        ExcludeConstraint(
            ("table_id", "="),
            ("reservation_period", "&&"),
            name="no_overlapping_reservations",
            using="gist",
        ),
    )
