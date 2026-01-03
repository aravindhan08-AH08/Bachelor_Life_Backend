from pydantic import BaseModel, EmailStr

# Base class la password vekka koodadhu, ஏன்னா அது Response-layum vandhidum
class OwnerBase(BaseModel):
    owner_name: str
    phone: str
    email: EmailStr

# Create pannumbodhu mattum dhaan password thevai
class OwnerCreate(OwnerBase):
    password: str 

# Response la password field irukka koodadhu
class OwnerResponse(OwnerBase):
    id: int
    
    class Config:
        from_attributes = True # Pydantic V2-ku idhu dhaan correct

# --- Rooms Schema ---

class RoomBase(BaseModel):
    room_name: str
    price: int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True # Inga 'orm_mode' ah 'from_attributes' nu mathunga