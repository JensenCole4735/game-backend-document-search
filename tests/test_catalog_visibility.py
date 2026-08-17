from collections.abc import Sequence

from game_document_search.embedding_catalog import GameDocumentCatalog
from game_document_search.models import DocumentKind, GameDocument, SearchAudience


class FixedEmbedder:
    vectors = {
        "Public cape\nA player-made cape in the item shop.": [0.8, 0.2],
        "Cape review\nA reported cape waiting for moderator review.": [1.0, 0.0],
        "cape report": [1.0, 0.0],
    }

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self.vectors[text] for text in texts]


def test_support_search_hides_moderation_queue_even_when_it_is_best_match() -> None:
    catalog = GameDocumentCatalog(FixedEmbedder())
    catalog.load(
        [
            GameDocument(
                document_id="asset-cape",
                kind=DocumentKind.PLAYER_ASSET,
                title="Public cape",
                body="A player-made cape in the item shop.",
            ),
            GameDocument(
                document_id="review-cape",
                kind=DocumentKind.MODERATION_QUEUE,
                title="Cape review",
                body="A reported cape waiting for moderator review.",
            ),
        ]
    )

    support_hits = catalog.search("cape report", SearchAudience.PLAYER_SUPPORT, 2)
    moderator_hits = catalog.search("cape report", SearchAudience.MODERATOR, 2)

    assert [hit.document_id for hit in support_hits] == ["asset-cape"]
    assert moderator_hits[0].document_id == "review-cape"
