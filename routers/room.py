from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.room_models import Room
from schema.room_schema import RoomCreate, RoomResponse
from core.security import get_current_user

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# 1. Get ONLY Approved Rooms (Public View)
@router.get("/", response_model=list[RoomResponse])
def get_all_rooms(db: Session = Depends(get_db)):
    # is_approved = True irukura rooms mattum dhaan user-ku theriyanum
    return db.query(Room).filter(Room.is_approved == True).all()

# 2. Create Room (JSON Format - Back to Normal)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db), current_owner: dict = Depends(get_current_user)):
    # room.dict() moolama JSON data-va dictionary-ah mathurom
    room_data = room.dict()
    
    # Swagger-la 'owner_id' kuduthurundhaalum adhai backend ignore pannidum
    room_data.pop("owner_id", None) 
    
    # Login panna owner-oda ID-ah backend-ae sethukum
    new_room = Room(**room_data, owner_id=current_owner.id, is_approved=False) 
    
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return {"message": "Room sent for Admin approval", "room": new_room}

# 3. Admin Route to Approve Room
@router.put("/{room_id}/approve", tags=["Admin"])
def approve_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room.is_approved = True # Admin approve panna dhaan room live aagum
    db.commit()
    return {"message": "Room approved successfully"}

# 4. Delete Room
@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db), current_owner: dict = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    # Intha owner-oda room-ah nu check pannuvom
    if room.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this room")

    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}