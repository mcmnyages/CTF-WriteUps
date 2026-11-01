---
title: "Voices Through the Air"
event: "The Great CTF Debrief 2026"
series: "Lost Signal"
category: forensics
difficulty: MEDIUM
points: 250
status: solved
flag: "FLAG{LS02_60AAA70740D0}"
tags: [audio, signal-processing, fsk, duplicate-detection]
---

# Voices Through the Air

> **TL;DR:** Decode tone-coded audio bursts into fields, reject a look-alike test transmitter by its origin marker and a corrupted retransmission by checksum, then decrypt the surviving payloads with a keystream seeded by the Chapter 1 token.

## Background (for beginners)
- Audio can carry data as **tones**: a marker tone to synchronize, then two distinct tones representing bit values 0 and 1.
- Bit packing order matters — here bits are packed **least-significant-bit first (LSB-first)**.
- A **checksum** catches corruption but not a genuine-looking message from the wrong source; the **origin field** identifies *who* sent it.
- **Duplicate sequence numbers** usually mean a retransmission — one copy may be corrupted and must be discarded.

## The Challenge
A long monitor recording held many logged bursts. A known reference recording provided a short, known two-byte test signal that revealed the audio code (marker tone, then 0/1 tones, LSB-first). Each burst decodes into fields: origin, sequence number, payload, and a check byte.

## Key Insight 💡
A valid checksum is not enough. One burst came from a **test/training transmitter** (wrong origin marker) despite a good checksum, and a duplicated sequence number signaled a **corrupted retransmission** — only the real origin field plus duplicate notes expose them.

## Solution
1. **Recover the code** — use the known two-byte test signal from the reference recording to establish the marker + 0/1 tone scheme and LSB-first packing. *Why: you cannot read bursts without the demod scheme.*
2. **Decode all bursts** into (origin, sequence, payload, check byte). *Why: structured fields enable filtering.*
3. **Reject the imposter** — drop the burst with the wrong origin marker even though its checksum passed. *Why: it is a test/training transmitter, not genuine traffic.*
4. **Resolve duplicates** — two bursts shared a sequence number; one failed the documented checksum (matching an operator note about a dropped signal), so keep the other. *Why: leaves exactly one genuine burst per sequence.*
5. **Decrypt payloads** — build the keystream from the Chapter 1 token and decrypt each payload. *Why: the token chains the series together.*
6. **Assemble** — join decrypted payloads in order into a readable sentence, then combine with case details to form this chapter's token. *Why: defined output format.*

## Why It Worked (the vulnerability / technique)
Checksums verify integrity, not provenance. Correct de-duplication required the real **origin field** to reject a look-alike test broadcast and operator notes to reject a corrupted retransmission. **Defensive note:** authenticate the source and sequence, not just the payload integrity.

## Flag
```
FLAG{LS02_60AAA70740D0}
```

## Takeaways
- Demodulate carefully: marker tone and bit-packing order are load-bearing details.
- Origin and sequence metadata, not just checksums, separate genuine from spoofed/retransmitted signals.
- Chained keystreams mean earlier chapters' tokens unlock later ones.

## Chain Note
Chapter 2 of **Lost Signal**. It consumes the **Chapter 1 token** to build its decryption keystream, so it cannot be solved before Lost Signal 1.
