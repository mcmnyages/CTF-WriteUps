---
title: "Rolodex"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: easy
points: 150
status: solved
flag: "FLAG{r0l0d3x-bl1nd-n0sql-0racl3}"
tags: [nosql-injection, operator-injection, boolean-based, blind-injection]
---

# Rolodex

> **TL;DR:** The search box sent a raw database filter to the server. An empty filter dumped every record (including a hidden service account), and a boolean "oracle" let us extract its API key one character at a time — blind NoSQL injection.

## Background (for beginners)
- **NoSQL injection** happens when user input is placed directly into a database query/filter. In document databases, attackers can smuggle **operators** (like "greater than" or "matches regex") instead of plain values.
- A **blind** injection gives no direct output, only a yes/no signal (record found vs. not). That signal is an **oracle** you can query repeatedly.
- **Boolean-based extraction** asks "is character N greater than X?" style questions to rebuild a secret bit by bit.
- Dangerous because it bypasses auth and exfiltrates hidden fields even when nothing is printed.

## The Challenge
A contacts app with a search box. The box forwards a **raw filter** to the backend database unrestricted. Tooling: `curl`, Python.

## Key Insight 💡
Submitting an **empty filter** returned *every* record — including a hidden service account that carried a secret API key field. The search was passing attacker-controlled query operators straight to the database.

## Solution
1. **Send an empty/permissive filter** to confirm the search returns all records, exposing the hidden service account and the existence of its API key field. *Why:* establishes that the filter is attacker-controlled and that a target secret exists.
2. **Craft boolean filter conditions** (operator injection) that are true only when a given character of the API key matches a guess. *Why:* turns "record returned or not" into a yes/no oracle.
3. **Automate the oracle in Python**, looping over each position and each candidate character, keeping the character whose filter returns the record. *Why:* blind extraction requires many scripted yes/no queries.
4. **Reassemble the extracted characters** into the full API key / flag. *Why:* concatenating each confirmed character yields the secret.

## Why It Worked (the vulnerability)
User input was interpreted as database **query operators** rather than a literal search value, so attackers controlled the filter logic. **Fix:** never pass raw user input as a query object; cast inputs to plain strings, validate types, and use a strict query schema.

## Flag
```
FLAG{r0l0d3x-bl1nd-n0sql-0racl3}
```

## Takeaways
- **Pattern:** raw user input used as a DB filter enables operator injection.
- **Spotting it:** try an empty filter and operator-style payloads; watch for all-records or boolean differences.
- **Fixing it:** enforce input types, reject operator objects, and parameterize queries.
