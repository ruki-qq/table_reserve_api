from datetime import date

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
    table_id: int
    reservation_time: date
    duration_minutes: int


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int
