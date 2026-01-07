from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from db.database import get_db
from models.owner_models import Owner
from models.user_models import Customer 
from core.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = auth.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(Owner).filter(Owner.email == email).first()
    
    if user is None:
        user = db.query(Customer).filter(Customer.email == email).first()
        
    if user is None:
        raise credentials_exception
        
    return user