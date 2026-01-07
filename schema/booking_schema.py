from pydantic import BaseModel
from datetime import datetime

class BookingBase(BaseModel):
    room_id: int

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
    status: str
    owner_name: str
    created_at: datetime

    class Config:
        from_attributes = True