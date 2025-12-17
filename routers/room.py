from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.room_models import Room
from schema.room_schema import RoomCreate

router = APIRouter(prefix="/rooms", tags=["Rooms"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Room
@router.post("/")
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    new_room = Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

# Read All Rooms
@router.get("/")
def get_all_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

# Read Single Room
@router.get("/{room_id}")
def get_rooms_by_id(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# Update Room
@router.put("/{room_id}")
def update_room(room_id: int, updated: RoomCreate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    for key, value in updated.dict().items():
        setattr(room, key, value)

    db.commit()
    db.refresh(room)
    return room

# Delete Room
@router.delete("/{room_id}")
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    db.delete(room)
    db.commit()
    return {"message": "Room deleted successfully"}