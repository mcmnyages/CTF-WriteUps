---
title: "The Telegraph Ledger"
event: "The Great CTF Debrief 2026"
series: "Lost Signal"
category: forensics
difficulty: BASIC
points: 150
status: solved
flag: "FLAG{LS01_8EC5C9EBF7C3}"
tags: [custom-encoding, timing-analysis, checksums, forensics]
---

# The Telegraph Ledger

> **TL;DR:** Separate genuine telegraph entries from forged/replayed decoys by clock-correcting timestamps across three stations, keep only timing- and checksum-valid fragments, decode them with a custom cipher, and combine with case details to build the token.

## Background (for beginners)
- A **checksum** is a tiny value that detects *accidental* corruption, but it does not prove authenticity — an attacker can recompute it after tampering.
- Historical telegraph networks relayed a message station-to-station, each with its own slightly off **clock offset**.
- **Timing correlation** across independent stations is a forensic tool: genuine traffic follows an expected schedule; forgeries and replays usually do not.
- Custom encodings require you to first recover the scheme (from notes) before any plaintext appears.

## The Challenge
A historical note pointed to a real 19th-century surveyed telegraph route (Mombasa -> Malindi -> Lamu), matching one of three candidate lines and ruling out two decoy routes. The ledger contained many logged message fragments — several altered or duplicated — each carrying a small checksum.

## Key Insight 💡
Checksums alone cannot catch tampering. The real discriminator is **timing**: correct each station's clock by its offset, then only fragments whose corrected times fit the expected schedule (fixed start at the first station, the next two at fixed delays) are genuine.

## Solution
1. **Confirm the route** — match the historical survey note to the Mombasa->Malindi->Lamu line, ruling out the two decoy routes. *Why: scopes which entries are even relevant.*
2. **Clock-correct timestamps** — apply each station's clock-offset to every entry. *Why: raw times are untrustworthy across stations.*
3. **Filter by schedule** — keep only entries whose corrected time matches the fixed start plus fixed per-hop delays. *Why: forgeries/replays break the timing pattern.*
4. **Cross-check** — the timing-correct entries also agreed with each other and passed their checksums; decoys failed timing and/or checksum. *Why: multi-signal agreement = authenticity.*
5. **Decode** — run each correct fragment through the custom cipher from the notes and join them in order. *Why: recovers the readable message.*
6. **Build the token** — combine the recovered message with case details via the challenge formula. *Why: that is the defined output format for the token.*

## Why It Worked (the vulnerability / technique)
A checksum detects accidental corruption, not deliberate tampering, so attackers can forge/replay entries with valid checksums. By cross-checking clock-corrected timing across three independent stations, genuine traffic is separable from forged or replayed entries. **Defensive note:** pair integrity checks with authenticated timestamps/signatures, not bare checksums.

## Flag
```
FLAG{LS01_8EC5C9EBF7C3}
```

## Takeaways
- Checksums catch accidents, not adversaries — never treat them as authentication.
- Clock-offset correction turns messy multi-station timestamps into a reliable filter.
- Corroborating signals (timing + checksum + mutual agreement) beat any single check.

## Chain Note
This is Chapter 1 of **Lost Signal**. The recovered token here is consumed by Lost Signal 2 ("Voices Through the Air") as the seed for its keystream.
