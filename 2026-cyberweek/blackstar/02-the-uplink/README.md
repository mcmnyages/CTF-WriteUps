---
title: "The Uplink"
event: "CyberWeek 2026"
series: "BLACKSTAR"
category: crypto
difficulty: medium
points: 300
status: solved
flag: "FLAG{BS02_9402A282B212}"
tags: [aes-cbc, rsa, fermat-factorization, key-derivation]
---

# The Uplink

> **TL;DR:** Derive an AES key from the Stage 1 token to unwrap an RSA-encrypted command, then break the RSA because its two primes are close enough for Fermat's factorization to split `n` instantly.

## Background (for beginners)
- **RSA** security rests on `n = p * q` being hard to factor. If `p` and `q` are chosen **close together**, `n` factors almost instantly.
- **Fermat's factorization** writes `n` as a difference of squares `a^2 - b^2`; it finds factors fast exactly when the primes are near each other.
- **Textbook RSA (no padding)** is deterministic and brittle — with the private key, decryption is immediate.
- A **key derivation function** (here SHA-256 of a token) turns a short secret into a fixed-size symmetric key.

## The Challenge
An encrypted uplink file was provided. The outer layer was AES-encrypted; inside sat an RSA public key `(n, e)` and an RSA-encrypted command to recover.

## Key Insight 💡
The RSA modulus was generated from two primes that sit suspiciously close together — a textbook setup for Fermat's method.

## Solution
1. **Derived the AES key** as SHA-256 of the Stage 1 token `007161435C98`; used the file's first 16 bytes as the IV and decrypted the remainder — chaining the prior stage's output into this one.
2. **Parsed the plaintext**, which contained the RSA public key `(n, e)` plus an encrypted command using textbook RSA (no padding).
3. **Ran Fermat's factorization** on `n` — it split on the first try, confirming the primes were too close.
4. **Rebuilt the private key** from `p` and `q` and decrypted the command to `RELAY_TOKEN=9402A282B212`.

## Why It Worked (the vulnerability)
RSA primes generated too close together collapse security — Fermat's method factors `n` in microseconds. *Defensive fix:* generate `p` and `q` independently with a large random gap (and use OAEP padding, never textbook RSA).

## Flag
```
FLAG{BS02_9402A282B212}
```

## Takeaways
- A close-prime RSA modulus is instantly breakable — always sanity-check `|p - q|`.
- Technique spotted: layered crypto where a symmetric layer wraps a weak asymmetric one; peel outward.

## Chain Note
BLACKSTAR Stage 2. **Token in:** `007161435C98` (from Stage 1, used as the AES key seed). **Token out:** `9402A282B212` (feeds Stage 3, The Flight Computer).
