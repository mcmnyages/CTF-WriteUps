---
title: "Fuata Njia"
event: "CyberWeek 2026"
series: "Heritage Trail"
category: osint
difficulty: basic
points: 150
status: solved
flag: "FLAG{M4A7P2}"
tags: [osint, geolocation, map-markers, heritage-sites]
---

# Fuata Njia

> **TL;DR:** A map of Kenyan locations carries coded markers; identify four heritage sites by location, match each to its marker code, and concatenate the codes in order.

## Background (for beginners)
- **Geolocation OSINT** is the skill of pinning down a place from clues (a description, a coastline, a nearby town) and cross-referencing it on a map.
- A **codebook/lookup** puzzle hides the real answer behind a lookup table — here, each place maps to a short code.
- "Fuata njia" means "follow the path": the puzzle rewards methodical tracing rather than guessing.

## The Challenge
An image map of Kenya showed markers at several locations, each labeled with a short code. Four heritage sites were described — near Migori, on the coast, and around Lamu — and each had to be matched to its marker.

## Key Insight 💡
The marker codes are meaningless alone; the value is in correctly *locating* each heritage site, then reading off that marker's code. Order matters — the flag is the codes concatenated in the given sequence.

## Solution
1. **Open the map image** (via Playwright) and catalog every marker and its code.
2. **Research the four heritage sites** from their descriptions — e.g. a site near Migori, coastal sites, and one in the Lamu area — to fix their map positions.
3. **Match each site to the marker** sitting at its location.
4. **Combine the codes in order** to form `M4A7P2`.

## Flag
```
FLAG{M4A7P2}
```

## Takeaways
- Nail the location first; the code is a trivial lookup once the pin is right.
- Keep a marker-to-code table so you don't misread adjacent pins.
- To be faster: identify sites from the text description before even opening the map, then just confirm positions.

## Chain Note
Stage 2 of the Heritage Trail. It reinforces the map/geolocation theme and contributes another answer to the growing set that HT7 and HT8 ultimately depend on.
