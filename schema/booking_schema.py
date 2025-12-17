from pydantic import BaseModel
from datetime import date, datetime

class BookingBase(BaseModel):
    user_id: int
    room_id: int
    start_date: date
    end_date: date


class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    booking_id: int
    booking_date: datetime

    class Config:
        from_attributes = True
