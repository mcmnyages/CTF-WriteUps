---
title: "Njia Nyingi, Nchi Moja"
event: "CyberWeek 2026"
series: "Heritage Trail"
category: osint
difficulty: basic
points: 100
status: solved
flag: "FLAG{ROOTS}"
tags: [osint, web-research, acrostic, museums-kenya]
---

# Njia Nyingi, Nchi Moja

> **TL;DR:** Visit five museum pages on museums.or.ke, pull one keyword (an ethnic community / feature) from each, then take a single specified letter from each keyword to spell the flag.

## Background (for beginners)
- **OSINT** (Open-Source Intelligence) means answering questions using only publicly available information — here, an official museum website.
- An **acrostic** puzzle hides a word in the first (or a chosen) letter of a series of answers. You must solve each clue, then read down the letters.
- Knowing *where* authoritative information lives (official `.or.ke` domains) is half the skill: trust the source, then mine it.

## The Challenge
The prompt ("Many paths, one country") pointed to five stops on `museums.or.ke`. Each stop yields one answer, and one letter from each answer builds the flag.

## Key Insight 💡
Each museum page is tied to a specific heritage community or feature. Identify that keyword per page, and the puzzle becomes a simple letter-extraction acrostic.

## Solution
1. **Enumerate the five stops**: Meru, Kabarnet, Lamu, Hyrax Hill, and Tambach Museums — each has its own page on the site.
2. **Find the keyword per page** — the community or feature each museum is known for: Meru, Pokot, Orma, Turkana, Sirikwa. (Knowing which community each region represents is the OSINT work.)
3. **Take one specified letter from each keyword.** The challenge dictates which position to pull, so you don't just use the first letter blindly.
4. **Read the letters in order** — they spell `ROOTS`, wrapped as the flag.

## Flag
```
FLAG{ROOTS}
```

## Takeaways
- Treat official institutional sites as a structured dataset — the "stops" map cleanly to pages.
- For acrostics, record each answer in full first; the extraction rule may not be "first letter."
- To be faster: open all five pages at once and tabulate community + candidate letters side by side.

## Chain Note
This is stage 1 of the eight-part Heritage Trail. Its answer `ROOTS` establishes the theme (origins/heritage) and, like every stage, becomes a reusable building block — HT7 explicitly recombines all six earlier answers, so logging each flag cleanly matters from the start.
