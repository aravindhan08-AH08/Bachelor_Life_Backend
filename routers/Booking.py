from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.booking_models import Booking
from models.room_models import Room
from schema.booking_schema import BookingCreate, BookingResponse
from core.security import get_current_user
from typing import List

router = APIRouter(prefix="/booking", tags=["Booking"])

# 1. Express Interest (NoBroker style)
@router.post("/", response_model=BookingResponse)
def create_booking(data: BookingCreate, db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    # Check if room exists and is approved/available
    room = db.query(Room).filter(Room.id == data.room_id, Room.is_approved == True).first()
    
    if not room:
        raise HTTPException(status_code=400, detail="Room not available or already taken")

    # Security Check: current_user dictionary-ah irundha ['id'], object-ah irundha .id
    u_id = current_user.id if hasattr(current_user, 'id') else current_user.get('id')

    # Create interest record
    new_booking = Booking(
        room_id=data.room_id, 
        user_id=u_id, 
        status="Interested"
    )
    
    # Logic: Property-ah public view-la irundhu hide panrom
    room.is_approved = False 
    
    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        return new_booking
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

# 2. Get My Interested Properties (User Dashboard)
@router.get("/me", response_model=List[BookingResponse])
def get_my_interests(db: Session = Depends(get_db), current_user: any = Depends(get_current_user)):
    u_id = current_user.id if hasattr(current_user, 'id') else current_user.get('id')
    return db.query(Booking).filter(Booking.user_id == u_id).all()