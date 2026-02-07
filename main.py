from fastapi import FastAPI
from app.routes.tasks import task_router    
from app.routes.users import user_router
from config.database import Base, engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # async DB setup if needed
    Base.metadata.create_all(bind=engine)
    yield
app = FastAPI(lifespan=lifespan)


app.include_router(task_router, prefix='/task')
app.include_router(user_router, prefix='/user')