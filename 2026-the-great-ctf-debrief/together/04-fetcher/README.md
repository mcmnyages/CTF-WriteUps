---
title: "Fetcher"
event: "The Great CTF Debrief 2026"
series: "Together"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{ssrf-h1ts-th3-1ntr4n3t}"
tags: [ssrf, loopback, port-scan, localhost-bypass]
---

# Fetcher

> **TL;DR:** A URL-preview feature fetched any URL server-side; pointing it at loopback (and port-scanning to find the real internal service) reached a localhost-only `/internal/handoff` page holding the stage flag and the final portal's login.

## Background (for beginners)
- Server-Side Request Forgery (SSRF) is tricking a server into making requests on your behalf, often to places you cannot reach directly.
- Internal services frequently trust "requests from localhost," so an SSRF that originates on the server bypasses that trust boundary.
- The public-facing port is not always the internal port; attackers scan loopback ports to find the real service.
- Fix in one line: validate and allowlist outbound fetch targets, and block loopback/private ranges.

## The Challenge
Stage 4 of 5 in the Together chain. After working through the earlier portals (P1 SQLi, P2 SSTI, P3 JWT `none`) to obtain the Fetcher login, you find a feature that previews any URL by fetching it **server-side**. An `/internal/handoff` endpoint is only allowed from localhost. Tools: curl, Python.

## Key Insight 💡
Because the server itself issues the fetch, a request aimed at **loopback** appears to come from localhost — but the public port did not answer internally, so the real service had to be found by scanning local ports.

## Solution
1. **Log in to Fetcher** with the credentials carried from Portal 3. (WHY: the chain hands each portal the next login.)
2. **Point the preview at loopback** to abuse the server as a proxy into the intranet. (WHY: the `/internal/handoff` page trusts localhost-origin requests.)
3. **Scan local ports** because the public port did not answer internally; identify the port where the real internal service listens. (WHY: internal and public ports differ; you must locate the live service.)
4. **Fetch the internal handoff page** on that port, returning the stage flag plus the final portal (Core) login. (WHY: the gated page holds the handoff credentials.)

## Why It Worked (the vulnerability)
The preview fetched arbitrary URLs server-side with no destination restrictions, so loopback-only services became reachable through the server. **Fix:** allowlist outbound targets and deny requests to loopback and private/internal address ranges.

## Flag
```
FLAG{ssrf-h1ts-th3-1ntr4n3t}
```

## Takeaways
- "It only accepts requests from localhost" is not a defense when the server can be made to originate the request.
- Always port-scan loopback during SSRF — the useful service is rarely on the obvious public port.
- Allowlisting and blocking internal ranges stop SSRF at the source.

## Chain Note
**Together** is a 5-portal chain where each portal hands over the next portal's login. Fetcher receives Portal 3's handoff credentials as input and outputs the stage flag plus the final Portal 5 (Core) login, read from the localhost-only `/internal/handoff` page via SSRF.
