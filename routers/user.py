from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db # database.py-la get_db irundha idhu okay
from models.owner_models import Owner # Owner model dhaan login-la use panrom
from schema.user_schema import UserCreate, UserResponse
from core.security import get_password_hash

router = APIRouter(prefix="/user", tags=["User"])

# 1. Create User (Ippo Owner table-la register aagum)
@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    # Owner table-la email check panrom
    existing = db.query(Owner).filter(Owner.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_pwd = get_password_hash(data.password)

    new_user = Owner(
        owner_name=data.name, # Model-la 'owner_name' nu irundha idhu correct
        phone=data.phone,
        email=data.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Baki functions (get_all, get_by_id) ellathulayum 'Customer'-ku bathila 'Owner' nu mathi use pannunga.