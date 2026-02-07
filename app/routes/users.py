from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.users import UserModel
from config.database import get_db
from app.schemas.users import *
from passlib.context import CryptContext


user_router = APIRouter(tags=['users'])


# hash password:
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def get_password_hash(password: str):
    return pwd_context.hash(password)


# registration:
@user_router.post('/register')
def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
   
    # email validation:
    db_user_email = db.query(UserModel).filter(UserModel.email == request.email).first()
    if db_user_email:
        raise HTTPException(detail='Email already registered', status_code=status.HTTP_400_BAD_REQUEST)
    
    # password validation:
    if request.password != request.confirm_password:
        raise HTTPException(detail='password and confirm_password do not match', status_code=status.HTTP_400_BAD_REQUEST)
    elif not request.strong_password():
        raise HTTPException(
            detail='Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character (like: !@#$%^&*)',
            status_code=status.HTTP_400_BAD_REQUEST
            )
    
    
    # hashing password:
    hashed_password = get_password_hash(request.password)
   
    # create user:
    user = UserModel(name=request.name, email=request.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    # successful response:
    return JSONResponse(
        content={'Server response': f'User <{user.name}> with email <{user.email}> and id <{user.id}> created successfully'
        },
        status_code=status.HTTP_201_CREATED
        )        
    
    

@user_router.post('/login')
def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    
    # email validation:
    db_user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if not db_user:
        raise HTTPException(detail='Email not found', status_code=status.HTTP_404_NOT_FOUND)
    
    # password validation:
    if not pwd_context.verify(request.password, db_user.hashed_password):
        raise HTTPException(detail='Incorrect password', status_code=status.HTTP_400_BAD_REQUEST)
    
    # successful response:
    return JSONResponse(
        content={'Server response': f'User with email <{db_user.email}> logged in successfully'
        },
        status_code=status.HTTP_200_OK
        )
    
    



