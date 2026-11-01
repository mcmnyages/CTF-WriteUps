---
title: "The Archive Room"
event: "The Great CTF Debrief 2026"
series: "Heritage Trail"
category: osint
difficulty: medium
points: 400
status: solved
flag: "FLAG{A17F09}"
tags: [osint, forensics, hash-verification, pdf-metadata]
---

# The Archive Room

> **TL;DR:** Identify the Taveta Chronicle from a historical clue, verify four PDFs against a SHA-256 manifest to find the single genuine one, then read two identifiers (BOX + FRAME) from its metadata.

## Background (for beginners)
- A **cryptographic hash** (SHA-256) is a fingerprint of a file. If the file changes by one byte, the hash changes completely — so a manifest of approved hashes lets you detect tampering.
- **File metadata** (author, custom fields in a PDF) can carry hidden data independent of the visible content.
- Core lesson: **trust the hash, not the filename or title** — attackers rename files and forge titles freely.

## The Challenge
A clue described a publication that first appeared in 1895, printed at Mahoo, Taveta. You were given four PDFs plus an integrity manifest of approved SHA-256 hashes, and had to extract a flag from the right one.

## Key Insight 💡
Filenames and document titles are untrustworthy. Only the SHA-256 manifest tells you which files are authentic, and only one of those actually matches the historical publication — the flag lives in *its* metadata.

## Solution
1. **Identify the publication** — first appeared 1895, printed at Mahoo, Taveta = the **Taveta Chronicle**, Kenya's first newspaper.
2. **Verify integrity**: hash all four PDFs with `sha256sum` and compare to the manifest. `record_02` is *not* on the list → untrusted, despite a convincing title.
3. **Narrow the trusted set**: of the three that match, only `record_03` is the genuine Taveta Chronicle document.
4. **Read its metadata** with a Python PDF-metadata reader — it holds two identifiers, `BOX` and `FRAME`. Join the values to form the flag.

## Flag
```
FLAG{A17F09}
```

## Takeaways
- Verify first, read second: hash-check before trusting any supplied document.
- A matching title/filename proves nothing; a matching hash on the manifest does.
- PDF metadata is a classic hiding spot — always dump it.

## Chain Note
Stage 5 (medium, OSINT/forensics). The answer `A17F09` is pivotal: in HT7 the earlier answers reveal that `A17F09` is *the filename* of the final data file to read, so this stage's flag doubles as a target reference downstream.
