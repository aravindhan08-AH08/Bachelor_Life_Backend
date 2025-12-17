from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.user_models import Customer
from schema.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/user", tags=["User"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all user
@router.get("/", response_model=list[UserResponse])
def get_all_user(db:Session = Depends(get_db)):
    return db.query(Customer).all()


# Create user
@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    

    user = Customer(
        name=data.name,
        phone=data.phone,
        email=data.email
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Get User by Id
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Customer).filter(Customer.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not Found")
    return user

# Update user
@router.put("/{user_id}", response_model=UserResponse)
def upadate_user(user_id: int, data: UserCreate, db:Session = Depends(get_db)):
    user = db.query(Customer).filter(Customer.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not Found")

    user.name = data.name
    user.phone = data.phone
    user.email = data.email

    db.commit()
    db.refresh(user)
    return user

# Delete User
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Customer).filter(Customer.id == user_id).first()
    if not user:
        raise HTTPException(404, "User Not Found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}