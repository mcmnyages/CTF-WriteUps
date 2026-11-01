---
title: "NestedRequest"
event: "CyberWeek 2026"
series: "Kivuli (cwa2026 finals)"
category: web
difficulty: advanced
points: 500
status: solved
flag: "FLAG{cwa2026_finals_ssrf_r3binding_bypass}"
tags: [ssrf, url-parser-confusion, allowlist-bypass, path-traversal]
---

# NestedRequest

> **TL;DR:** A URL-parser mismatch (a backslash before `@`) makes the allowlist check see an approved domain while the HTTP client connects to an internal host, enabling SSRF to a hidden internal page.

## Background (for beginners)
- **SSRF (Server-Side Request Forgery)** tricks a server into making requests on the attacker's behalf — often to internal services the attacker can't reach directly.
- **Allowlist bypasses** happen when the security check and the actual fetch **parse the URL differently** (parser confusion).
- In `http://approved.com\@internal/`, one parser reads the host as `approved.com` (before the `\`), another as `internal` (after the `@`) — the two disagree.
- **Path traversal (`../`)** can normalize/clean a request path to reach a specific internal endpoint.

## The Challenge
A service fetches any URL the user supplies but only permits three approved feed domains and blocks internal addresses. The goal is to reach an internal secret page.

## Key Insight 💡
The safety check and the real HTTP client parsed the host differently; a backslash before an `@` split them — the check saw an approved domain, the fetcher connected to the host written before the backslash.

## Solution
1. **Probed the fetcher**: it allows only three approved feed domains and blocks internal addresses.
2. **Found the parser confusion**: a `\` before an `@` made the allowlist validator see an approved domain while the HTTP library connected elsewhere — bypassing the check.
3. **Pointed the fetch inward** to the server's internal network and scanned, discovering a hidden internal service on a neighbouring address.
4. **Added a `../` sequence** to normalize the path and land on the internal secret page.
5. **Retrieved the flag** from that page.

## Why It Worked (the vulnerability)
Two components parsed the same URL differently, so passing the allowlist did not guarantee the same destination was fetched. *Defensive fix:* use a single, strict URL parser for both validation and fetching, and resolve/deny internal IP ranges after parsing.

## Flag
```
FLAG{cwa2026_finals_ssrf_r3binding_bypass}
```

## Takeaways
- SSRF allowlists fail when validation and fetch don't share one parser — never validate a string you re-parse later.
- Watch for `@`, `\`, and `../` tricks in URL handling; canonicalize before deciding.

## Chain Note
Kivuli stage 5. The Kivuli set is numbered with gaps (stages 1, 5, 7, 8 here; others exist in the wider finals). **Produced for the chain:** `signing_fragment = deadbeef12345678`, consumed later by Kivuli 8 (PaddingOracle).
