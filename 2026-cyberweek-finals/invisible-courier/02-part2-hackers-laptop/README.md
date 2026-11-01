---
title: "Hacker's Laptop — Part 2"
event: "CyberWeek 2026"
series: "Invisible Courier"
category: forensics
difficulty: HARD
points: 400
status: unsolved
flag: "unsolved"
tags: [dfir, file-signature, disk-image, carving]
---

# Hacker's Laptop — Part 2

> **TL;DR:** A disguised file on the suspect's laptop image has a mismatched signature/extension; find it, identify its true type, and locate the credential needed to open it. Currently unsolved.

## Background (for beginners)
- Files carry **magic bytes** (a signature at the start) that reveal their true type regardless of the extension on the name.
- Attackers hide data by **renaming** files so the extension lies about the content — a file-signature vs extension mismatch exposes it.
- **Encrypted/password-protected containers** (archives, encrypted volumes) need a key or password, which is often stashed elsewhere on the same disk.
- Tools like **The Sleuth Kit** (`fls`, `icat`), **Autopsy**, `file`, and `binwalk` let you enumerate, extract, and fingerprint files inside a raw disk image.

## The Challenge
"The suspect tried to hide another file by making it look like something it isn't. Find it, work out what it really is, and track down what you need to open it."

Download: a Google Drive zip (the same image as Part 1). Extract the zip first; the image inside is `laptop_work.001`.

- Image SHA256: `e901f026abe19b5b4fe0108d140c7486e91110db56a8ea1bd58e785515fb897d`
- Suggested tools: Autopsy or The Sleuth Kit
- Flag format: `FLAG{...}`

## Key Insight 💡
The hint points squarely at a **file-signature/extension mismatch** — a disguised file whose magic bytes disagree with its name. The file is likely an encrypted or password-protected container, and the password/key must be tracked down elsewhere on the disk.

## Status: Unsolved
**What is known**
- The artifact is a single disguised file hidden among normal laptop content on `laptop_work.001`.
- Its extension is expected to be misleading; the real type should be determined by its header/magic bytes.
- Opening it will almost certainly require a password or key stored somewhere else in the image.

**Suggested approach**
1. Verify the download: confirm the extracted image's SHA256 equals `e901f026...fb897d` before analysis. *Why: ensures you are working on the intended, intact image.*
2. Enumerate files: run `fls` (and recursively) over `laptop_work.001` to list all entries, including deleted ones.
3. Fingerprint everything: `icat` suspicious files out and run `file` / inspect magic bytes to find where the true type disagrees with the extension.
4. Carve for hidden/embedded data: run `binwalk` and signature-based carving to surface containers that are not obvious as named files.
5. Identify the container: once the real type is known (e.g. an archive or encrypted volume), note what credential it demands.
6. Hunt the key material: search the disk for passwords, keyfiles, notes, browser/credential stores, or chat logs; correlate with Part 1's case context.
7. Open and extract the flag once the true file and its password are reunited.

## Why It Matters (the technique)
Extension-based trust is unreliable; true identification relies on content signatures. **Defensive note:** validate file types by magic bytes, not names, and monitor for renamed/disguised containers.

## Flag
```
unsolved
```

## Takeaways
- Never trust an extension — magic bytes reveal what a file really is.
- Disguised containers usually pair with a password hidden elsewhere; solve both halves.
- Signature carving (binwalk/TSK) surfaces data that directory listings hide.

## Chain Note
Part 2 of **The Invisible Courier**, continuing on the same disk image as Part 1 ("The Vanishing Trace").
