---
title: "Follow the Analyst"
event: "CyberWeek 2026"
series: "Standalone"
category: forensics
difficulty: basic
points: 100
status: solved
flag: "FLAG{C1-B6-A4-B1}"
tags: [visual-analysis, incident-response, evidence-review, authenticated-access]
---

# Follow the Analyst

> **TL;DR:** An incident-sheet image was login-gated, so it was viewed inside a signed-in browser; an analyst's red-pen annotations marked which security events mattered, and the tail of each circled event ID, read in time order, spelled the flag.

## Background (for beginners)
- **Visual evidence analysis** means treating a screenshot or scanned document as the artifact itself; the information lives in what is drawn, circled, or struck out, not in file metadata.
- **Access-gated media** is content that will not render unless you are authenticated. Downloading the raw URL often fails or returns a placeholder, while an already-signed-in browser session can display it.
- Analysts routinely annotate evidence (circling relevant rows, crossing out noise) to communicate a triage decision at a glance.
- Reading annotations in the intended order (here, chronological) is what turns scattered marks into a coherent answer.

## The Challenge
An incident sheet was provided as an image that required a login to view. The image contained a table of security events. An analyst had reviewed it by hand: some rows were circled in red pen, and others were crossed out or ignored.

## Key Insight 💡
The flag is not hidden in the file; it is encoded by the analyst's own markings. Only the **circled** events count, and the meaningful piece of each is the **last part of its event ID** — assembled in **chronological** order.

## Solution
1. **Open the image in a signed-in browser** instead of downloading it directly — the media was access-gated, so an authenticated session was required just to render the table. *Why:* a raw download would not have shown the content.
2. **Visually inspect the annotations** and separate the circled rows from the crossed-out/ignored rows. *Why:* the crossed-out rows are deliberate noise meant to distract.
3. **Extract the last segment of each circled event's ID.** *Why:* that trailing token is the flag fragment the analyst was pointing to.
4. **Sort the circled events by their timestamp** and concatenate the fragments in that order. *Why:* time order is the intended sequence, producing `C1-B6-A4-B1`.

## Why It Worked (the vulnerability / technique)
This is pure visual evidence analysis combined with authenticated access to gated media. The "secret" was steganographic only in spirit — it lived in human annotations overlaid on an image. **Defensive note:** sensitive triage notes embedded in shared images can leak decision logic; redact or store analyst markup separately from distributable evidence.

## Flag
```
FLAG{C1-B6-A4-B1}
```

## Takeaways
- When media will not load, try an authenticated browser session before assuming the file is broken.
- Human annotations are data; respect both what is highlighted and what is deliberately struck out.
- Order matters — chronological sequencing was the final key to assembling the flag.
