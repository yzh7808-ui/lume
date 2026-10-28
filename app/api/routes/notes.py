from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.note import NoteCreate, NoteRead
from app.services.note_service import NoteService

router = APIRouter(prefix="/api/v1/notes", tags=["notes"])


@router.post("", response_model=NoteRead)
async def create_note(payload: NoteCreate, db: AsyncSession = Depends(get_db)) -> NoteRead:
    service = NoteService(db)
    note = await service.create_note(payload)
    return NoteRead(
        id=note.id,
        user_id=note.user_id,
        title=note.title,
        content=note.content,
        summary=note.summary,
        source=note.source,
        category=note.category,
        mood=note.mood,
        importance=note.importance,
        is_archived=note.is_archived,
        created_at=note.created_at,
        updated_at=note.updated_at,
        tags=[tag.name for tag in note.tags],
    )


@router.get("", response_model=list[NoteRead])
async def list_notes(
    user_id: str = Query(...),
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> list[NoteRead]:
    service = NoteService(db)
    notes = await service.list_notes(user_id=user_id, skip=skip, limit=limit)
    result = []
    for note in notes:
        result.append(
            NoteRead(
                id=note.id,
                user_id=note.user_id,
                title=note.title,
                content=note.content,
                summary=note.summary,
                source=note.source,
                category=note.category,
                mood=note.mood,
                importance=note.importance,
                is_archived=note.is_archived,
                created_at=note.created_at,
                updated_at=note.updated_at,
                tags=[tag.name for tag in note.tags],
            )
        )
    return result


@router.get("/search")
async def search_notes(
    user_id: str = Query(...),
    query: str = Query(...),
    limit: int = 5,
    db: AsyncSession = Depends(get_db),
):
    service = NoteService(db)
    return service.search_similar(user_id=user_id, query=query, limit=limit)
