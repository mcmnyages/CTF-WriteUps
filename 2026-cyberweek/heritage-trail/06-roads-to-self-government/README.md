---
title: "Roads to Self-Government"
event: "CyberWeek 2026"
series: "Heritage Trail"
category: osint
difficulty: advanced
points: 500
status: solved
flag: "FLAG{BICAMERAL}"
tags: [osint, crypto, columnar-transposition, historical-dating]
---

# Roads to Self-Government

> **TL;DR:** Date six independence milestones to order them, read off their COLUMN numbers (4,1,6,2,5,3) as a columnar-transposition key, then read a letter grid column-by-column in that order.

## Background (for beginners)
- A **columnar transposition cipher** writes text into a grid and scrambles it by reordering the columns. To decrypt, you read the columns back in the correct order — the **key**.
- Here the key is *earned*: you derive it from history rather than being handed it.
- **Dating events** precisely is again the gating OSINT skill.

## The Challenge
Six fragments described milestones on Kenya's road to independence. Each had a COLUMN number, but the dates were removed — you had to research the years, order the milestones, and use the resulting COLUMN sequence as a cipher key for a second file (a six-column letter grid).

## Key Insight 💡
The timeline *is* the key. Once the milestones are in chronological order, their attached COLUMN numbers give the exact column-read order for the transposition.

## Solution
1. **Research each milestone's year** (dates were stripped from the fragments).
2. **Order earliest → latest**:
   - First nominated African member joined LegCo (1944)
   - First elected African members (1957)
   - First Lancaster House Conference (1960)
   - Lancaster settlement establishing a two-house Parliament (1962)
   - Independence (1963)
   - Republic (1964)
3. **Read off the COLUMN numbers in that order** → key = `4,1,6,2,5,3`.
4. **Apply to the six-column grid**: read each column top-to-bottom in key order, then drop the padding after the closing brace — the result is the flag.

## Flag
```
FLAG{BICAMERAL}
```

## Takeaways
- Deriving a cipher key from research is a common "crypto + OSINT" combo — look for a sequence hidden in the clues.
- `BICAMERAL` (a two-house legislature) ties directly to the 1962 Lancaster settlement — the answer thematically confirms the history.
- To be faster: build the date table first; the key falls out immediately.

## Chain Note
Stage 6 (advanced). `BICAMERAL` is the sixth and final "building block" answer. HT7 reuses all six Heritage Trail answers as instructions, so this completes the set the finale depends on.
