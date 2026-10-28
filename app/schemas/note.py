from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str


class NoteCreate(BaseModel):
    user_id: str
    title: Optional[str] = None
    content: str = Field(..., min_length=1)
    source: str = "text"
    category: str = "reflection"
    mood: Optional[str] = None
    importance: float = 0.0
    tags: List[str] = []


class NoteRead(BaseModel):
    id: int
    user_id: str
    title: Optional[str]
    content: str
    summary: Optional[str]
    source: str
    category: str
    mood: Optional[str]
    importance: float
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    tags: List[str] = []

    class Config:
        from_attributes = True
