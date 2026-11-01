---
title: "Keymaster"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{jku-h34d3r-by0k-jwks-f0rg3ry}"
tags: [jwt, jku-injection, jwks-forgery, rs256, access-control]
---

# Keymaster

> **TL;DR:** RS256 session tokens trusted any `jku` URL on the Keymaster domain, which also serves user content; publishing your own JWKS via the branding feature and pointing a forged `role=admin` token's `jku` at it let the server verify your signature and release the vault flag.

## Background (for beginners)
- A **JWT** is a signed token; with **RS256** the server verifies it using a public key, often fetched from a URL named in the token's `jku` header.
- If the server trusts any `jku` URL on its own domain but that domain also hosts user-uploaded content, an attacker can publish their own public key and have the server trust it.
- The attacker signs a forged token with their matching private key — **JWKS forgery / bring-your-own-key**.

## The Challenge
You sign in as guest. The session token is RS256 and its header's `jku` points to a key list hosted on the Keymaster domain. The vault page refuses non-admins. A "publish a branding pack" feature saves your content and serves it back from that same Keymaster domain.

## Key Insight 💡
The `jku` check only requires the URL to be on the Keymaster domain — but the branding feature lets *you* serve arbitrary content from that domain. So you can host your own public key there, satisfying the domain trust while controlling the key.

## Solution
1. Decode the guest token; note RS256 and a `jku` pointing at a key list on the Keymaster domain. *Why: identifies the verification mechanism and trust rule.*
2. Generate your own RSA key pair. *Why: you need a key whose public half the server will trust and whose private half you hold.*
3. Publish the public key formatted as a JWKS key list via the branding feature. *Why: this gives you a key-list URL on the trusted Keymaster domain.*
4. Build a token with `role=admin`, set its `jku` header to your published key-list URL, and sign it with your private key. *Why: the forged claims plus your signature will verify against your published key.*
5. Send the forged token to the vault. *Why: the server fetches your key from the trusted domain, verifies the signature, and treats you as admin.*

## Solver sketch (illustrative pseudocode)
```
priv, pub = rsa_generate()
jwks_url = branding_publish(jwks_from(pub))
token = jwt_sign({"role":"admin"}, priv, alg=RS256, header={"jku": jwks_url})
GET /vault  with Authorization: token
```

## Why It Worked (the vulnerability)
The server trusted any `jku` URL on its own domain, but that domain served user-controlled content, so an attacker-published key verified an attacker-forged token. **Fix:** pin verification to a fixed, server-controlled key/JWKS; never fetch keys from a user-writable origin, and allowlist exact `jku` URLs.

## Flag
```
FLAG{jku-h34d3r-by0k-jwks-f0rg3ry}
```

## Takeaways
- `jku`/`jwks` headers are attacker-controlled hints — never trust them by domain alone.
- User-uploadable content on a trusted domain collapses "same-domain" trust.
- Pin JWT keys server-side; don't fetch verification keys from token headers.
