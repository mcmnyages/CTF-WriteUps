---
title: "Gateway"
event: "CyberWeek 2026"
series: "Together"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{sql1-un10n-l00t-th3-g4t3w4y}"
tags: [sql-injection, union-based, sqlite, string-concat]
---

# Gateway

> **TL;DR:** The parts-search API concatenated user text directly into a SQLite query; a UNION injection dumped a hidden `secrets` table holding the flag and the next portal's login.

## Background (for beginners)
- SQL injection happens when user input is pasted into a database query as code instead of being treated as data.
- A single quote (`'`) breaks out of a string literal; if the app crashes or leaks the query, injection is confirmed.
- UNION-based injection appends attacker-controlled rows to legitimate results, letting you read other tables.
- Fix in one line: use parameterized queries (prepared statements), never string concatenation.

## The Challenge
The first portal of the Together chain is a parts-catalog site with a search box. The search text is sent to an API that builds its database query by pasting the text straight in. Tools needed: just a browser.

## Key Insight 💡
A single quote in the search box produced an error that **printed the query itself** — proof the input lands inside the SQL, and that the backend is SQLite.

## Solution
1. **Probe with `'`** — the error echoed the raw query, confirming string-concatenation SQLi against SQLite. (WHY: an error that reflects the query is the clearest injection signal.)
2. **Enumerate tables via UNION** — a UNION injection listed the schema's tables, revealing a hidden table named `secrets`. (WHY: UNION lets you pull data from tables the UI never intended to expose.)
3. **Dump `secrets`** — selecting its rows returned the flag plus the login credentials for Portal 2 (Mailer). (WHY: the chain hands each portal the next portal's login.)

## Why It Worked (the vulnerability)
The API built SQL by concatenating raw user text, so input was parsed as query logic. **Fix:** use parameterized/prepared statements so input is always bound as data.

## Flag
```
FLAG{sql1-un10n-l00t-th3-g4t3w4y}
```

## Takeaways
- An error that reflects the query is a gift — it tells you the dialect and the injection point at once.
- Hidden tables are often named obviously (`secrets`); always enumerate the schema first.
- Parameterized queries defeat this entire class of bug.

## Chain Note
**Together** is a 5-portal chain where each portal hands over the next portal's login. Gateway takes nothing in (it is the entry point) and outputs the flag plus Portal 2 (Mailer) credentials dumped from the `secrets` table.
