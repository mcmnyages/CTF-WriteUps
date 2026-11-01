---
title: "The Broken Handshake"
event: "The Great CTF Debrief 2026"
series: "The Blackout Protocol"
category: rev
difficulty: medium
points: 400
status: solved
flag: "FLAG{BP03_8CD2027966B9}"
tags: [reverse-engineering, auth-downgrade, replay-attack, challenge-response]
---

# The Broken Handshake

> **TL;DR:** The legacy recovery login reads the wrong part of the conversation, skipping the replay-counter recheck; reversing the firmware and hand-simulating each candidate finds the one stale-counter replay the device accepted, yielding the token.

## Background (for beginners)
- A challenge-response handshake proves identity: the server asks a fresh question (challenge) and the client must answer it, usually with a counter to prevent replays.
- A replay attack resends a previously valid answer; a replay counter (nonce) is what stops it — if a code path skips that check, old answers work again.
- An authentication downgrade occurs when a weaker "legacy" or "recovery" mode can be selected, bypassing the stronger path's checks.
- Reverse engineering firmware means decoding/disassembling it to compare how two code paths actually behave.

## The Challenge
The Chapter 2 token unlocks a scrambled firmware image, shuffled network-audit records of remote-login handshakes, and controller telemetry receipts. Tools: Python stdlib.

## Key Insight 💡
The firmware's two login programs differ by **one step**: the legacy recovery check reads the **wrong piece of the conversation**, so it never re-checks the question just asked — a stale answer passes.

## Solution
1. **Unlock with the Chapter 2 token**, then decode the scrambled firmware image. (WHY: each chapter's token unlocks the next; the image must be un-scrambled to read.)
2. **Disassemble both programs** — the normal login check and the legacy recovery check — and diff them. (WHY: the vulnerability is a single differing step between the two.)
3. **Identify the flaw:** the legacy path reads the wrong stored value and never re-validates the current challenge, skipping the replay-counter check. (WHY: this is what allows a replayed, stale answer.)
4. **Filter sessions** to the right window with a valid signed record chain and confirmed receipts. (WHY: only genuine, in-window sessions are candidates.)
5. **Among the remaining visitor-level legacy-mode logins** (each using a stale counter and answering a different question than asked), **hand-simulate the legacy program per candidate**; only one produces the exact answer the device accepted. (WHY: simulating the buggy logic pinpoints the real replay.)
6. **Combine that session's IDs and VM trace with the formula** for the token. (WHY: the formula binds the proven replay to the flag.)

## Why It Worked (the vulnerability)
The legacy recovery mode was a downgrade path: it validated against the wrong stored value and skipped the replay-counter recheck, so a stale, previously-valid answer could be replayed. **Fix:** remove/disable legacy downgrade paths and enforce the replay-counter check on every authentication mode.

## Flag
```
FLAG{BP03_8CD2027966B9}
```

## Takeaways
- Legacy/recovery code paths are frequent downgrade vulnerabilities — audit them as closely as the main path.
- A one-instruction difference (reading the wrong value) can defeat replay protection entirely.
- Hand-simulating the actual bytecode beats guessing when many sessions look similar.

## Chain Note
**The Blackout Protocol** is a chained series where each chapter's token unlocks the next. Chapter 3 takes the Chapter 2 token (`FLAG{BP02_...}`) as input to unlock its firmware and records, and outputs `FLAG{BP03_...}`, which Chapter 4 uses to unlock its evidence set.
