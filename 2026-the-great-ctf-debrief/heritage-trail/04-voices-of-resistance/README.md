---
title: "Voices of Resistance"
event: "The Great CTF Debrief 2026"
series: "Heritage Trail"
category: osint
difficulty: medium
points: 300
status: solved
flag: "FLAG{ORDER}"
tags: [osint, historical-dating, odd-one-out, sorting]
---

# Voices of Resistance

> **TL;DR:** Six history records each carry a letter token; discard the one that isn't actually resistance (a 2007 statue), then sort the remaining five by date — their tokens spell ORDER.

## Background (for beginners)
- **Historical OSINT** means verifying events and, crucially, *dating* them from reliable sources.
- **Odd-one-out** reasoning: part of the puzzle is recognizing one item doesn't belong with the rest.
- **Sorting as a cipher key**: when tokens must be read "in order," the ordering itself (here, chronological) is the hidden instruction.

## The Challenge
An archive unzipped into six short history records, each tagged with a one-letter token. All looked like Kenyan "resistance" history — but one was a distractor.

## Key Insight 💡
The flag literally is `ORDER`, and the puzzle enforces it two ways: you must drop the non-resistance item, then place the rest in chronological order. The theme word *is* the method.

## Solution
1. **Unzip** and read the six records.
2. **Identify each event** from Kenyan heritage sources:
   - Siyu resisting Omani rule (19th century)
   - Nandi resistance under Koitalel arap Samoei (ended 1905)
   - Mekatilili wa Menza & the Giriama uprising (1913–1914)
   - Muindi Mbingu's destocking protest (1938)
   - The Kapenguria Six trial (1952–1953)
3. **Spot the odd one out** — the sixth record was the Dedan Kimathi statue (2007), an act of *remembrance*, not resistance. Remove it.
4. **Order the remaining five earliest → latest**; their tokens read `O, R, D, E, R` = `ORDER`.

## Flag
```
FLAG{ORDER}
```

## Takeaways
- Always sanity-check category fit: a commemoration is not an event of resistance.
- Precise dating (end-years, trial years) is what makes the sort unambiguous.
- To be faster: extract dates first, flag anything that breaks the pattern immediately.

## Chain Note
Stage 4 (medium). Its answer `ORDER` is both a flag and a foreshadowing of the ordering mechanics in HT6, and it joins the pool of answers reused by HT7.
