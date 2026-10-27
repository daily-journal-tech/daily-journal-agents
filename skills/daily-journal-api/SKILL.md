---
name: daily-journal-api
description: Brazilian and world news in Portuguese from Daily Journal, every story cited to the outlets that reported it (Folha, G1, UOL, Poder360, BBC, Guardian, FT, NYT, WSJ, Bloomberg, Al Jazeera). Use when the user asks about Brazilian current events — politics, Congresso, STF, Lula, eleições, economia, Petrobras, the Real, BC/Selic — wants news in Portuguese, wants to know how several outlets covered a story, or wants background on an ongoing story (a war, an election, a scandal, a public figure). Also for official figures Daily Journal keeps as datasets: Brazil's public debt, the payroll, revenue and spending of Brazilian states and capitals, retail electricity prices by country, Brazilian state and distributor, and Brazil's major physical assets (mines, oil fields, power plants, ports) with owners and output. Also when they mention Daily Journal.
---

# Daily Journal

Daily Journal (dailyjournal.news) is a Brazilian news publication in Portuguese
(pt-BR). Each story is written from several outlets' reporting and keeps the list of
those articles, so every claim can be traced to its source. Topic pages hold
evergreen background on people, institutions and ongoing stories. Datasets hold
official figures, compiled from the publishers named in each one.

## Tools

This plugin connects the Daily Journal MCP server. Six read-only tools:

| Tool | Use it for |
| --- | --- |
| `search_news` | Finding stories. No arguments = the latest news. Filters: `category`, `topic` (slug), `date_from` / `date_to` (YYYY-MM-DD), `search` (full-text, Portuguese works best), `limit`, `cursor`. |
| `get_news` | One story in full, by `slug` (not `id`): body, bullets and every source article with its URL and outlet. |
| `list_topics` | Browsing topic pages. `hot: true` returns the stories Daily Journal is following most closely right now. |
| `get_topic` | Background on one topic: summary, sections, FAQ, recent news. |
| `list_datasets` | The datasets, what each covers, its `key` format and its parameters. |
| `get_dataset` | Official figures from one dataset: the whole of it, or one entry by `key` (a country, a UF, a series group). Narrow with `path`, `where`, `fields`, `offset`, `limit`. |

If the tools are not available (connector not added, or another client), read
`references/curl-api.md` and call the same public API with `curl`. If there is no shell fallback, explain that the Daily Journal MCP connection
needs to be enabled in the host application before these tools can be used.

## Flow

0. **A figure, a count, a ranking or a series** (how much debt, which state
   spends most on payroll, the electricity price in Germany, who owns a mine) →
   `get_dataset` first, news after for what the figure means. Our news can quote
   several numbers for one fact; the dataset holds the one figure with its date.
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

Datasets come back within a 25,000-character budget. A list arrives a page of rows
at a time with `next_offset`; anything larger arrives as an `outline` of its fields
and sizes. Read `notice`: it names the next call (`path="pins"`, a `where` value
the field actually takes). Ask for the rows you need with `where` and `fields`
rather than paging through everything.

`category` takes English keys: `world`, `politics`, `economy`, `finance`,
`business`, `agribusiness`, `technology`, `science`, `sports`, `entertainment`, `brazil`.

## Coverage limits

The tools only read public news, topics and datasets. They cannot publish, edit, or retrieve
private subscriber data. Search may return partial or loosely related matches;
check relevance before claiming coverage. If there is no relevant evidence, say
so rather than inventing a story or sources.

## Answering

- Reply in the user's language. The content is in Portuguese; translate when the
  user writes in another language.
- Give dates. News moves fast and `published_at` is what tells the user how fresh it is.
- **Cite on every story you use**: link the Daily Journal `url` for the summary, and
  name the outlets (`outlets[].name`) — "segundo Folha e BBC". When quoting an
  outlet's own reporting, link its article from `sources[].url`.
- **Cite every figure from a dataset**: link its `page_url`, name the original
  publisher the data gives (Tesouro Nacional, ANEEL, Eurostat…) and the reference
  date or period.
- When outlets disagree or cover a story differently, say so; that comparison is
  what the source list is for.
- Don't present Daily Journal's synthesis as the original outlet's words, or the
  reverse.
