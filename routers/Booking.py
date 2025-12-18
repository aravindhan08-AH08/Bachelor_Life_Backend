from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.booking_models import Booking
from schema.booking_schema import BookingCreate, BookingResponse, BookingUpdate
from typing import List

router = APIRouter(prefix="/booking", tags=["Booking"])

# Get All Bookings
@router.get("/", response_model=List[BookingResponse])
def get_all_booking(db: Session = Depends(get_db)):
    return db.query(Booking).all()

# Create Booking
@router.post("/", response_model=BookingResponse)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    booking = Booking(**data.dict())
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking




# Get Booking By User
@router.get("/user/{user_id}", response_model=List[BookingResponse])
def get_user_booking(user_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.user_id == user_id).all()


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, data: BookingUpdate, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(
        Booking.booking_id == booking_id
    ).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not Found")

    booking.start_date = data.start_date
    booking.end_date = data.end_date
    booking.status = data.status

    db.commit()
    db.refresh(booking)
    return booking


# Delete Booking
@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not Found")

    db.delete(booking)
    db.commit()
    return {"message": "Booking deleted successfully"}