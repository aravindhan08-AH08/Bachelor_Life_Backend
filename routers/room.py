from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from db.database import get_db
from models.room_models import Room
from schema.room_schema import RoomResponse
from deps import get_current_user
from typing import Optional, List
import shutil
import os

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# Image upload folder logic
UPLOAD_DIR = "static/room_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 1. GET ALL ROOMS (Approved rooms mattum kaattum)
@router.get("/", response_model=List[RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    return db.query(Room).filter(Room.is_approved == True, Room.is_available == True).all()

# 2. CREATE ROOM (With Image & Amenities)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_room(
    title: str = Form(...),
    location: str = Form(...),
    rent: int = Form(...),
    room_type: str = Form(...),
    max_persons: int = Form(1),
    description: str = Form(...),
    bachelor_allowed: bool = Form(True),
    wifi: bool = Form(False),
    ac: bool = Form(False),
    attached_bath: bool = Form(False),
    kitchen_access: bool = Form(False),
    parking: bool = Form(False),
    laundry: bool = Form(False),
    security: bool = Form(False),
    gym: bool = Form(False),
    is_available: bool = Form(True),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_owner: any = Depends(get_current_user)
):
    file_path = None
    if file:
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    new_room = Room(
        title=title, location=location, rent=rent, room_type=room_type,
        description=description, max_persons=max_persons, bachelor_allowed=bachelor_allowed,
        wifi=wifi, ac=ac, attached_bath=attached_bath,
        kitchen_access=kitchen_access, parking=parking, laundry=laundry,
        security=security, gym=gym, image_url=file_path, is_available=is_available,
        owner_id=current_owner.id, is_approved=False
    )
    
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return {"message": "Room listed successfully!", "room": new_room}

# 3. UPDATE ROOM
@router.put("/{room_id}", response_model=RoomResponse)
async def update_room(
    room_id: int,
    title: str = Form(...),
    location: str = Form(...),
    rent: int = Form(...),
    room_type: str = Form(...),
    max_persons: int = Form(...),
    description: str = Form(...),
    bachelor_allowed: bool = Form(True),
    wifi: bool = Form(False),
    ac: bool = Form(False),
    attached_bath: bool = Form(False),
    kitchen_access: bool = Form(False),
    parking: bool = Form(False),
    laundry: bool = Form(False),
    security: bool = Form(False),
    gym: bool = Form(False),
    is_available: bool = Form(True),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_owner: any = Depends(get_current_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized to update")

    if file:
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        room.image_url = file_path

    room.title = title
    room.location = location
    room.rent = rent
    room.room_type = room_type
    room.max_persons = max_persons
    room.description = description
    room.bachelor_allowed = bachelor_allowed
    room.wifi = wifi
    room.ac = ac
    room.attached_bath = attached_bath
    room.kitchen_access = kitchen_access
    room.parking = parking
    room.laundry = laundry
    room.security = security
    room.gym = gym
    room.is_available = is_available
    room.is_approved = True 

    db.commit()
    db.refresh(room)
    return room

# 4. DELETE ROOM
@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db), current_owner: any = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    if room.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this room")

    # Image irundha adhaiyum delete panna idhu use aagum
    if room.image_url and os.path.exists(room.image_url):
        os.remove(room.image_url)

    db.delete(room)
    db.commit()
    return {"message": "Room and its image deleted successfully"}