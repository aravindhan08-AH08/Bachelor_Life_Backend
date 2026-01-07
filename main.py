from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import os
from routers import room, Booking, user, owner
from routers.owner import router as owner_router
from routers.user import router as user_router
from db.database import Base, engine
from models import owner_models, user_models, room_models, booking_models

app = FastAPI(title="Welcome to BachelorLife Backend")

Base.metadata.create_all(bind=engine)


if not os.path.exists("static/images"):
    os.makedirs("static/images")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"message": "Welcome to BachelorLife"}

app.include_router(owner_router, tags=["Owner"])
app.include_router(user_router, tags=["User"])
app.include_router(room.router, tags=["Rooms"])
app.include_router(Booking.router, tags=["Booking"])