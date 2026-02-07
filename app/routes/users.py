from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db


user_router = APIRouter()


@user_router.post('/register')
def user_register():
    pass



