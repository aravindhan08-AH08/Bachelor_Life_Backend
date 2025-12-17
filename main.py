from fastapi import FastAPI
from routers import room
from routers.owner import router as owner_router
from db.database import Base, engine
from models.room_models import Room
from models.owner_models import Owner
from routers.user import router as user_router
from routers import Booking

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return{"message": "Welcome to BachelorLife"}


app.include_router(room.router)
app.include_router(owner_router)
app.include_router(user_router)
app.include_router(Booking.router)