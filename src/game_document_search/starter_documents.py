from .models import DocumentKind, GameDocument


STARTER_DOCUMENTS = [
    GameDocument(
        document_id="asset-ember-cape",
        kind=DocumentKind.PLAYER_ASSET,
        title="Ember Cape submission",
        body="Player-made crimson cape with animated sparks, submitted for the avatar shop.",
    ),
    GameDocument(
        document_id="event-moon-market",
        kind=DocumentKind.LIVE_EVENT,
        title="Moon Market weekend",
        body="Limited-time night market with crafting quests and double guild tokens.",
    ),
    GameDocument(
        document_id="review-ember-cape",
        kind=DocumentKind.MODERATION_QUEUE,
        title="Ember Cape review",
        body="Moderation review for the player-made cape due to a reported emblem.",
    ),
]
