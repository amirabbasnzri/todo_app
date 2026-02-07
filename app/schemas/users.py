from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    username: str = Field(..., min_length=8, max_length=256)
    email: str = EmailStr()
    password: str = Field(..., min_length=8, max_length=128)
    
class UserCreateSchema(UserBaseSchema):
    pass