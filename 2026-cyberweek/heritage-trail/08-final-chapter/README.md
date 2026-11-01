---
title: "Final Chapter"
event: "CyberWeek 2026"
series: "Heritage Trail"
category: forensics
difficulty: basic
points: 200
status: solved
flag: "FLAG{MANY_PATHS_ONE_LAND}"
tags: [forensics, aes-zip, password-protected-archive, chained-challenge]
---

# Final Chapter

> **TL;DR:** The HT7 answer `KENYA-HERITAGE` is the password to an AES-encrypted ZIP; open it (with an AES-capable tool) and the flag is in the final note inside.

## Background (for beginners)
- A **password-protected ZIP** can use legacy ZipCrypto or stronger **AES** encryption. AES archives won't open with every tool — you need one that supports AES (e.g. `7-Zip`, or `pyzipper` in Python).
- **Key reuse across stages** is the whole point of a chained CTF: the answer to one puzzle is the credential for the next.
- Forensics here is simple once you have the key — the challenge is recognizing *where* the key came from.

## The Challenge
The download was a password-protected ZIP. No password was given directly — it had to come from the previous challenge.

## Key Insight 💡
The password isn't hidden in this file at all — it's the HT7 flag content, `KENYA-HERITAGE`. The archive uses AES, so a standard unzip may fail; use an AES-aware extractor.

## Solution
1. **Use the previous answer as the password**: `KENYA-HERITAGE`.
2. **Open the AES-encrypted ZIP** with a tool/script that supports AES (standard ZipCrypto handlers may reject it).
3. **Read the contents** — two notes inside; the final note holds the flag.

*Illustrative* pseudocode:
```
import pyzipper
with pyzipper.AESZipFile("final.zip") as z:
    z.setpassword(b"KENYA-HERITAGE")
    z.extractall()
```

## Flag
```
FLAG{MANY_PATHS_ONE_LAND}
```

## Takeaways
- If an archive refuses a correct-looking password, suspect AES and switch tools.
- In chained events, always try the previous flag/answer as the next credential.
- The flag `MANY_PATHS_ONE_LAND` echoes HT1's opening theme ("many paths, one country"), closing the loop.

## Chain Note
Stage 8 is the finale of the eight-part Heritage Trail. The chain terminates here: `KENYA-HERITAGE` (built from all six core answers in HT7) is the AES key, and the archive yields the capstone flag that ties the whole series back to its HT1 premise.
