from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/v1/insights", tags=["insights"])


@router.get("/weekly")
async def weekly_summary(user_id: str = Query(...)) -> dict:
    return {
        "user_id": user_id,
        "summary": "This is a placeholder for weekly reflection summaries.",
        "themes": ["growth", "work", "life"],
        "questions": [
            "What am I repeatedly thinking about?",
            "Which of these questions deserve more attention?",
        ],
    }
