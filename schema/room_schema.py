from pydantic import BaseModel

class RoomCreate(BaseModel):
    title: str
    location: str
    rent: int
    room_type: str
    description: str


# class RoomResponse(RoomCreate):
#     id: int

#     class Config:
#         from_attributes = True

