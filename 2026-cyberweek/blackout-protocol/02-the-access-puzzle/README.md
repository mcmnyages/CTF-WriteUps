---
title: "The Access Puzzle"
event: "CyberWeek 2026"
series: "The Blackout Protocol"
category: network
difficulty: medium
points: 300
status: solved
flag: "FLAG{BP02_35C2C90A3900}"
tags: [cache-collision, auth-tag-verification, access-control, path-continuity]
---

# The Access Puzzle

> **TL;DR:** A lease cache keyed badges by a short digest, so two badges collided in one slot; tracing the single physically-continuous four-door path with verified auth tags and panel receipts reveals an intruder who borrowed another person's cached engineering access, yielding the token.

## Background (for beginners)
- A cache that indexes entries by a short digest (hash) of a key can suffer collisions: two different keys map to the same slot.
- For access control, a badge-ID collision means one person's cached role can be served for a different person's request — a silent privilege grant.
- Verifying each request's authentication tag and matching it to a physical confirmation (the door actually opened) separates real passages from log noise.
- Fix in one line: key caches by the full identifier, never a truncated digest.

## The Challenge
Reusing the Chapter 1 token unlocks a network capture, door-control logs, badge records, access leases, a flawed lease cache, and physical door-panel receipts. You must find the one real unauthorized passage. Tools: Python stdlib.

## Key Insight 💡
The lease cache indexes badges by a **short digest, not the full badge ID**, so two badges collide in one cache slot — a request can be evaluated with a **different person's cached role**.

## Solution
1. **Reuse the Chapter 1 token** to unlock this chapter's evidence. (WHY: each chapter's token unlocks the next.)
2. **Verify every request's auth tag.** (WHY: only cryptographically valid requests are real.)
3. **Match each request to a physical panel receipt** confirming the door actually opened. (WHY: a log entry without a physical confirmation is not a real passage.)
4. **Require each step to chain to the previous** one, forming a physically-continuous path. (WHY: a real intrusion is a continuous route, not scattered events.)
5. **Find the one complete four-door path** (public → restricted cage), one session and one real badge the whole way, reaching the final door in the exact window before the Chapter 1 blackout. (WHY: only the genuine passage satisfies continuity, timing, and single-identity constraints.)
6. **Observe that this path borrowed another person's cached engineering access on every hop**, then combine session/badge/step IDs with the formula for the token. (WHY: the collision is the mechanism; the formula binds it to the flag.)

## Why It Worked (the vulnerability)
The lease cache used a truncated digest as its key, so colliding badges shared a slot and an attacker's requests were evaluated with a victim's cached engineering role. **Fix:** key the cache by the full badge ID and verify identity per request.

## Flag
```
FLAG{BP02_35C2C90A3900}
```

## Takeaways
- Truncated keys cause collisions; in security contexts collisions become authorization bugs.
- Correlate digital logs with physical receipts to confirm events really happened.
- Path continuity (one session, one badge, right window) filters decoys from the real intrusion.

## Chain Note
**The Blackout Protocol** is a chained series where each chapter's token unlocks the next. Chapter 2 takes the Chapter 1 token (`FLAG{BP01_...}`) as input to unlock its evidence and outputs `FLAG{BP02_...}`, which Chapter 3 uses to unlock its firmware and audit records.
