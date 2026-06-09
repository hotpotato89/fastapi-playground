from datetime import datetime
from typing import Optional

from src.app.core.enums import Genre

from .base import BaseSchema
from pydantic import Field, field_validator


class BookCreate(BaseSchema):
    title: str = Field(..., max_length=30, description="Book title")
    author: str = Field(..., max_length=60, description="Book author")
    description: Optional[str] = Field(None, description="Book desctiption")
    genre: Genre = Field(..., description='Genre of book')

    @field_validator("title", "author")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Cannot be empty")
        return v.strip().capitalize()


class BookResponse(BaseSchema):
    """Response from database"""

    id: int
    title: str
    author: str
    description: Optional[str] = None
    created_at: datetime
    genre: Genre


class BookUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=30, description="Book title")
    author: Optional[str] = Field(None, max_length=60, description="Book author")
    description: Optional[str] = Field(None, description="Book description")
    genre: Optional[Genre] = Field(None, description='Genre of book')

    @field_validator("title", "author")
    @classmethod
    def not_empty(cls, v: Optional[str]):
        if v is not None:
            if not v.strip():
                raise ValueError("Cannot be empty")
            return v.strip().capitalize()
        return v
