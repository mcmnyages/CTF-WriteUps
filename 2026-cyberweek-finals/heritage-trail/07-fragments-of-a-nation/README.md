---
title: "Fragments of a Nation"
event: "CyberWeek 2026"
series: "Heritage Trail"
category: crypto
difficulty: advanced
points: 600
status: solved
flag: "FLAG{KENYA-HERITAGE}"
tags: [crypto, puzzle, grid-extraction, chained-challenge]
---

# Fragments of a Nation

> **TL;DR:** The six earlier Heritage Trail answers are *instructions* — they tell you which file (A17F09), where to start, which direction, and which cells to read from two letter grids, which spell KENYA and HERITAGE.

## Background (for beginners)
- A **chained puzzle** reuses prior answers as inputs, so earlier solves must be recorded exactly.
- **Grid extraction** means pulling specific cells (by row/column position) out of a letter matrix to reconstruct a hidden word.
- The twist: answers you already have aren't just flags — they're a *decoding procedure*.

## The Challenge
The penultimate stage reused all six previous Heritage Trail answers. Rather than new research, each answer described part of a hidden reading operation over a data file.

## Key Insight 💡
The earlier answers stop being trivia and become a step-by-step instruction set: *which* file, *how many* sections, *where* to start, *which direction* to read, and *which* cells to pick — assembled in order.

## Solution
1. **Recognize the reuse** — the six prior answers encode the method, not new clues.
2. **Decode the instructions** from them: the target file is `A17F09` (from HT5); it has two sections; plus the start point, reading direction, and which cells to pick, keeping sections in order.
3. **Open the file** — two letter grids. Using the given cell positions, pull one piece from three rows in each grid.
4. **Assemble**: first grid spells `KENYA`, second spells `HERITAGE`; join them. A deliberate marker in the data confirms the correct read.

## Flag
```
FLAG{KENYA-HERITAGE}
```

## Takeaways
- In a chain, keep a clean log of every earlier answer — you may need them verbatim.
- When a stage "reuses" prior work, re-interpret those answers as parameters/instructions, not as facts to look up again.
- Confirm reads against any built-in marker before submitting.

## Chain Note
Stage 7 is the payoff of the chain: every prior answer feeds in, and the result `KENYA-HERITAGE` is not just a flag — it becomes the AES password that unlocks the final archive in HT8.
