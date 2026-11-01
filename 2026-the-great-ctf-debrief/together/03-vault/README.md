---
title: "Vault"
event: "The Great CTF Debrief 2026"
series: "Together"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{jwt-n0n3-0p3ns-th3-v4ult}"
tags: [jwt, alg-none, auth-bypass, privilege-escalation]
---

# Vault

> **TL;DR:** The app accepted a JWT with `alg: none` and an empty signature; forging a token with `role: admin` unlocked an admin-only records page containing the flag and the next portal's login.

## Background (for beginners)
- A JWT (JSON Web Token) has three parts: header, payload, signature. The header names the signing algorithm.
- The `none` algorithm means "no signature" — it was meant for already-trusted contexts, but servers that accept it from clients let anyone forge tokens.
- If a server trusts the header's `alg` blindly, an attacker can set `alg: none`, change the payload (e.g. `role: admin`), and send an empty signature.
- Fix in one line: pin the expected algorithm server-side and reject `none`.

## The Challenge
Portal 3 of the Together chain. After logging in with Vault credentials recovered from Mailer, you receive a JWT with `role: viewer`. A records page is admin-only. Tools: curl, Python.

## Key Insight 💡
The token's header **states its own signing method**, and the server honored it — so declaring `alg: none` tells the server to skip signature verification entirely.

## Solution
1. **Log in with Mailer's credentials** and capture the issued JWT (role `viewer`). (WHY: the chain supplies this portal's login from the previous one.)
2. **Forge a new token** with header `alg: none`, payload `role: admin`, and an empty signature. (WHY: `none` disables verification, so the forged claims are accepted.)
3. **Replay the forged token** against the admin-only records page; the server accepted it and returned the flag plus the Portal 4 (Fetcher) login. (WHY: privilege escalation unlocks the gated data.)

## Why It Worked (the vulnerability)
The server validated tokens using the algorithm named in the attacker-controlled header, accepting `alg: none` and skipping signature checks. **Fix:** hard-code the accepted algorithm (e.g. HS256/RS256) server-side and reject tokens declaring `none`.

## Flag
```
FLAG{jwt-n0n3-0p3ns-th3-v4ult}
```

## Takeaways
- Never let the token decide how it is verified — the server must pin the algorithm.
- `alg: none` and algorithm-confusion are classic, high-impact JWT flaws.
- Always test role/claim tampering when a token gates access.

## Chain Note
**Together** is a 5-portal chain where each portal hands over the next portal's login. Vault receives Mailer's leaked credentials as input and outputs the flag plus Portal 4 (Fetcher) credentials from the admin-only records page.
