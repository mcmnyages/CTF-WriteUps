---
title: "DeskNest"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{st0r3d-xss-4g3nt-h1j4ck}"
tags: [stored-xss, filter-bypass, iframe-srcdoc, session-hijack]
---

# DeskNest

> **TL;DR:** A support ticket allowed HTML; an `iframe srcdoc` with HTML-encoded `<script>` tags bypassed the sanitiser and ran in the support agent's privileged browser, which called the admin-only release-token link and wrote the real flag back onto the ticket.

## Background (for beginners)
- **Stored XSS** is when attacker-supplied script is saved by the server and later executed in another user's browser when they view the content.
- It is dangerous because the script runs with the *victim's* privileges and session, not the attacker's.
- Naive sanitisers blocklist obvious vectors (plain `<script>`, `onclick=`) but miss alternate execution contexts.
- An `<iframe srcdoc="...">` holds a whole HTML document inside an attribute; HTML entities inside it are decoded and the markup runs when the iframe loads.

## The Challenge
You register a normal account and open a support ticket. A support agent opens every new ticket in a real browser to review it. The flag sits behind an admin-only "release token" link; as a normal user that link returns only a fake flag, so a privileged user must trigger it. Ticket messages allow HTML.

## Key Insight 💡
The sanitiser stripped event-handler attributes and plain script tags, but it did not decode and re-inspect the contents of an `iframe srcdoc`. HTML-encoded tags inside `srcdoc` are decoded by the browser at render time, so the hidden script survives sanitisation yet still executes.

## Solution
1. Register an account and confirm ticket messages render HTML. *Why: establishes the stored sink.*
2. Test plain `<script>` and `onerror=` — both stripped. *Why: maps the blocklist.*
3. Craft a ticket body containing an `<iframe srcdoc="...">` whose inner `<script>` tags are HTML-entity encoded. *Why: the encoded markup isn't recognised as script by the filter but is decoded and run by the browser.*
4. Inside that script, call the admin-only release-token endpoint to read the real flag, then POST it as an internal note back onto your own ticket. *Why: exfiltrates the privileged result to a place you can read.*
5. Wait for the agent to review the ticket, then open your ticket and read the note. *Why: the agent's privileged browser executed the payload.*

## Why It Worked (the vulnerability)
The HTML sanitiser was a blocklist that never normalised/decoded nested `srcdoc` content, allowing script execution in the reviewer's privileged session (stored XSS → agent/session hijack). **Fix:** use an allowlist-based sanitiser (e.g. a vetted library), forbid `iframe`/`srcdoc`, and serve user content under a strict Content-Security-Policy.

## Flag
```
FLAG{st0r3d-xss-4g3nt-h1j4ck}
```

## Takeaways
- Stored XSS turns any privileged viewer into your proxy — target the person who reads the data.
- Blocklist sanitisers fail on alternate execution contexts like `srcdoc` and HTML-encoded payloads.
- Allowlist sanitisation + CSP, not keyword stripping, is the real fix.
