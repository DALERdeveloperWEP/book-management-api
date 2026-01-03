from fastapi import FastAPI
from app.models import Book  
from app.database import engine, Base
from app.routers.books import router

app = FastAPI(title='Book Management API')

Base.metadata.create_all(bind=engine)

app.include_router(router)