from pydantic import BaseModel, Field

from .models import SearchAudience, SearchHit


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    audience: SearchAudience
    limit: int = Field(default=3, ge=1, le=10)


class SearchResponse(BaseModel):
    hits: list[SearchHit]
