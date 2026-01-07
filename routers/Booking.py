from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.booking_models import Booking
from models.room_models import Room
from models.owner_models import Owner
from schema.booking_schema import BookingCreate, BookingResponse
from typing import List

router = APIRouter(prefix="/booking", tags=["Booking"])

@router.post("/", response_model=BookingResponse)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.room_id, Room.is_approved == True).first()
    if not room:
        raise HTTPException(status_code=400, detail="Room not available or not approved")

    owner = db.query(Owner).filter(Owner.id == room.owner_id).first()
    owner_name = owner.owner_name if owner else "Unknown Owner"
    owner_phone = owner.phone if owner else "No Phone"

    new_booking = Booking(
        room_id=data.room_id, 
        user_id=data.user_id,
        status="Interested"
    )
    
    
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    new_booking.owner_name = owner_name 
    
    return {
        "id": new_booking.id,
        "room_id": new_booking.room_id,
        "user_id": new_booking.user_id,
        "status": new_booking.status,
        "owner_name": owner_name,
        "owner_phone": owner_phone
    }

@router.put("/{booking_id}/approve")
def approve_booking(booking_id: int, owner_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    room = db.query(Room).filter(Room.id == booking.room_id).first()
    
    if room.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this room!")

    booking.status = "Approved"
    db.commit()
    return {"message": "Booking approved successfully", "status": booking.status}