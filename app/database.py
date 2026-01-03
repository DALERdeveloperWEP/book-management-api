from sqlalchemy import URL, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, DeclarativeBase
from app.config import settings


url = URL.create(
    drivername='postgresql+psycopg2',
    username=settings.db_user,
    password=settings.db_pass,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name
)

engine = create_engine(url=url)
Base: DeclarativeBase = declarative_base() 
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()