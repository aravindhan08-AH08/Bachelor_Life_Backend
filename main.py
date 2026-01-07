from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles # Typo fixed here
import os
from routers import room, auth, Booking, user, owner
from routers.owner import router as owner_router
from routers.user import router as user_router
from db.database import Base, engine
from models import owner_models, user_models, room_models, booking_models

# 1. First app create pannanum
app = FastAPI(title="Welcome to BachelorLife Backend")

# 2. Database tables create pannum
Base.metadata.create_all(bind=engine)

# 3. Static folder setup (Images store panna)
if not os.path.exists("static/images"):
    os.makedirs("static/images")

# 4. Mount static files (App create panna apram dhaan idhu varanum)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return {"message": "Welcome to BachelorLife"}

# 5. Include Routers
app.include_router(auth.router, tags=["Authentication"]) 
app.include_router(owner_router, tags=["Owner"])
app.include_router(user_router, tags=["User"])
app.include_router(room.router, tags=["Rooms"])
app.include_router(Booking.router, tags=["Booking"])