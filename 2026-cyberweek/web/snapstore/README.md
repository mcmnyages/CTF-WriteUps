---
title: "Snapstore"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{p4th-tr4v3rs4l-d0t-d0t-pwn}"
tags: [path-traversal, sanitisation-bypass, lfi, filter-bypass]
---

# Snapstore

> **TL;DR:** A file-serving endpoint stripped `../` exactly once; sending `....//` collapsed back into `../` after that single pass, escaping the public folder into a private one to read the real license key.

## Background (for beginners)
- **Path traversal** uses sequences like `../` in a filename to climb out of an intended directory and read files elsewhere.
- Servers often "sanitise" by deleting `../` from the input, but a **single, non-recursive** replacement is easy to defeat.
- The trick: craft input that *becomes* `../` only after the removal runs once.

## The Challenge
The site serves files from a public folder by name. Private license keys live in a separate private folder next to it, and the public flag file is a decoy. Attempts to climb out with `../` fail because the app removes `../` from the filename.

## Key Insight 💡
The app removes `../` only once (non-recursively). The string `....//` contains an embedded `../`; deleting that one occurrence leaves the surrounding characters forming a fresh `../`. One-pass sanitisation reconstructs exactly what it tried to remove.

## Solution
1. Request a normal file and confirm files are served by name from the public folder. *Why: establishes the sink and base directory.*
2. Try `../` — rejected/removed. *Why: identifies the sanitiser.*
3. Submit `....//` as part of the path. *Why: after the single removal of the inner `../`, the leftover collapses to `../`, giving real traversal.*
4. Point the traversed path at the private folder's real key file. *Why: the decoy is in the public folder; the real flag is in the sibling private folder.*

## Why It Worked (the vulnerability)
The filter did a single-pass string replacement of `../` instead of fully canonicalising the path, so `....//` survived as `../`. **Fix:** resolve the path to an absolute real path and verify it stays within the allowed base directory; never rely on string stripping.

## Flag
```
FLAG{p4th-tr4v3rs4l-d0t-d0t-pwn}
```

## Takeaways
- One-pass "remove the bad substring" sanitisers are defeated by overlapping/nested payloads (`....//`).
- Always normalise then validate the final resolved path against an allowlisted root.
- The obvious flag file is often a decoy — the sibling private directory is the target.
