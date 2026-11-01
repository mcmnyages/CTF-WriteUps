---
title: "Intercept Log"
event: "CyberWeek 2026"
series: "TIDEBREAKER"
category: crypto
difficulty: ADVANCED
points: 400
status: solved
flag: "FLAG{TB01_D486CE57852A}"
tags: [aes-ctr, nonce-reuse, many-time-pad, crib-dragging]
---

# Intercept Log

> **TL;DR:** 14 messages encrypted under AES-CTR with a reused nonce form a many-time pad; XOR pairs and the "space trick" recover the shared keystream column by column, decrypting everything without the key.

## Background (for beginners)
- **AES-CTR** turns a block cipher into a stream cipher: it generates a keystream and XORs it with plaintext. Security depends on **never reusing the (key, nonce) pair**.
- Reusing the keystream across messages creates a **many-time pad** — a classic, breakable mistake.
- XORing two ciphertexts that share a keystream cancels it, leaving `P1 XOR P2`.
- The **space trick (crib dragging):** in English text, XORing with a space (0x20) flips letter case, which reveals where spaces sit and thus the underlying letters.

## The Challenge
14 intercepted messages were all encrypted with AES-CTR using the **same keystream** (reused nonce). The task: recover the plaintext operator chatter — and the handshake token hidden inside it — without the AES key.

## Key Insight 💡
Nonce reuse collapses AES-CTR to a many-time pad. The key is irrelevant: the shared keystream can be reconstructed position-by-position from the English structure of the plaintexts alone.

## Solution
1. **Identify the reuse** — recognize all 14 ciphertexts share one keystream. *Why: this is what makes a keyless break possible.*
2. **XOR pairs** — XOR any two ciphertexts to cancel the keystream and get `P1 XOR P2`. *Why: isolates plaintext relationships.*
3. **Apply the space trick** — use XOR-with-space behavior across the set to pin down keystream bytes per column. *Why: English spaces leak letter positions.*
4. **Recover column by column** — work across all 14 messages per position to rebuild the full keystream, then decrypt. *Why: more messages per column means higher confidence.*
5. **Confirm via crib** — Message 3 read "Relay intercept confirmed token D486CE57852A retain this value for the handshake"; using that line as a crib derived the keystream and decoded all 14 cleanly. *Why: a known plaintext validates the recovered keystream and confirms the token.*

## Why It Worked (the vulnerability / technique)
Reusing an AES-CTR keystream/nonce across messages is a many-time pad; redundancy in natural-language plaintext lets an analyst recover the keystream without the key. **Defensive note:** never reuse a (key, nonce) pair in CTR mode — use a unique random nonce or a counter guaranteed never to repeat.

## Flag
```
FLAG{TB01_D486CE57852A}
```

## Takeaways
- Nonce reuse is catastrophic for any stream cipher, including AES-CTR.
- Crib dragging and the space trick turn XORed plaintexts into readable text.
- More ciphertexts sharing a keystream makes the break *easier*, not harder.
