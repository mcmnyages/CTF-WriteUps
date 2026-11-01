---
title: "Receipts"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: easy
points: 150
status: solved
flag: "FLAG{l3dg3rly-s3ttl3m3nt-id0r}"
tags: [idor, access-control, authorization, broken-access-control]
---

# Receipts

> **TL;DR:** Receipt IDs were just encoded `accountname + number` strings. Rebuild the ID for another account and the app serves that account's receipt with no ownership check — classic IDOR.

## Background (for beginners)
- **IDOR** (Insecure Direct Object Reference) happens when an app exposes a reference to a record (an ID) and trusts whoever asks for it, without checking they own it.
- "Encoded" is not "secured." Base64 or similar encodings scramble text but anyone can decode and re-encode them.
- The real defense is an **authorization check** on the server: does *this* logged-in user own *this* object?
- IDOR is dangerous because it lets any authenticated user read or change other people's data at scale.

## The Challenge
You are logged in as a `demo` user with access to your own receipts. Each receipt is fetched by an opaque ID that looks random. Tooling: `curl`.

## Key Insight 💡
The "opaque" receipt ID was only **encoded text**. Decoding one of your own IDs revealed it was simply your account name plus a number. If you can read the format, you can forge it for any account.

## Solution
1. **Capture your own receipt ID** from the app while browsing as `demo`. *Why:* we need a real sample to understand the format.
2. **Decode the ID.** It turned out to be `accountname` + a number. *Why:* this reveals the ID is predictable, not a secret.
3. **Build the same ID for a different important account** by substituting that account's name and the relevant number, then re-encoding it the same way. *Why:* if the server doesn't check ownership, a valid-looking ID is all it needs.
4. **Request that forged receipt** with `curl`. The app returned the other account's receipt without verifying ownership. *Why:* no access-control check means the forged reference is honored. The flag was in the response.

## Why It Worked (the vulnerability)
The server resolved a receipt purely from its (decodable, forgeable) ID and never confirmed that the requesting session owned that receipt. **Fix:** on every receipt fetch, verify the receipt belongs to the authenticated user (server-side authorization), and never rely on encoding as a secret.

## Flag
```
FLAG{l3dg3rly-s3ttl3m3nt-id0r}
```

## Takeaways
- **Pattern:** predictable/encoded object references + no ownership check = IDOR.
- **Spotting it:** decode any "random" ID; if it contains meaningful fields, try changing them.
- **Fixing it:** enforce per-object authorization server-side; treat IDs as untrusted input.
