---
title: "Reviewly"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{s3c0nd-0rd3r-sqli-st0r3d-un10n}"
tags: [sql-injection, second-order-sqli, union-based, stored-injection]
---

# Reviewly

> **TL;DR:** The search box was firewalled, but the display name — stored at registration — was later placed unescaped into a query on the "my reviews" page; a UNION payload as the display name read the `secrets` table and returned the flag.

## Background (for beginners)
- **Second-order (stored) SQL injection** stores attacker input safely at one point, then uses it unescaped in a query somewhere else later.
- Defences placed only on the obvious input (a search firewall) miss the stored value's second use.
- **UNION-based** injection appends an attacker-chosen result set, letting you pull data from other tables.

## The Challenge
You make an account. The search box is blocked by a firewall, but the "my reviews" page lists reviews filed under your display name. The flag lives in a `secrets` table.

## Key Insight 💡
The firewall only guards the search box. The display name you register is stored and later interpolated straight into the "my reviews" query — a second, unprotected injection point. Registering a display name containing a single quote breaks that page, proving unescaped interpolation.

## Solution
1. Confirm the search box is firewalled (direct injection blocked). *Why: rules out the obvious path.*
2. Register a display name containing a `'` and load "my reviews" — it errors/breaks. *Why: proves the display name is placed unescaped into a DB query (a stored injection point).*
3. Set the display name to a UNION query that enumerates table names. *Why: the firewall doesn't cover this second-order path; UNION reveals the schema, exposing `secrets`.*
4. Set the display name to a UNION that reads from `secrets`, then reload "my reviews". *Why: the stored payload executes on render and returns the flag in the results.*

## Solver sketch (illustrative pseudocode)
```
register(display_name = "' UNION SELECT table_name FROM information_schema.tables-- ")
view_my_reviews()   # schema leaks here
register(display_name = "' UNION SELECT flag FROM secrets-- ")
view_my_reviews()   # flag leaks here
```

## Why It Worked (the vulnerability)
The firewall guarded only the search box, while the stored display name was concatenated into a later query without escaping — classic second-order SQLi. **Fix:** parameterise *every* query (including those that use stored values), not just the input that looks user-facing.

## Flag
```
FLAG{s3c0nd-0rd3r-sqli-st0r3d-un10n}
```

## Takeaways
- Input validated at entry can still be dangerous when reused in a later query.
- Second-order SQLi hides where stored values are read, not where they're written.
- Parameterise all queries; perimeter firewalls don't cover internal data flows.
