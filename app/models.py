from sqlalchemy import Column, Integer, String, DateTime, Float


from app.database import Base


class Book(Base):
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(length=165), nullable=False)
    author = Column(String(length=64), nullable=False)
    genre = Column(String(length=64), nullable=False)
    year = Column(DateTime, nullable=False)
    rating = Column(Float, nullable=False)