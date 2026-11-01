---
title: "The First Alert"
event: "The Great CTF Debrief 2026"
series: "The Blackout Protocol"
category: forensics
difficulty: basic
points: 200
status: solved
flag: "FLAG{BP01_E39F35ADE250}"
tags: [log-correlation, clock-drift, integrity-chain, decoy-rejection]
---

# The First Alert

> **TL;DR:** After correcting every host's clock via sync beacons, cryptographically verify a full chain (unauthorized access grant → control message → delivery receipt → outage sensor reading) and pick the earliest corrected-timestamp chain, rejecting decoys, to derive the token.

## Background (for beginners)
- Raw log timestamps across different hosts cannot be trusted — each host's clock drifts, so you must correct them to a common reference before ordering events.
- Matching record IDs alone is weak evidence; attackers (and noise) can produce IDs that look related. Independent cryptographic integrity stamps confirm records are genuine.
- A real incident shows a complete, ordered chain across independent sources, not a single suspicious line.
- Technique lesson: correlate multi-source evidence, correct clock drift first, then verify integrity to separate the real event from decoys.

## The Challenge
You are given logs: remote-access grants, control messages, delivery receipts, sensor readings confirming an outage, and a clock-offset note. Several chains look like "the" incident. Tools: Python stdlib.

## Key Insight 💡
The earliest incident can only be found **after** fixing clock drift and **after** requiring an independent cryptographic chain — matching IDs by themselves are not enough to pick the real one from the decoys.

## Solution
1. **Correct every host clock** using the sync beacons before anything else. (WHY: raw timestamps are untrustworthy; ordering on them would pick the wrong "earliest.")
2. **Verify each record's integrity stamp.** (WHY: only cryptographically sound records count as evidence.)
3. **Require a full matching chain** — an unauthorized access grant + matching control message + independent delivery receipt + a sensor reading confirming the outage — all in the same session, in the right order, within the allowed time gaps. (WHY: a genuine incident is corroborated across independent sources.)
4. **Among the multiple complete chains, pick the earliest corrected timestamp**; it resolves to an access grant never authorized under policy. (WHY: the true first alert is the earliest verified, policy-violating chain.)
5. **Combine the chain's IDs with the challenge formula** to produce the token/flag. (WHY: the formula binds the proven incident to the token.)

## Why It Worked (the vulnerability)
The decoys relied on investigators trusting raw timestamps and ID matches. Correcting drift and demanding independent cryptographic confirmation exposed the real earliest, unauthorized incident. **Fix (defensive):** enforce trusted, synchronized time and verify integrity stamps before correlating events.

## Flag
```
FLAG{BP01_E39F35ADE250}
```

## Takeaways
- Always correct clock drift before ordering cross-host events.
- Corroboration across independent sources beats any single matching field.
- Treat ID matches as a hint, not proof — require cryptographic integrity.

## Chain Note
**The Blackout Protocol** is a chained series where each chapter's token unlocks the next. Chapter 1 takes no prior token (it is the start) and outputs the token `FLAG{BP01_...}`, which Chapter 2 reuses to unlock its evidence.
