---
title: "Harmonic Drift"
event: "CyberWeek 2026"
series: "SC Series"
category: stego
difficulty: MEDIUM
points: 350
status: solved
flag: "FLAG{SC03_73DA9B6E4F21}"
tags: [fsk, signal-processing, drift-tracking, decoy-rejection]
---

# Harmonic Drift

> **TL;DR:** Demodulate 4-FSK audio while tracking a drifting frequency reference via a pilot tone, decode three valid-CRC frames, then match each frame's SHA-256 against receiver receipts — only the CONFIRMED/RELEASED packet is the real flag.

## Background (for beginners)
- **FSK** (Frequency-Shift Keying) encodes data as distinct tone frequencies; **4-FSK** uses four tones, so each symbol carries 2 bits.
- A **drifting reference** means the transmitter/receiver clock or oscillator slowly shifts frequency over time, so fixed tone thresholds stop working.
- A **pilot tone** is a known reference signal you measure to estimate and cancel that drift.
- A valid-looking flag with a correct **CRC** is not proof of authenticity — independent **receipts/hashes** are needed to reject decoys.

## The Challenge
Recordings are 4-level FSK radio at 8000 samples/sec, 40 ms per symbol, with a continuously drifting frequency reference. A known calibration recording confirmed the demod method by decoding its test flag correctly. Multiple packets decoded to flag-shaped text, so a valid flag alone was not proof.

## Key Insight 💡
Because the reference drifts, each symbol must be decided relative to a measured **pilot tone** (near 3115 Hz); and because several packets produce valid-CRC flag text, authenticity requires matching **frame hashes** against independent release receipts — not trusting the flag shape.

## Solution
1. **Validate the method** — use the calibration recording to confirm the demodulator by decoding its known test flag. *Why: proves the pipeline is correct before trusting real data.*
2. **Track drift per symbol** — measure the pilot tone near 3115 Hz each symbol, then shift the four FSK tone frequencies by that amount before deciding the symbol. *Why: the drifting reference would otherwise cause mis-decodes.*
3. **Decode frames** — turn tone symbols into bytes and parse each frame (header, obfuscated payload, CRC32), reversing the obfuscation; all three packets decoded with valid CRCs and flag-shaped text. *Why: CRC confirms clean decode but not authenticity.*
4. **Reject decoys by hash** — take SHA-256 of each full frame and match against independent receiver receipts; only one packet matched a receipt marked **CONFIRMED and RELEASED**. *Why: the other two were a calibration echo and a held transmission.*
5. **Extract the genuine flag** from that confirmed packet. *Why: it is the only released, authentic frame.*

## Why It Worked (the vulnerability / technique)
Robust FSK demodulation requires pilot-based drift tracking; and because decoys also yield valid CRCs and flag text, cross-checking frame hashes against release receipts is what distinguishes the genuine transmission. **Defensive note:** integrity (CRC) and authenticity (signed/receipted hashes) are different guarantees — verify both.

## Flag
```
FLAG{SC03_73DA9B6E4F21}
```

## Takeaways
- Track and cancel reference drift with a pilot tone before deciding symbols.
- A valid CRC proves a clean decode, not a genuine message.
- Match frame hashes against independent receipts to reject echoes and held transmissions.

## Chain Note
SC03 of the cross-category **SC Series** (SC01/SC02/SC03), closing out the multi-discipline storyline.
