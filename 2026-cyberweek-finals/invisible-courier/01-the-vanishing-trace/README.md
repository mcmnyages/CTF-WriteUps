---
title: "The Vanishing Trace"
event: "CyberWeek 2026"
series: "Invisible Courier"
category: forensics
difficulty: BASIC
points: 200
status: solved
flag: "FLAG{IC01_9E23CA265972}"
tags: [dfir, hash-chain, hmac, timeline-analysis]
---

# The Vanishing Trace

> **TL;DR:** Among twelve custody sessions only one is genuine; clock-correct timestamps, verify a hash chain + HMAC signatures, and match TX/RX witnesses to isolate session T-731, whose four event IDs in order unlock the capsule.

## Background (for beginners)
- **DFIR** (Digital Forensics & Incident Response) often means reconstructing a trustworthy timeline from noisy, partly-forged records.
- A **hash chain** links records so each one's hash depends on the previous — tampering breaks the chain.
- An **HMAC** is a keyed signature proving a record is authentic and unaltered.
- **Clock offsets** between stations must be corrected before any timing check is meaningful; **witness correlation** (independent TX and RX observers) confirms an event really happened.

## The Challenge
Twelve claimed custody sessions were provided, but only one genuinely documents the courier's disappearance. A valid route needed four stages in order — ARRIVAL, PICKUP, TRANSFER, SILENCE — on a fixed path, inside a time window, with linked hashes and independent witnesses. A provided offline console committed candidate event IDs.

## Key Insight 💡
No single check is decisive; authenticity emerges only when clock-corrected timing, an unbroken hash chain, valid HMACs, non-reused nonces, and matched TX/RX witnesses **all** hold — and drills and completed (DELIVERED) handovers are excluded.

## Solution
1. **Clock-correct** — fix each station's clock using offset beacons, then check the overall window and each inter-stage gap. *Why: timing checks are meaningless on uncorrected clocks.*
2. **Verify integrity** — confirm event hashes and HMAC signatures, that each stage's hash chains to the previous, and that no nonce was reused. *Why: proves records are authentic and ordered.*
3. **Match witnesses** — require each stage to have one valid TX and one valid RX witness within 8 seconds. *Why: independent corroboration that the stage occurred.*
4. **Exclude distractors** — reject drills and any session with a completed (DELIVERED) handover. *Why: a delivered courier did not vanish.*
5. **Commit the answer** — exactly one session, **T-731**, passed; commit its four event IDs in order to unlock the sealed capsule. *Why: ordered event IDs are the defined key.*

## Why It Worked (the vulnerability / technique)
Genuine custody is provable only through **multi-source forensic correlation**: clock correction + hash-chain/HMAC verification + TX/RX witness matching together reject forgeries that pass any single test. **Defensive note:** chain-of-custody systems should bind time, integrity, and independent witnesses so no one forged field can stand alone.

## Flag
```
FLAG{IC01_9E23CA265972}
```

## Takeaways
- Correct clocks before trusting any timeline.
- Hash chains + HMACs catch tampering a lone checksum would miss.
- Correlating independent witnesses is what separates real events from plausible fakes.

## Chain Note
Part 1 of **The Invisible Courier**. Part 2 ("Hacker's Laptop") continues the investigation on the same case and disk image.
