from pydantic import BaseModel, EmailStr
class OwnerBase(BaseModel):
    owner_name: str
    phone: str
    email: EmailStr

class OwnerCreate(OwnerBase):
    password: str 

class OwnerResponse(OwnerBase):
    id: int
    
    class Config:
        from_attributes = True 


class RoomBase(BaseModel):
    room_name: str
    price: int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True