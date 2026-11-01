---
title: "Padly"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: basic
points: 150
status: solved
flag: "FLAG{cr4ck-th3-c0d3-3asy-d3duct10n}"
tags: [brute-force, constraint-satisfaction, logic-puzzle]
---

# Padly

> **TL;DR:** A hidden 3-digit code came with five "how close" clues. Test all 1000 codes against every clue and only one satisfies all five — a constraint-satisfaction brute force.

## Background (for beginners)
- A **brute force** tries every possible answer. With only 1000 three-digit codes, exhaustive search is instant.
- **Constraint satisfaction** means filtering that full space down to candidates that meet *all* given rules at once.
- Each clue (a guess plus how close it was, e.g. Mastermind-style hints) is a constraint that eliminates most candidates.
- Not a memory-corruption bug — this is logic deduction automated with code. (The category is "web" but it is really a logic puzzle.)

## The Challenge
The game reveals a hidden 3-digit code only after you guess it. It gives five clues, each describing how close a particular guess was. Tooling: Python brute-force solver.

## Key Insight 💡
Instead of reasoning the clues out by hand, **check every 3-digit code (000–999) against all five clues at once.** Exactly one code is consistent with every clue.

## Solution
1. **Model each clue as a check** — a function that, given a candidate code, returns whether the clue's "closeness" would hold. *Why:* this makes each clue a precise filter.
2. **Loop over all 1000 codes** and keep only those passing *every* clue. *Why:* the correct code must satisfy all constraints simultaneously.
3. **Read off the single surviving candidate.** *Why:* a well-posed puzzle leaves exactly one solution.
4. **Submit that code** back to the game to receive the flag. *Why:* the game validates the code and reveals the flag.

Illustrative pseudocode:
```
for code in range(000..999):
    if all(clue_matches(code) for clue in clues):
        print(code)   # the answer
```

## Why It Worked (the vulnerability)
The code space was tiny and fully constrained by the clues, so exhaustive search trivially recovers it. **Fix (for a real secret):** never rely on a small, guessable secret space; use large, random, rate-limited secrets.

## Flag
```
FLAG{cr4ck-th3-c0d3-3asy-d3duct10n}
```

## Takeaways
- **Pattern:** tiny keyspaces fall instantly to brute force.
- **Spotting it:** count the possibilities — if small, enumerate them.
- **Fixing it:** large random secrets, attempt rate limiting, and lockouts.
