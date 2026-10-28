from typing import Any, Dict, List

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


class EmbeddingService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = QdrantClient(
            host=self.settings.qdrant_host,
            port=self.settings.qdrant_port,
        )
        self.model = SentenceTransformer(self.settings.embedding_model)

    def ensure_collection(self) -> None:
        try:
            self.client.get_collection(self.settings.qdrant_collection)
        except Exception:
            self.client.create_collection(
                collection_name=self.settings.qdrant_collection,
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance.COSINE,
                ),
            )

    def embed_text(self, text: str) -> List[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def upsert_note(self, note_id: int, user_id: str, text: str, metadata: Dict[str, Any]) -> None:
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

    def search_similar(self, user_id: str, query: str, limit: int = 5):
        query_vector = self.embed_text(query)
        return self.client.search(
            collection_name=self.settings.qdrant_collection,
            query_vector=query_vector,
            limit=limit,
            with_payload=True,
            query_filter={"must": [{"key": "user_id", "match": {"value": user_id}}]},
        )
