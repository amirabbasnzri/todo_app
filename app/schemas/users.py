from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    email: str = EmailStr()
    password: str = Field(..., min_length=8, max_length=128)
    
class UserRegisterSchema(UserBaseSchema):

    name: str = Field(..., min_length=8, max_length=256)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    def strong_password(self) -> bool:
        has_upper = any(char.isupper() for char in self.password)
        has_lower = any(char.islower() for char in self.password)
        has_digit = any(char.isdigit() for char in self.password)
        has_special = any(not char.isalnum() for char in self.password)
        return all([has_upper, has_lower, has_digit, has_special])
    
    
class UserLoginSchema(UserBaseSchema):
    pass