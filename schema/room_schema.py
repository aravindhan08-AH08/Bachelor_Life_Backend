from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    title: str
    location: str
    rent: int
    room_type: str
    description: str
    bachelor_allowed: Optional[bool] = True


# class RoomResponse(RoomCreate):
#     id: int

#     class Config:
#         from_attributes = True

