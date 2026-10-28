import hashlib
import logging
from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

logger = logging.getLogger("lume")


class EmbeddingService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = QdrantClient(
            host=self.settings.qdrant_host,
            port=self.settings.qdrant_port,
        )
        self.model = None
        try:
            self.model = SentenceTransformer(self.settings.embedding_model)
            logger.info("Loaded embedding model: %s", self.settings.embedding_model)
        except Exception as exc:  # pragma: no cover - runtime dependency
            logger.warning("Embedding model unavailable; falling back to deterministic vector: %s", exc)

    def ensure_collection(self) -> None:
        try:
            self.client.get_collection(self.settings.qdrant_collection)
        except Exception:
            try:
                self.client.create_collection(
                    collection_name=self.settings.qdrant_collection,
                    vectors_config=VectorParams(
                        size=768,
                        distance=Distance.COSINE,
                    ),
                )
            except Exception as exc:  # pragma: no cover
                logger.warning("Could not initialize Qdrant collection: %s", exc)

    def embed_text(self, text: str) -> List[float]:
        if self.model is not None:
            try:
                vector = self.model.encode(text, normalize_embeddings=True)
                return vector.tolist()
            except Exception as exc:  # pragma: no cover
                logger.warning("SentenceTransformer encode failed, using fallback vector: %s", exc)

        # Deterministic fallback so note creation still works without external embedding model.
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # produce 768-dim vector using the digest bytes repeated and normalized
        vec = []
        for i in range(768):
            byte = digest[i % len(digest)]
            vec.append((byte / 255.0) * 2.0 - 1.0)
        norm = (sum(x * x for x in vec) ** 0.5) or 1.0
        return [x / norm for x in vec]

    def upsert_note(self, note_id: int, user_id: str, text: str, metadata: Dict[str, Any]) -> None:
        try:
            self.ensure_collection()
            vector = self.embed_text(text)
            payload = {"note_id": note_id, "user_id": user_id, **metadata}
            self.client.upsert(
                collection_name=self.settings.qdrant_collection,
                points=[
                    PointStruct(
                        id=f"{user_id}:{note_id}",
                        vector=vector,
                        payload=payload,
                    )
                ],
            )
        except Exception as exc:  # pragma: no cover
            logger.warning("Qdrant upsert failed for note %s: %s", note_id, exc)

    def search_similar(self, user_id: str, query: str, limit: int = 5):
        try:
            query_vector = self.embed_text(query)
            return self.client.search(
                collection_name=self.settings.qdrant_collection,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
                query_filter={"must": [{"key": "user_id", "match": {"value": user_id}}]},
            )
        except Exception as exc:  # pragma: no cover
            logger.warning("Qdrant search failed: %s", exc)
            return []
