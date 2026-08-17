from dataclasses import dataclass
from enum import StrEnum


class DocumentKind(StrEnum):
    PLAYER_ASSET = "player_asset"
    LIVE_EVENT = "live_event"
    MODERATION_QUEUE = "moderation_queue"


class SearchAudience(StrEnum):
    PLAYER_SUPPORT = "player_support"
    MODERATOR = "moderator"


@dataclass(frozen=True)
class GameDocument:
    document_id: str
    kind: DocumentKind
    title: str
    body: str


@dataclass(frozen=True)
class SearchHit:
    document_id: str
    kind: DocumentKind
    title: str
    score: float
