---
title: "Sealbox"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{cbc-p4dd1ng-0r4cl3-f0rg3d-s34l}"
tags: [crypto, padding-oracle, aes-cbc, token-forgery]
---

# Sealbox

> **TL;DR:** The encrypted "seal" cookie leaked distinct bad-padding vs. wrong-content errors — an AES-CBC padding oracle; it was used to decrypt the token and then, in reverse, to forge a seal decrypting to `{"u":"guest","r":"admin"}`, unlocking the vault.

## Background (for beginners)
- **AES-CBC** without integrity protection is malleable: flipping ciphertext bytes predictably changes the decrypted plaintext.
- A **padding oracle** exists when the server reveals whether decryption produced valid padding, distinct from other errors.
- That one bit per guess lets an attacker both **decrypt** ciphertext and **forge** new ciphertext that decrypts to chosen plaintext — no key needed.

## The Challenge
You sign in and receive a "seal" cookie (an encrypted token). The vault releases its document only to a seal with the admin role. Slightly altering the seal produces two different errors: one for bad padding, one for readable-but-wrong content.

## Key Insight 💡
Two distinguishable errors = a padding oracle. The "bad padding" vs. "wrong content" distinction tells you, byte by byte, when your tampered ciphertext decrypts to valid PKCS#7 padding, which is enough to recover plaintext and to craft arbitrary plaintext.

## Solution
1. Capture the seal cookie and confirm two distinct error responses to tampering. *Why: proves a padding oracle (CBC, no integrity check).*
2. Run a standard padding-oracle decryption against the oracle. *Why: recovers the plaintext — `{"u":"guest","r":"user"}`.*
3. Run the oracle in reverse (encryption/forging mode) to build a ciphertext decrypting to `{"u":"guest","r":"admin"}`. *Why: the vault keys off the admin role; forging avoids needing the key.*
4. Send the forged seal cookie to the vault. *Why: the server decrypts it to the admin token and grants access.*

## Solver sketch (illustrative pseudocode)
```
plain  = padding_oracle_decrypt(seal, oracle)      # -> {"u":"guest","r":"user"}
forged = padding_oracle_encrypt('{"u":"guest","r":"admin"}', oracle)
GET /vault  with Cookie: seal=forged
```

## Why It Worked (the vulnerability)
CBC ciphertext had no integrity/authentication and the server distinguished padding errors, giving an oracle to decrypt and forge tokens. **Fix:** use authenticated encryption (AES-GCM or encrypt-then-MAC) and return a single uniform error on any decryption failure.

## Flag
```
FLAG{cbc-p4dd1ng-0r4cl3-f0rg3d-s34l}
```

## Takeaways
- Distinct crypto error messages are a leak — always fail uniformly.
- Unauthenticated CBC is forgeable; a padding oracle gives both decrypt and encrypt.
- Use AEAD (GCM) or encrypt-then-MAC, never raw CBC for tokens.
