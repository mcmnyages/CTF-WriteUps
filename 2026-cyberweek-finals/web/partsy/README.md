---
title: "Partsy"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{bl1nd-sql1-0r4cl3-dr1p}"
tags: [sql-injection, blind-sqli, waf-bypass, boolean-oracle]
---

# Partsy

> **TL;DR:** A parts search was blind-SQL-injectable behind a WAF that blocked keywords and spaces; replacing spaces with inline comments and building spaces via `CHAR()` bypassed the filter, and a boolean true/false oracle dripped out table names and the licensing data.

## Background (for beginners)
- **Blind boolean SQL injection** extracts data by asking the database yes/no questions and observing which answer the app returns, without ever seeing error text or raw data.
- **WAFs** often blocklist attack keywords and spaces; both are routinely bypassable.
- Spaces can be replaced with inline comments (`/**/`) and generated from character codes (`CHAR(32)`), avoiding literal blocked tokens.

## The Challenge
The parts search box sends a name the server looks up in a DB. A filter blocks common attack words *and any space character*, returning a fake flag when triggered. The real flag lives in licensing data in the database.

## Key Insight 💡
The filter blocks literal spaces and keywords, but SQL doesn't need literal spaces: `/**/` substitutes for whitespace, and `CHAR()` builds characters (including spaces) inside strings. A safe boolean comparison lets you distinguish true from false in the normal response without tripping the filter.

## Solution
1. Confirm the search queries a DB and that spaces/keywords trigger the decoy. *Why: maps the injection point and the WAF.*
2. Replace every space with an empty inline comment `/**/` and build any needed space characters with a character-code function. *Why: removes literal spaces/keywords so the WAF never matches.*
3. Use a boolean comparison that returns normal results on TRUE and nothing (or different output) on FALSE. *Why: creates a reliable yes/no oracle.*
4. Ask one bit at a time: enumerate table names, then the licensing table's columns, then its row contents. *Why: blind extraction proceeds character-by-character via the oracle.*
5. Reassemble the leaked licensing contents into the flag. *Why: that's where the real flag is stored.*

## Solver sketch (illustrative pseudocode)
```
for each position i, candidate char c:
    payload = inject(" AND SUBSTRING(secret,i,1)=CHAR(code_of_c) ")  # spaces -> /**/
    if response == TRUE_marker: keep c
```

## Why It Worked (the vulnerability)
User input was concatenated into SQL, and the only defence was a keyword/space blocklist defeated by comment-for-space and `CHAR()`. **Fix:** use parameterised queries; a WAF is not a substitute for prepared statements.

## Flag
```
FLAG{bl1nd-sql1-0r4cl3-dr1p}
```

## Takeaways
- Blind SQLi needs only a single observable true/false difference to leak everything.
- Space/keyword WAFs fall to `/**/` and `CHAR()`-built characters.
- Parameterise queries; blocklists only slow attackers down.
