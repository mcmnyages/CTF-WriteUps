---
title: "The Flight Computer"
event: "The Great CTF Debrief 2026"
series: "BLACKSTAR"
category: rev
difficulty: hard
points: 400
status: solved
flag: "FLAG{BS03_0D9E75EA984A}"
tags: [reverse-engineering, binary-analysis, strings, chained-challenge]
---

# The Flight Computer

> **TL;DR:** A Linux binary demands a launch authorisation token; the correct value is the Stage 2 token, and entering it exactly prints the next relay token.

## Background (for beginners)
- **Reverse engineering** means figuring out how a compiled program behaves without its source — often starting with readable text (`strings`) inside the binary.
- Programs frequently gate behavior behind an input check, printing success or `ACCESS DENIED` depending on a comparison.
- In a **chained CTF**, the "secret" one stage expects is simply the token produced by the previous stage.
- Running an unknown binary safely means using a controlled environment (here, WSL/Linux).

## The Challenge
An executable "flight computer" asks for a *launch authorisation token*. Wrong input yields `ACCESS DENIED`; the goal is to satisfy it and recover the next token.

## Key Insight 💡
The brief hinted the authorisation comes "from the previous stage" — no cracking needed, just feed in the Stage 2 token in the exact expected form.

## Solution
1. **Dumped strings** from the binary to understand its flow — it prompts for a launch authorisation token and branches to `ACCESS DENIED` on a mismatch.
2. **Read the brief**, which stated the auth value comes from the prior stage, so the candidate was the Stage 2 token `9402A282B212`.
3. **Ran the binary in Linux (WSL)** and entered the token; it was accepted and printed `RELAY_TOKEN=0D9E75EA984A`. (Lowercase or random inputs were rejected — the check is exact and case-sensitive.)

## Why It Worked (the vulnerability)
The binary hardcodes/derives its expected token from a predictable chain value rather than a true secret, so knowing the prior stage fully authorizes you. *Defensive fix:* never treat a reused, guessable token as an authorization credential — require independently verified, non-predictable secrets.

## Flag
```
FLAG{BS03_0D9E75EA984A}
```

## Takeaways
- `strings` plus reading the prompt flow often reveals exactly what a binary wants.
- In chained challenges, test the prior stage's output before attempting any heavy reversing.

## Chain Note
BLACKSTAR Stage 3. **Token in:** `9402A282B212` (from Stage 2, the launch code). **Token out:** `0D9E75EA984A` (feeds Stage 4, The Telemetry Gateway).
