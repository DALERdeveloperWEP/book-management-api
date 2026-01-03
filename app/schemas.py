from typing import Optional, Annotated
from pydantic import BaseModel, Field
from datetime import datetime


class BookCreate(BaseModel):
    title: Annotated[str, Field(max_length=165)] 
    author: Annotated[str, Field(max_length=64)] 
    genre: Annotated[str, Field(max_length=64)] 
    year: datetime 
    rating: Annotated[float, Field(ge=0.0, le=10.0)]


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: datetime
    rating: float


class BookUpdate(BaseModel):
    title: Annotated[Optional[str], Field(max_length=165)] = None
    author: Annotated[Optional[str], Field(max_length=64)] = None
    genre: Annotated[Optional[str], Field(max_length=64)] = None
    year: Optional[datetime] = None
    rating: Annotated[Optional[float], Field(ge=0.0, le=10.0)] = None