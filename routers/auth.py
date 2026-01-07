from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import get_db
from models.owner_models import Owner 
from models.user_models import Customer
from core.security import verify_password, create_access_token

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. First Owner table-la thedurom
    db_user = db.query(Owner).filter(Owner.email == data.username).first()
    
    # 2. Owner table-la illai na, Customer table-la thedurom
    if not db_user:
        db_user = db.query(Customer).filter(Customer.email == data.username).first()
    
    # 3. Rendu table-layume illai na dhaan "Not Found" error
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials - User/Owner Not Found"
        )
    
    # 4. Password check (Owner-kum Customer-kum field name 'hashed_password' dhaan la?)
    if not verify_password(data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # 5. Token create panrom
    access_token = create_access_token(data={"sub": db_user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}