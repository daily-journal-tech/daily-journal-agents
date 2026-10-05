---
description: Daily news briefing from Daily Journal — today's main stories with dates, links and the outlets behind each one
argument-hint: "[category or subject, e.g. economia, politics, eleições]"
---

Give the user a news briefing from Daily Journal. Follow the `daily-journal-api`
skill for the tools and citation rules.

Scope: $ARGUMENTS

1. If the scope is empty, call `search_news` with no filters and `limit: 30`. If it
   names a category (`world`, `politics`, `economy`, `finance`, `business`,
   `technology`, `science`, `sports`, `entertainment`, `brazil`, or the Portuguese
   equivalent), pass it as `category`. Anything else goes in `search`, in Portuguese.
2. Keep what was published in the last 24 hours. If that leaves fewer than five
   stories, widen to 48 hours and say so.
3. Group stories on the same event into one item. Rank by importance, using
   `outlet_count` as a signal: a story many outlets covered usually matters more.
4. For the top three, call `get_news` with each item's `slug` and use the bullets
   for one or two sentences of substance each.
5. Output 5–8 items, most important first. Each item: a bold one-line headline,
   one or two sentences on what happened, then the date, the Daily Journal link and
   the outlets ("Folha, G1, BBC"). Close with one line naming any topic page worth
   opening for background (`topics[].slug` → dailyjournal.news/topics/<slug>).

Reply in the user's language. No preamble.
