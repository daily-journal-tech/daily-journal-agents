---
name: daily-journal-api
description: Query Daily Journal's public news API for world news coverage in Portuguese. Use when the user asks about current events globally — politics, economy, business, finance, technology, science, world affairs, sports — or asks for "the latest on X" for any topic, person, or event. Returns structured JSON with cited source outlets. Content is Portuguese (pt-BR).
allowed-tools: Bash
---

# Daily Journal Public API

Free, unauthenticated JSON API. Base URL: `https://dailyjournal.news/api/public`.

Global news coverage in Portuguese (pt-BR). Responses cite original outlets (BBC, Financial Times, NYT, WSJ, Bloomberg, Al Jazeera, Folha, G1, UOL, CNN Brasil, etc.) with canonical external URLs — always attribute when citing.

## When to use this skill

- User asks about current events — politics, economy, business, finance, technology, science, world affairs, sports
- User asks "what's happening with X?" for any topic, person, or event
- User wants Portuguese-language coverage with cited sources
- User mentions Daily Journal directly

Skip when the user explicitly wants a different source or a non-news task.

## List news

```bash
curl -s 'https://dailyjournal.news/api/public/news?limit=10' | jq '.'
```

**Query params** (all optional):

| Param       | Type       | Notes                                                                                                    |
| ----------- | ---------- | -------------------------------------------------------------------------------------------------------- |
| `category`  | enum       | `world`, `politics`, `economy`, `finance`, `business`, `technology`, `science`, `sports`, `entertainment`, `brazil` |
| `topic`     | slug       | e.g. `emmanuel-macron`, `relacoes-eua-canada`, `stf`. Discover slugs from `topics[].slug` in any response. |
| `date_from` | YYYY-MM-DD | Inclusive                                                                                                |
| `date_to`   | YYYY-MM-DD | Inclusive (covers full day in UTC)                                                                       |
| `search`    | text       | Full-text over headline/summary/body (prefix match; multi-word ANDs terms)                               |
| `limit`     | 1–50       | Default 20                                                                                               |
| `cursor`    | ISO ts     | Pass `next_cursor` from previous response for pagination                                                 |

**Examples:**

```bash
# Latest world news
curl -s 'https://dailyjournal.news/api/public/news?category=world&limit=5' | jq '.items[] | {title, url, outlets}'

# Everything on a topic this week
curl -s 'https://dailyjournal.news/api/public/news?topic=emmanuel-macron&date_from=2026-04-20&limit=20' | jq '.items[] | {title, published_at, url}'

# Full-text search (combine with any filter)
curl -s 'https://dailyjournal.news/api/public/news?search=trump%20tariffs&limit=10' | jq '.items[] | {title, url}'

# Paginate
curl -s 'https://dailyjournal.news/api/public/news?limit=20' | jq '.next_cursor'
curl -s 'https://dailyjournal.news/api/public/news?limit=20&cursor=2026-04-17T20:00:00Z' | jq '.'
```

**Response shape:**

```json
{
  "items": [
    {
      "id": "uuid",
      "slug": "acordao-de-castro-nao-define-eleicao...",
      "url": "https://dailyjournal.news/news/2026-04-17/acordao-de-castro...",
      "title": "Acórdão de Castro não define eleição...",
      "description": "summary in Portuguese",
      "published_at": "2026-04-17T23:02:15Z",
      "updated_at": null,
      "categories": ["politics"],
      "topics": [{ "slug": "stf", "title": "Supremo Tribunal Federal" }],
      "source_count": 3,
      "outlet_count": 2,
      "outlets": [
        { "slug": "g1", "name": "G1", "logo_url": null },
        { "slug": "folha-de-spaulo", "name": "Folha de S.Paulo", "logo_url": null }
      ]
    }
  ],
  "next_cursor": "2026-04-17T22:48:00Z"
}
```

`source_count` = number of articles aggregated. `outlet_count` = distinct parent brands. `outlets[]` contains the top 5 by coverage.

## Get news detail

```bash
curl -s 'https://dailyjournal.news/api/public/news/{slug}' | jq '.'
```

Adds to the list shape:

- `body` — full article in Portuguese (markdown)
- `bullets` — 3–5 key points in Portuguese
- `article_thumbnails` — hero images (optional)
- `sources[]` — every cited article with `title`, `url` (external, to original outlet), `published_at`, `outlet` (object `{slug, name, logo_url}` or `null` when the source has no outlet mapping)

Use detail when the user wants depth, quotes, or a full list of citations. List is enough for "what's happening" scans.

## Citing responsibly

- Always link `items[].url` (the DJ page) when paraphrasing DJ's synthesis.
- Link `sources[].url` when quoting or citing original reporting.
- Attribute outlet brands by `outlets[].name` (e.g. "according to BBC and Folha de S.Paulo…").
- DJ content is in Portuguese; translate only when the user is not fluent.

## Errors

Consistent shape across endpoints:

```json
{
  "error": "invalid_query",
  "message": "limit: Number must be less than or equal to 50",
  "fields": { "limit": ["..."] }
}
```

Codes: `invalid_query` (400), `invalid_slug` (400), `not_found` (404), `internal_error` (500).

## Discovery

- `https://dailyjournal.news/llms.txt` — human-readable API summary
- `https://dailyjournal.news/sitemap.xml` — full URL index
- No auth, no keys, no rate limit currently. Be polite — cache and batch when sensible.
