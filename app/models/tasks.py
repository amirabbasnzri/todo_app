from config.database import Base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, func


class TaskModel(Base):
    
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, is_completed={self.is_completed}, updated_at={self.updated_at})>"
    
    def mark_completed(self) -> None:
        self.is_completed = True
        self.updated_at = func.now()
        