from config.database import Base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, func


class UserModel(Base):
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    hashed_password = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'id: {self.id}, username: {self.username}, is_active: {self.is_active}'