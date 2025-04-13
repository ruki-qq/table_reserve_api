from datetime import datetime

from pydantic import BaseModel


class TableBase(BaseModel):
    name: str
    seats: int
    location: str


class TableCreate(TableBase):
    pass


class Table(TableBase):
    id: int


class ReservationBase(BaseModel):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int


class ReservationCreate(ReservationBase):
    table_id: int


class Reservation(ReservationBase):
    id: int
    table: Table
