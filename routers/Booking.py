from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from models.booking_models import Booking
from schema.booking_schema import BookingCreate, BookingResponse
from typing import List

router = APIRouter(prefix="/booking", tags=["Booking"])

# Crete
@router.post("/", response_model=BookingResponse)
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):
    booking = Booking(**data.dict())
    db.add(booking)
    db.commit()
    return booking

# Get All
@router.get("/", response_model=list[BookingResponse])
def get_all_booking(db: Session = Depends(get_db)):
    return db.query(Booking).all()


# Get By User
@router.get("/user/{user_id}", response_model=list[BookingResponse])
def get_user_booking(user_id: int, db: Session = Depends(get_db)):
    return db.query(Booking).filter(Booking.user_id == user_id).all()

# Delete
@router.delete("/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.booking_id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
    return {"message":"Booking deleted Successfully"}