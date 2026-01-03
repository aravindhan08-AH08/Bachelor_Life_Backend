from pydantic import BaseModel
from typing import Optional

class RoomCreate(BaseModel):
    title: str
    location: str
    rent: int
    room_type: str
    description: str
    owner_id: int 
    bachelor_allowed: Optional[bool] = True

class RoomResponse(BaseModel):
    id: int
    title: str
    location: str
    rent: int
    room_type: str
    description: str
    bachelor_allowed: bool
    class Config:
        from_attributes = True