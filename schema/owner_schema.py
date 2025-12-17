from pydantic import BaseModel

class OwnerBase(BaseModel):
    owner_name: str
    phone: str
    email: str

class OwnerCreate(OwnerBase):
    pass

class OwnerResponse(OwnerBase):
    id: int
    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    room_name: str
    price: int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
