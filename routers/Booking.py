from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.booking_models import Booking
from models.room_models import Room
from models.owner_models import Owner
from schema.booking_schema import BookingCreate, BookingResponse
from deps import get_current_user # Namma pudhu deps-ah import panrom
from typing import List
from deps import get_current_user

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.post("/", response_model=BookingResponse)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    room = db.query(Room).filter(Room.id == data.room_id, Room.is_approved == True).first()
    if not room:
        raise HTTPException(status_code=400, detail="Room not available")

    owner = db.query(Owner).filter(Owner.id == room.owner_id).first()
    owner_name = owner.owner_name if owner else "Unknown"

    new_booking = Booking(
        room_id=data.room_id, 
        user_id=current_user.id, 
        status="Interested"
    )
    
    room.is_approved = False 
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    new_booking.owner_name = owner_name 
    return new_booking

@router.put("/{booking_id}/approve")
def approve_booking(booking_id: int, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Room check
    room = db.query(Room).filter(Room.id == booking.room_id).first()
    
    # Security: This is check for to the owner only
    if room.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Neenga intha room-oda owner illai!")

    booking.status = "Approved"
    db.commit()
    return {"message": "Booking approved by Owner", "status": booking.status}