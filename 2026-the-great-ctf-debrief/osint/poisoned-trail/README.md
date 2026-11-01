---
title: "The Poisoned Trail"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: osint
difficulty: medium
points: 250
status: solved
flag: "FLAG{alice_smith}"
tags: [osint, digital-signature, decoy-evidence, cryptographic-verification]
---

# The Poisoned Trail

> **TL;DR:** Chat logs and a blog post framed one person as a decoy; verifying the photo's digital signature against every available key found exactly one match, which belonged to a *different* employee — the real culprit.

## Background (for beginners)
- **OSINT (Open-Source Intelligence)** gathers clues from public artifacts — chats, blogs, photos, staff lists — and pieces them into a conclusion.
- **Digital signatures** let anyone verify that a file was produced by the holder of a specific private key; verification succeeds with only the matching key.
- A **false trail (decoy)** is planted evidence meant to point investigators at the wrong person.
- The lesson: **circumstantial narrative** can be fabricated, but a valid **cryptographic signature** is hard evidence that resists manipulation.

## The Challenge
An archive unpacked into chat logs, a blog post, a photo, a digital signature, a staff list, and several keys. The chat log and blog post both named one person — but the story felt too convenient, like a plant.

## Key Insight 💡
Ignore the narrative. The photo's signature can be verified against the key set, and **only the key that actually verifies** identifies the true author — who turns out to be someone other than the framed person.

## Solution
1. **Download and unpack the evidence** (chat logs, blog post, photo, signature file, staff list, keys). *Why:* you need every key and the signed photo together to test them.
2. **Read the chat log and blog post** — both implicate one named individual. *Why:* recognizing this as the obvious, planted lead is what prompts skepticism.
3. **Verify the photo's digital signature against each candidate key** (e.g., with OpenSSL). *Why:* a signature validates against exactly one key; this is objective proof of authorship.
4. **Only one key matches.** Map that key back to the staff list. *Why:* the matching key belongs to a **different** employee than the one the narrative accused.
5. **Report that employee as the answer** → `alice_smith`. *Why:* cryptographic proof overrides the circumstantial framing.

Illustrative verification step (pseudocode):
```
for key in keys:
    if openssl_verify(photo, signature, key) == OK:
        suspect = lookup(key, staff_list)   # the one true match
```

## Why It Worked (the vulnerability / technique)
The challenge pits persuasive but forgeable narrative evidence against unforgeable cryptographic proof. The decoy succeeds only if you stop at the story. **Defensive/analytic note:** when signatures are available, let them arbitrate attribution — trust cryptographic proof over circumstantial evidence.

## Flag
```
FLAG{alice_smith}
```

## Takeaways
- Treat conveniently obvious evidence with suspicion; it may be planted.
- A valid digital signature is decisive attribution — verify it against every available key.
- Cross-reference the verified key against authoritative records (the staff list) to name the real actor.
