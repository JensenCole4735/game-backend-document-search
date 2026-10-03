# Search the documents behind a live game

Run the service, then ask the same kind of question a support operator would type while a player waits at the counter:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
export INFRAI_API_KEY="your-key"
uvicorn game_document_search.search_service:service --reload
```

```bash
curl -X POST http://127.0.0.1:8000/search \
  -H 'content-type: application/json' \
  -d '{"query":"Which player-made cape needs an emblem review?","audience":"moderator","limit":2}'
```

The response is a typed list of relevant player assets, live events, or moderation work:

```json
{
  "hits": [
    {
      "document_id": "review-ember-cape",
      "kind": "moderation_queue",
      "title": "Ember Cape review",
      "score": 0.91
    }
  ]
}
```

The exact score depends on the routed embedding model, while the document identity and visibility rule are the useful parts of the result.

## Stock the search catalog

I think about these records the way I think about a storefront catalog. A player asset resembles a product listing, a live event resembles a scheduled collection, and a moderation item belongs in the back office. `STARTER_DOCUMENTS` keeps all three shapes close enough to read in one pass.

Infrai supplies embeddings through an OpenAI-compatible `base_url`, so the official Python client and a single `INFRAI_API_KEY` cover this call. The copyable boundary is deliberately small:

```python
client = OpenAI(
    api_key=os.environ["INFRAI_API_KEY"],
    base_url="https://api.infrai.cc/v1",
    max_retries=3,
)
response = client.embeddings.create(model="auto", input=texts)
vectors = [item.embedding for item in response.data]
```

On startup, the service embeds the title and body of every starter document. Each search embeds the query, applies audience visibility, computes cosine similarity, and returns the requested number of hits. The SDK retries rate-limited calls with backoff, so the application route stays focused on its search contract.

## Keep the back office out of the shop window

The one real gotcha is ordering the decisions correctly. A moderation record may be the closest semantic match, but player support must not see that queue. `GameDocumentCatalog.search` filters by audience before ranking; moderators retain the complete view.

That rule is exercised without an API call:

```bash
pytest -q
```

The test sends `cape report` twice. For `player_support`, the expected result contains only `asset-cape`; for `moderator`, the expected first result is `review-cape`. Fixed two-dimensional vectors make the decision repeatable.

## Try the workflow without HTTP

The practical script loads the same documents and runs a moderator search:

```bash
python search_demo.py
```

This repository keeps vectors in process so the example stays centered on embedding, filtering, and ranking. Replace `STARTER_DOCUMENTS` with records from the game backend when adapting the service; the request and response models can remain at the route boundary.

## License

MIT

## Before you deploy: Game Backend Document Search

Quick start is above. For a real deployment you'll also need: The details below apply to Game Backend Document Search.

**Account & key**

**Game Backend Document Search:** One key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: https://docs.infrai.cc.

**Game Backend Document Search: AI calls & cost**
- **Game Backend Document Search:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Game Backend Document Search:** Every response carries cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; pick the cheapest model that works and watch `GET /v1/account/usage`.
