---
title: "CurveBreaker"
event: "CyberWeek 2026"
series: "Kivuli (cwa2026 finals)"
category: crypto
difficulty: easy
points: 100
status: solved
flag: "FLAG{cwa2026_finals_inv4lid_curv3_attack}"
tags: [invalid-curve-attack, ecdh, p-256, sha256-kdf]
---

# CurveBreaker

> **TL;DR:** An invalid-curve attack had already leaked the server's private key; re-running the provided solver's decryption (drop 8 bytes, derive a SHA-256 key from the shared secret) reveals the flag and a session secret.

## Background (for beginners)
- **ECDH** key exchange lets two parties derive a shared secret from points on an elliptic curve (e.g. P-256).
- An **invalid-curve attack** works when a server never checks the point you send is actually on the correct curve. Points from a weaker curve leak information, letting an attacker recover the server's private key piece by piece.
- Once the private key is known, the attacker can reconstruct the shared secret and decrypt captured traffic.
- A **KDF** (here SHA-256 of the shared secret) turns that secret into a symmetric key.

## The Challenge
The download contained four files: key-exchange notes, the server public key, a captured encrypted session, and a solver script. The challenge stated the attack was already completed and the solver held the recovered shared secret.

## Key Insight 💡
Reading the provided solver first (good practice with untrusted scripts) revealed exactly how the session is decrypted — no new attack work was needed.

## Solution
1. **Reviewed the four files** and noted the challenge said the invalid-curve attack was already done; the solver script already held the recovered shared secret.
2. **Read the solver script before running** anything, learning it drops the first 8 bytes of the session file and decrypts the rest using a SHA-256-based key derived from the shared secret.
3. **Reproduced that decryption** on the captured session.
4. **Recovered the flag** plus a `session_secret` (`cafe20261a6b72`) needed later in the Kivuli chain.

## Why It Worked (the vulnerability)
The server never validated that the client's point lay on the P-256 curve, so crafted off-curve points leaked its private key. *Defensive fix:* always validate incoming ECDH points are on the expected curve (and in the correct subgroup) before use.

## Flag
```
FLAG{cwa2026_finals_inv4lid_curv3_attack}
```

## Takeaways
- Missing point validation in ECDH enables full private-key recovery via invalid-curve attacks.
- Always read supplied scripts before executing — both for safety and to understand the intended path.

## Chain Note
Kivuli stage 7. The Kivuli set is numbered with gaps (stages 1, 5, 7, 8 here; others exist in the wider finals). **Token out:** `session_secret = cafe20261a6b72`, which feeds Kivuli 8 (PaddingOracle).
