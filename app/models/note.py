from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

note_tag = Table(
    "note_tag",
    Base.metadata,
    Column("note_id", ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(128), index=True)

    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    source: Mapped[str] = mapped_column(String(64), default="text")
    category: Mapped[str] = mapped_column(String(64), default="reflection")
    mood: Mapped[str | None] = mapped_column(String(64), nullable=True)
    importance: Mapped[float] = mapped_column(Float, default=0.0)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    tags: Mapped[List["Tag"]] = relationship(
        secondary=note_tag,
        back_populates="notes",
        lazy="selectin",
    )


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)

    notes: Mapped[List[Note]] = relationship(
        secondary=note_tag,
        back_populates="tags",
        lazy="selectin",
    )
