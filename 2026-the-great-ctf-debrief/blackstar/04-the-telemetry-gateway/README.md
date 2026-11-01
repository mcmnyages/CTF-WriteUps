---
title: "The Telemetry Gateway"
event: "The Great CTF Debrief 2026"
series: "BLACKSTAR"
category: web
difficulty: hard
points: 450
status: solved
flag: "FLAG{BS04_14E529E26143}"
tags: [hash-length-extension, sha256, mac-forgery, privilege-escalation]
---

# The Telemetry Gateway

> **TL;DR:** The gateway authenticates clearance tokens with a `SHA-256(secret || data)` tag; a hash length extension attack appends `;clearance=operator` and forges a valid tag without the secret.

## Background (for beginners)
- A **MAC** proves a message is authentic. A naive construction, `SHA-256(secret || data)`, is insecure.
- **Hash length extension** exploits how SHA-256 works: knowing `hash(secret||data)` and the length of `secret`, an attacker can compute `hash(secret||data||padding||extra)` — a valid tag for a *longer* message — without ever knowing the secret.
- The attacker doesn't learn the secret; they only need its length, which can be brute-forced.
- Correct MACs use **HMAC**, which is immune to this.

## The Challenge
A telemetry gateway issues a signed clearance token and will only release the abort key to an **operator** clearance. The issued token carried `station=NBO;clearance=viewer` with a SHA-256 tag.

## Key Insight 💡
The tag was `SHA-256(secret || data)` — the classic vulnerable MAC — so a new field could be appended and re-authenticated via length extension.

## Solution
1. **Inspected the token**: data `station=NBO;clearance=viewer` plus a SHA-256 tag computed as hash of secret joined to data — presenting the Stage 3 token to obtain it.
2. **Recognized the vulnerable MAC** form and set up a hash length extension attack to append `;clearance=operator`.
3. **Brute-forced the secret length** (needed for correct SHA-256 padding); length **23** produced a tag the server accepted.
4. **Submitted the forged token**, and the server returned the abort key `14E529E26143`.

## Why It Worked (the vulnerability)
`SHA-256(secret || data)` leaks enough internal state to extend the message and forge a tag. *Defensive fix:* use `HMAC-SHA256` instead of a raw secret-prefixed hash.

## Flag
```
FLAG{BS04_14E529E26143}
```

## Takeaways
- Any secret-prefixed hash MAC is forgeable via length extension — a red flag in any protocol.
- Spot it when a tag looks like `hash(secret + data)` and the server accepts extended messages; fix by switching to HMAC.

## Chain Note
BLACKSTAR Stage 4. **Token in:** `0D9E75EA984A` (from Stage 3, to obtain the clearance token). **Token out (abort key):** `14E529E26143` (feeds Stage 5, The Abort Sequence).
