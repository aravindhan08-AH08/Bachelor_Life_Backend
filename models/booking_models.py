from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from db.database import Base

class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    room_id = Column(Integer)

    booking_date = Column(DateTime(timezone=True), server_default=func.now())
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default="pending")