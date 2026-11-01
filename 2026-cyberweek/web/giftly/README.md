---
title: "Giftly"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{t0ct0u-d0ubl3-sp3nd-r4c3-w1n}"
tags: [race-condition, toctou, double-spend, concurrency]
---

# Giftly

> **TL;DR:** The redeem endpoint checked "is this code used?" and marked it used in two non-atomic steps; firing many concurrent redeems for the same single-use 100-credit code let several slip through, pushing the balance past the 1000 needed to buy the vault.

## Background (for beginners)
- A **race condition / TOCTOU** (time-of-check to time-of-use) bug occurs when a check and the action based on it aren't performed atomically.
- If many requests run at once, several can pass the same check before any of them records the result.
- For a single-use code, this means **double-spending**: it's redeemed multiple times.

## The Challenge
Each new account gets one welcome code worth 100 credits; the reserve vault needs 1000. Redeeming once gives 100; redeeming the same code again is correctly rejected as already used.

## Key Insight 💡
The rejection on a *second sequential* attempt works, but the "already used?" check and the "mark used" step are separate. If you send many redeem requests simultaneously, they all read "not used yet" before any writes "used," so each credits +100.

## Solution
1. Redeem once (100 credits) and confirm a sequential re-redeem is rejected. *Why: establishes single-use enforcement and a credit gap of 900 to reach the vault.*
2. Prepare many identical redeem requests for the same code. *Why: concurrency is what breaks the non-atomic check.*
3. Fire them all at the same instant (e.g. a shell loop of parallel requests). *Why: they hit the window between check and mark-used together.*
4. Observe several succeed, each adding 100, pushing the balance past 1000. *Why: multiple requests passed the stale "not used" check.*
5. Buy the reserve vault. *Why: the purchase gate is the credit threshold, now met.*

## Solver sketch (illustrative pseudocode)
```
for i in 1..30: curl -X POST /redeem -d code=WELCOME &   # all in parallel
wait
POST /buy-vault
```

## Why It Worked (the vulnerability)
The used-check and the mark-used write were not atomic (no lock/transaction/unique constraint), so concurrent requests double-spent a single-use code. **Fix:** make redemption atomic — a DB transaction with a unique constraint or an atomic conditional update (compare-and-set) on the code's state.

## Flag
```
FLAG{t0ct0u-d0ubl3-sp3nd-r4c3-w1n}
```

## Takeaways
- Sequential correctness doesn't imply concurrent correctness — test with parallel requests.
- TOCTOU windows turn single-use tokens into infinite-use ones.
- Enforce atomicity with transactions, locks, or unique constraints.
