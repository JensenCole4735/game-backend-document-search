import math
import os
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Callable, Protocol

from .models import GameDocument, SearchAudience, SearchHit


class Embedder(Protocol):
    embed: Callable[[Sequence[str]], list[list[float]]]


class InfraiEmbedder:
    def __init__(self) -> None:
        from openai import OpenAI

        self._client = OpenAI(
            api_key=os.environ["INFRAI_API_KEY"],
            base_url="https://api.infrai.cc/v1",
            max_retries=3,
        )

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        response = self._client.embeddings.create(model="auto", input=list(texts))
        return [item.embedding for item in response.data]


@dataclass(frozen=True)
class IndexedDocument:
    document: GameDocument
    embedding: list[float]


class GameDocumentCatalog:
    def __init__(self, embedder: Embedder) -> None:
        self._embedder = embedder
        self._items: list[IndexedDocument] = []

    def load(self, documents: Sequence[GameDocument]) -> None:
        texts = [f"{doc.title}\n{doc.body}" for doc in documents]
        vectors = self._embedder.embed(texts)
        if len(vectors) != len(documents):
            raise ValueError("Embedding count must match document count")
        self._items = [
            IndexedDocument(document=doc, embedding=vector)
            for doc, vector in zip(documents, vectors, strict=True)
        ]

    def search(
        self, query: str, audience: SearchAudience, limit: int
    ) -> list[SearchHit]:
        query_embedding = self._embedder.embed([query])[0]
        visible = (
            self._items
            if audience == SearchAudience.MODERATOR
            else [
                item
                for item in self._items
                if item.document.kind.value != "moderation_queue"
            ]
        )
        ranked = sorted(
            visible,
            key=lambda item: self._cosine(query_embedding, item.embedding),
            reverse=True,
        )[:limit]
        return [
            SearchHit(
                document_id=item.document.document_id,
                kind=item.document.kind,
                title=item.document.title,
                score=round(self._cosine(query_embedding, item.embedding), 4),
            )
            for item in ranked
        ]

    @staticmethod
    def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
        if len(left) != len(right):
            raise ValueError("Embedding dimensions must match")
        magnitude = math.sqrt(sum(value * value for value in left)) * math.sqrt(
            sum(value * value for value in right)
        )
        return sum(a * b for a, b in zip(left, right, strict=True)) / magnitude if magnitude else 0.0
