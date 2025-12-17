from pydantic import BaseModel
from datetime import date

class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    start_date: date
    end_date: date

class BookingUpdate(BaseModel):
    start_date: date
    end_date: date
    status: str

class BookingResponse(BaseModel):
    booking_id: int
    user_id: int
    room_id: int
    start_date: date
    end_date: date
    status: str

    class Config:
        from_attributes = True