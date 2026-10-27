---
name: topico
description: Explain a person, institution, or ongoing news story using Daily Journal topic pages when the user wants background or a timeline.
---

Explain a subject using Daily Journal's topic pages. Read the bundled [daily-journal-api skill](../daily-journal-api/SKILL.md) for the tools and citation rules.

Subject: the subject requested by the user.

1. If the subject is empty, call `list_topics` with `hot: true` and offer the list.
   Stop there.
2. Find the slug. Call `search_news` with the subject (in Portuguese) as `search`
   and `limit: 10`, then look at `topics[].slug` on the results. If nothing
   matches, page through `list_topics`. Slugs look like `eleicoes-brasileiras-2026`
   or `guerra-do-ira`. If there is no topic page, say so and answer from the news
   items alone.
3. Call `get_topic` with the slug and `news_limit: 5`. Large topics come back
   trimmed: read `sections_notice` and fetch only the sections the question needs
   (`sections: ["<type>"]`), usually `situacao-atual-*`, `linha-do-tempo` or
   `principais-atores`. Don't fetch them all.
4. Compare the topic's `last_updated_at` with the dates in `recent_news`. If the
   news is newer, the page doesn't know the latest developments: call `get_news`
   (by `slug`) on the one or two most recent items that bear on the question and
   take the current state from them.
5. Output: what it is, in two or three sentences; how it got here, as a short
   dated timeline; where it stands now; the latest two or three news items with
   dates and links. Link the topic page (its `url`) at the top. If the user asked
   something specific, answer that first and keep the rest short.

Reply in the user's language.
