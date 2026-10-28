from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.note import Note, Tag
from app.schemas.note import NoteCreate
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService


class NoteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.embedding_service = EmbeddingService()
        self.llm_service = LLMService()

    def _serialize_for_search(self, note: Note, score: float = 1.0):
        return {
            "id": note.id,
            "score": score,
            "payload": {
                "note_id": note.id,
                "title": note.title,
                "summary": note.summary,
                "category": note.category,
                "mood": note.mood,
                "source": note.source,
                "user_id": note.user_id,
            },
        }

    async def create_note(self, payload: NoteCreate) -> Note:
        note = Note(
            user_id=payload.user_id,
            title=payload.title or payload.content[:30],
            content=payload.content,
            source=payload.source,
            category=payload.category,
            mood=payload.mood,
            importance=payload.importance,
        )

        tag_objects = []
        for tag_name in payload.tags:
            tag_result = await self.session.execute(select(Tag).where(Tag.name == tag_name))
            tag = tag_result.scalar_one_or_none()
            if not tag:
                tag = Tag(name=tag_name)
            tag_objects.append(tag)

        note.tags = tag_objects

        summary = await self.llm_service.summarize_note(payload.content)
        extracted = await self.llm_service.extract_tags_and_mood(payload.content)

        note.summary = summary
        note.category = extracted.get("category", note.category)
        note.mood = extracted.get("mood", note.mood)

        if payload.title is None:
            note.title = f"Note-{datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"

        self.session.add(note)
        await self.session.commit()
        await self.session.refresh(note)

        self.embedding_service.upsert_note(
            note_id=note.id,
            user_id=note.user_id,
            text=note.content,
            metadata={
                "title": note.title,
                "summary": note.summary,
                "category": note.category,
                "mood": note.mood,
                "source": note.source,
            },
        )

        return note

    async def list_notes(self, user_id: str, skip: int = 0, limit: int = 20):
        result = await self.session.execute(
            select(Note)
            .where(Note.user_id == user_id)
            .order_by(Note.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_keyword(self, user_id: str, query: str, limit: int = 5):
        if not query or not query.strip():
            return []

        search_term = f"%{query.strip()}%"
        result = await self.session.execute(
            select(Note)
            .where(Note.user_id == user_id)
            .where(
                or_(
                    Note.title.ilike(search_term),
                    Note.content.ilike(search_term),
                    Note.summary.ilike(search_term),
                )
            )
            .order_by(Note.created_at.desc())
            .limit(limit)
        )
        notes = result.scalars().all()
        return [self._serialize_for_search(note, score=1.0) for note in notes]

    def search_similar(self, user_id: str, query: str, limit: int = 5):
        return self.embedding_service.search_similar(user_id=user_id, query=query, limit=limit)
