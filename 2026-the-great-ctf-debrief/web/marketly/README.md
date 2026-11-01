---
title: "Marketly"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: basic
points: 150
status: solved
flag: "FLAG{n3g4t1v3-qty-buys-th3-k3y}"
tags: [input-validation, business-logic, negative-quantity, integer-abuse]
---

# Marketly

> **TL;DR:** The cart let you order a **negative** quantity of a cheap item, subtracting value from the total. Pair a rare item with a huge negative quantity of a sticker and the bill drops under your 50-credit balance.

## Background (for beginners)
- A **business-logic flaw** is a bug in the rules of the app, not in its code syntax — the app does exactly what it was told, but what it was told is wrong.
- **Missing input validation** on numeric fields (like quantity) lets attackers send values the designers never intended, such as negatives.
- A negative quantity multiplied by a price yields a **negative line total**, acting like a discount or credit.
- Dangerous because it bypasses payment/limits without any "hacking" — just unexpected numbers.

## The Challenge
Your wallet holds 50 credits. A rare item costs far more than that; a cheap sticker is also for sale. Tooling: Python.

## Key Insight 💡
Nothing stops a **negative quantity**. Buying a big negative quantity of the cheap sticker produces a negative subtotal that cancels out most of the rare item's cost, pulling the order total below 50.

## Solution
1. **Inspect the order request** and confirm quantity is sent as a plain number. *Why:* we need to know the field we can tamper with.
2. **Add the rare item (quantity 1)** plus the cheap sticker at a **large negative quantity**. *Why:* the sticker's negative line total offsets the rare item's price.
3. **Tune the negative quantity** so the computed total is at or below your 50-credit balance. *Why:* the server only checks that total ≤ balance, not that quantities are valid.
4. **Submit the order.** It went through, granting the rare item and the flag. *Why:* the total passed the balance check, so the purchase completed.

## Why It Worked (the vulnerability)
The server computed the total without validating that quantities are positive, so negative quantities reduced the bill. **Fix:** validate every quantity as a positive integer within sane bounds server-side, and reject negative or absurd values before pricing.

## Flag
```
FLAG{n3g4t1v3-qty-buys-th3-k3y}
```

## Takeaways
- **Pattern:** unvalidated numeric inputs enable negative-value / business-logic abuse.
- **Spotting it:** try negatives, zero, and huge values on any quantity or amount field.
- **Fixing it:** server-side bounds checks and type/range validation on all numbers.
