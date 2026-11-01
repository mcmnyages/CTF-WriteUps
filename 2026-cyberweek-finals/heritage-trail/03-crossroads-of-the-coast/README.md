---
title: "Crossroads of the Coast"
event: "CyberWeek 2026"
series: "Heritage Trail"
category: osint
difficulty: basic
points: 200
status: solved
flag: "FLAG{MONSOON}"
tags: [osint, steganography, pixel-data, acrostic]
---

# Crossroads of the Coast

> **TL;DR:** An acrostic from four coastal-site descriptions spells EAST, which points to the right edge of a downloaded image; the flag is hidden in the pixel color values along that edge.

## Background (for beginners)
- **Steganography** is hiding data inside another file — here, bytes tucked into the color values of an image's pixels.
- An **acrostic** (again) first yields a *hint*, not the flag — showing clues can be nested.
- Pixels store **RGB color values** (0–255 each). Those numbers can be repurposed to smuggle a hidden message, readable only if you know where to look.

## The Challenge
Four coastal heritage sites — Gede Ruins, Siyu Fort, Lamu Museum, Takwa Ruins — each had a description. One letter from each spelled a direction, which then told you *where* in a supplied image the real data was hidden.

## Key Insight 💡
The OSINT acrostic (`EAST`) isn't the flag — it's a map coordinate. "East" = the right edge of the image, so you only need to decode the pixel values down that one column.

## Solution
1. **Read the four site descriptions** and take one letter from each: they spell `EAST`.
2. **Interpret the hint** — East means the right-hand edge of the image is where data is concealed.
3. **Download the coded image** (via Playwright).
4. **Decode the right edge** pixel by pixel in Python, reading the hidden data out of the color values — it spells the flag.

*Illustrative* pseudocode:
```
for y in range(height):
    r,g,b = image.getpixel((width-1, y))
    # map color value(s) back to a character
    message += chr(...)
```

## Flag
```
FLAG{MONSOON}
```

## Takeaways
- An OSINT answer can be a *pointer* into a forensics step — read the whole puzzle before deciding what the answer "is."
- For edge-based stego, test both axes and both ends; "EAST" removes the guesswork.
- `MONSOON` fits the theme: monsoon winds drove the Swahili coast's trade crossroads.

## Chain Note
Stage 3 bridges pure OSINT into light steganography, and its answer `MONSOON` joins the reusable answer set that the later chained stages (HT7/HT8) draw on.
