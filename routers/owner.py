from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.owner_models import Owner
from models.room_models import Room
from schema.owner_schema import OwnerCreate, OwnerResponse, RoomCreate, RoomResponse

router = APIRouter(prefix="/owner", tags=["Owner"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# get all Owner
@router.get("/")
def get_all_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    rooms = db.query(Room).filter(Room.owner_id == owner_id).all()

    return {
        "owner_id": owner.id,
        "owner_name": owner.owner_name,
        "total_rooms": len(rooms),
        "rooms": rooms
    }

# Owner Create
@router.post("/", response_model=OwnerResponse)
def create_owner(data: OwnerCreate, db: Session = Depends(get_db)):
    existing = db.query(Owner).filter(Owner.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email already exists")

    new = Owner(
        owner_name=data.owner_name,
        phone=data.phone,
        email=data.email
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

# Get Owner by ID
@router.get("/{owner_id}", response_model=OwnerResponse)
def get_owner_by_id(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(404, "Owner not found")
    return owner

# Update Owner
@router.put("/{owner_id}", response_model=OwnerResponse)
def update_owner(owner_id: int, data: OwnerCreate, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(404, "Owner not found")

    owner.owner_name = data.owner_name
    owner.phone = data.phone
    owner.email = data.email

    db.commit()
    db.refresh(owner)
    return owner

# Delete Owner
@router.delete("/{owner_id}")
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(404, "Owner not found")

    db.delete(owner)
    db.commit()
    return {"message": "Owner deleted"}

# Add Room under Owner
@router.post("/{owner_id}/room", response_model=RoomResponse)
def add_room(owner_id: int, data: RoomCreate, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(404, "Owner not found")

    room = Room(
        room_name=data.room_name,
        price=data.price,
        owner_id=owner_id
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
