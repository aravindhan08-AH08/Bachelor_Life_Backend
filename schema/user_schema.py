from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    phone: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class config:
        orm_mode = True