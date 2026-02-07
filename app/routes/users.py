from fastapi import APIRouter, Path, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.users import UserModel
from config.database import get_db
from app.schemas.users import *
from passlib.context import CryptContext


user_router = APIRouter()


# hash password:
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def get_password_hash(password: str):
    return pwd_context.hash(password)


# registration:
@user_router.post('/register')
def user_register(request: UserCreateSchema, db: Session = Depends(get_db)):
   
    # email validation:
    db_user_email = db.query(UserModel).filter(UserModel.email == request.email).first()
    if db_user_email:
        raise HTTPException(detail='Email already registered', status_code=status.HTTP_400_BAD_REQUEST)
    
    # hashing password:
    hashed_password = get_password_hash(request.password)
    
    # create user:
    user = UserModel(name=request.name, email=request.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return JSONResponse(content={'Server response': f'User {user.name} with email {user.email} and id {user.id} created successfully'})        
    
    
    
    
    



