from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request

from .api_models import SearchRequest, SearchResponse
from .embedding_catalog import GameDocumentCatalog, InfraiEmbedder
from .starter_documents import STARTER_DOCUMENTS


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    catalog = GameDocumentCatalog(InfraiEmbedder())
    catalog.load(STARTER_DOCUMENTS)
    app.state.catalog = catalog
    yield


service = FastAPI(title="Game backend document search", lifespan=lifespan)


@service.post("/search", response_model=SearchResponse)
def search_documents(payload: SearchRequest, request: Request) -> SearchResponse:
    catalog: GameDocumentCatalog = request.app.state.catalog
    return SearchResponse(
        hits=catalog.search(payload.query, payload.audience, payload.limit)
    )
