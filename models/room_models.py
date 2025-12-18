from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from db.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    location = Column(String)
    rent = Column(Integer)
    room_type = Column(String)
    description = Column(String)
    bachelor_allowed = Column(Boolean, default=True)
