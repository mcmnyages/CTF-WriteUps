---
title: "PaddingOracle"
event: "The Great CTF Debrief 2026"
series: "Kivuli (cwa2026 finals)"
category: crypto
difficulty: advanced
points: 500
status: solved
flag: "FLAG{cwa2026_finals_cbc_p4dding_0r4cl3}"
tags: [padding-oracle, aes-cbc, cookie-forgery, privilege-escalation]
---

# PaddingOracle

> **TL;DR:** Combine two earlier chain secrets to log in as analyst, then use an AES-CBC padding oracle to decrypt the session cookie and forge one that decrypts to `role=admin`.

## Background (for beginners)
- **AES-CBC** encrypts in blocks; plaintext is padded to a block boundary before encryption.
- A **padding oracle** exists when a server reveals (even indirectly) whether decrypted padding is valid. Each distinct error ("Invalid padding" vs. other) leaks one bit at a time.
- With that oracle, an attacker can **decrypt** ciphertext without the key — and, running it in reverse, **forge** ciphertext that decrypts to a chosen plaintext.
- This works because CBC lacks **integrity** — nothing stops the attacker from tampering with the ciphertext.

## The Challenge
The landing page said the login is built from two earlier chain results — a **signing fragment** (`deadbeef12345678`) and a **session secret** (`cafe20261a6b72`). After logging in as analyst you get an encrypted session cookie, but the admin area rejects the analyst role.

## Key Insight 💡
Tampering with the cookie returned "Invalid padding" for some edits and different errors for others — a textbook padding oracle, meaning the cookie could be decrypted and forged without the key.

## Solution
1. **Built credentials** by combining the signing fragment `deadbeef12345678` and session secret `cafe20261a6b72` into username/password, and signed in as analyst.
2. **Obtained the encrypted session cookie**; the admin area refused the analyst role.
3. **Confirmed the oracle**: cookie edits produced "Invalid padding" vs. other errors, distinguishing valid padding from invalid.
4. **Decrypted the cookie** with the padding oracle, recovering `role=analyst`.
5. **Forged in reverse** a cookie that decrypts to `role=admin`, submitted it, and the admin area returned the flag.

## Why It Worked (the vulnerability)
AES-CBC without integrity protection, plus distinguishable padding errors, lets an attacker decrypt and forge tokens. *Defensive fix:* authenticate ciphertext (encrypt-then-MAC or AES-GCM) and return a single uniform error.

## Flag
```
FLAG{cwa2026_finals_cbc_p4dding_0r4cl3}
```

## Takeaways
- Distinguishable padding errors turn any CBC token into a decrypt/forge oracle.
- Never rely on CBC alone — add authenticated encryption and uniform error handling.

## Chain Note
Kivuli stage 8. The Kivuli set is numbered with gaps (stages 1, 5, 7, 8 here; others exist in the wider finals). **Tokens in:** `signing_fragment = deadbeef12345678` (from Kivuli 5, NestedRequest) and `session_secret = cafe20261a6b72` (from Kivuli 7, CurveBreaker) — both consumed to construct the login.
