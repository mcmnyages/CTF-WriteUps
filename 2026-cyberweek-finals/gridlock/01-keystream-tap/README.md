---
title: "Keystream Tap"
event: "CyberWeek 2026"
series: "GRIDLOCK"
category: crypto
difficulty: INSANE
points: 600
status: solved
flag: "FLAG{GL01_D40FC56C0D64}"
tags: [lfsr, berlekamp-massey, known-plaintext, stream-cipher]
---

# Keystream Tap

> **TL;DR:** A 64-bit LFSR stream cipher falls to a known-plaintext attack: a fixed 30-byte header yields 240 keystream bits, Berlekamp-Massey recovers the recurrence, and running it forward decrypts the whole log.

## Background (for beginners)
- An **LFSR** (linear feedback shift register) generates a pseudo-random bit stream from a linear recurrence. XORing that stream with plaintext is a simple stream cipher.
- LFSR streams are **fully predictable**: once you know enough output bits, you know the rest forever.
- The **Berlekamp-Massey algorithm** finds the shortest linear recurrence that produces a given bit sequence — it needs only about **2n bits** to recover an n-bit LFSR.
- A **known-plaintext attack** uses text you can predict (like a fixed header) to extract keystream.

## The Challenge
A relay log was XOR-encrypted with the keystream of a **64-bit LFSR**. The log always begins with a fixed header: `GRIDLOCK SUBSTATION RELAY LOG` + newline (30 bytes). The full ciphertext was 176 bytes.

## Key Insight 💡
The fixed 30-byte header is a known plaintext. XORing it against the first 30 ciphertext bytes yields 240 raw keystream bits — well over the 2*64 = 128 needed for Berlekamp-Massey to reconstruct a 64-bit LFSR exactly.

## Solution
1. **Spot the known header** — the log always starts with the 30-byte fixed string. *Why: predictable plaintext is the attack's entry point.*
2. **Extract keystream** — XOR the first 30 ciphertext bytes with the header to recover 240 keystream bits. *Why: keystream = ciphertext XOR known plaintext.*
3. **Run Berlekamp-Massey** — feed the bits (MSB first) in to recover the exact 64-bit linear recurrence. *Why: 240 > 128 bits fully determines the LFSR.*
4. **Regenerate full keystream** — run the recurrence forward to produce keystream for all 176 bytes. *Why: an LFSR is deterministic once its recurrence is known.*
5. **Decrypt and read** — XOR the full keystream against the whole ciphertext; the log contained "keystream tap token D40FC56C0D64". *Why: yields the token.*

## Why It Worked (the vulnerability / technique)
An LFSR stream cipher is linear and fully predictable: a short known header recovers the entire keystream via Berlekamp-Massey, regardless of key length. **Defensive note:** never use a bare LFSR as a cipher — use a cryptographically secure keystream generator.

## Flag
```
FLAG{GL01_D40FC56C0D64}
```

## Takeaways
- ~2n output bits are enough to fully clone an n-bit LFSR.
- Fixed headers/magic bytes are free known-plaintext for stream-cipher attacks.
- Linearity is fatal in cryptography; Berlekamp-Massey exploits it directly.
