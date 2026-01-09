from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from db.database import get_db
from models.booking_models import Booking
from models.room_models import Room
from models.owner_models import Owner

from schema.booking_schema import BookingCreate 

router = APIRouter(prefix="/booking", tags=["Booking"])

# 1. CREATE BOOKING
@router.post("/", status_code=201)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == data.room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found!")

    new_booking = Booking(
        room_id=data.room_id,
        user_id=data.user_id,
        status="Pending"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return {"message": "Booking request sent to Owner! Waiting for payment request.", "booking": new_booking}

@router.put("/approve/{booking_id}")
def approve_booking(
    booking_id: int, 
    owner_email: str = Form(...),
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found!")

    room = db.query(Room).filter(Room.id == booking.room_id).first()
    owner = db.query(Owner).filter(Owner.id == room.owner_id).first()

    if owner.email != owner_email:
        raise HTTPException(
            status_code=403, 
            detail="You are not this room's owner! Permission denied."
        )

    booking.status = "Confirmed"
    room.is_available = False

    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking successfully confirmed by Owner!",
        "status": booking.status,
        "room_title": room.title
    }