from game_document_search.embedding_catalog import GameDocumentCatalog, InfraiEmbedder
from game_document_search.models import SearchAudience
from game_document_search.starter_documents import STARTER_DOCUMENTS


def main() -> None:
    catalog = GameDocumentCatalog(InfraiEmbedder())
    catalog.load(STARTER_DOCUMENTS)
    hits = catalog.search(
        query="Which player-made cape needs an emblem review?",
        audience=SearchAudience.MODERATOR,
        limit=2,
    )
    for hit in hits:
        print(f"{hit.score:.4f}  {hit.kind.value:18}  {hit.title}")


if __name__ == "__main__":
    main()
