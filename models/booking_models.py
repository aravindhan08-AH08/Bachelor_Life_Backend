from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id")) 
    user_id = Column(Integer, ForeignKey("customer.id")) 
    status = Column(String, default="Interested")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    room = relationship("Room", back_populates="bookings")
    user = relationship("Owner")