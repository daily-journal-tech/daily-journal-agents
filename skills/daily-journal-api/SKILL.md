---
name: daily-journal-api
description: Brazilian and world news in Portuguese from Daily Journal, every story cited to the outlets that reported it (Folha, G1, UOL, Poder360, BBC, Guardian, FT, NYT, WSJ, Bloomberg, Al Jazeera). Use when the user asks about Brazilian current events — politics, Congresso, STF, Lula, eleições, economia, Petrobras, the Real, BC/Selic — wants news in Portuguese, wants to know how several outlets covered a story, or wants background on an ongoing story (a war, an election, a scandal, a public figure). Also when they mention Daily Journal.
---

# Daily Journal

Daily Journal (dailyjournal.news) is a Brazilian news publication in Portuguese
(pt-BR). Each story is written from several outlets' reporting and keeps the list of
those articles, so every claim can be traced to its source. Topic pages hold
evergreen background on people, institutions and ongoing stories.

## Tools

This plugin connects the Daily Journal MCP server. Four read-only tools:

| Tool | Use it for |
| --- | --- |
| `search_news` | Finding stories. No arguments = the latest news. Filters: `category`, `topic` (slug), `date_from` / `date_to` (YYYY-MM-DD), `search` (full-text, Portuguese works best), `limit`, `cursor`. |
| `get_news` | One story in full, by `slug` (not `id`): body, bullets and every source article with its URL and outlet. |
| `list_topics` | Browsing topic pages. `hot: true` returns the stories Daily Journal is following most closely right now. |
| `get_topic` | Background on one topic: summary, sections, FAQ, recent news. |

If the tools are not available (connector not added, or another client), read
`references/curl-api.md` and call the same public API with `curl`. On claude.ai and
in Cowork, the connector is added from the plugin's **Connectors** tab; mention that
to the user if the tools are missing and there is no shell to fall back on.

## Flow

1. **What's happening with X** → `search_news` with `search` (or `topic` if you
   already know the slug). Scan titles and descriptions. Search in Portuguese:
   `tarifas trump`, not `trump tariffs`.
2. **Depth, quotes or "who reported this"** → `get_news` on the one or two stories
   that matter. List results carry only the top outlets; `sources[]` in the detail
   has every article.
3. **Background, "explain", "what is", "how did we get here"** → `get_topic`. Topic
   slugs come from `topics[].slug` on any news item, or from `list_topics`.
4. **Big topics** come back trimmed to a 25k-character budget. Every section is
   listed with its size; read `sections_notice` and call `get_topic` again with
   `sections: ["<type>"]` for the part the user asked about. Don't fetch every
   section of a large topic.

`category` takes English keys: `world`, `politics`, `economy`, `finance`,
`business`, `technology`, `science`, `sports`, `entertainment`, `brazil`.

## Answering

- Reply in the user's language. The content is in Portuguese; translate when the
  user writes in another language.
- Give dates. News moves fast and `published_at` is what tells the user how fresh it is.
- **Cite on every story you use**: link the Daily Journal `url` for the summary, and
  name the outlets (`outlets[].name`) — "segundo Folha e BBC". When quoting an
  outlet's own reporting, link its article from `sources[].url`.
- When outlets disagree or cover a story differently, say so; that comparison is
  what the source list is for.
- Don't present Daily Journal's synthesis as the original outlet's words, or the
  reverse.
