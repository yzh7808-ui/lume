from typing import Any, Dict

from app.core.config import get_settings


class LLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def summarize_note(self, text: str) -> str:
        if not text:
            return ""
        return text[:200]

    async def extract_tags_and_mood(self, text: str) -> Dict[str, Any]:
        return {
            "themes": ["life", "work"],
            "mood": "neutral",
            "keywords": ["growth", "reflection"],
            "category": "reflection",
        }
