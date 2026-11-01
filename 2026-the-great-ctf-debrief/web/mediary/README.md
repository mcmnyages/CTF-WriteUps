---
title: "Mediary"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{t4r-syml1nk-upl04d-byp4ss}"
tags: [archive-extraction, tar-symlink, path-traversal, file-disclosure]
---

# Mediary

> **TL;DR:** The upload unpacked archives and blocked `../` path escapes but not **symlinks**. A tar containing a symlink to the app's source (then to the flag file) let us read files outside the upload folder.

## Background (for beginners)
- Apps that **extract uploaded archives** (zip/tar) must treat the entries as untrusted; a malicious archive can try to write or point **outside** the intended folder.
- The obvious attack is **path traversal** (`../../etc/...`) inside entry names — many apps now block this.
- A subtler attack uses **symbolic links** stored in the archive: a symlink entry can point to any absolute path, and if the extractor follows it, reading the "uploaded" file reads the *target*.
- Dangerous because blocking `../` alone is insufficient — unsafe extraction still exposes arbitrary files.

## The Challenge
An upload feature accepts compressed files and unpacks them. It **blocks `../` path escapes** but still processes symlink entries. Tooling: browser, CLI to build a tar with symlinks.

## Key Insight 💡
The extractor filtered traversal sequences but **honored symlinks**. A symlink entry pointing outside the upload directory is read as if it were your file — so you can point it at anything on disk.

## Solution
1. **Build a tar containing a symlink** that targets the app's own source code, using a CLI that lets you add symlink entries. *Why:* `../` is blocked, but a symlink sidesteps the filter.
2. **Upload and then access the extracted symlink**, reading the app source. *Why:* following the symlink discloses the source, which revealed where the real flag file lives.
3. **Build a second tar with a symlink pointing straight at the flag file** path discovered from the source. *Why:* now you know the exact target to read.
4. **Upload and access it** to read the flag. *Why:* the extractor again follows the symlink to the flag file's contents.

## Why It Worked (the vulnerability)
Archive extraction followed symlink entries pointing outside the destination directory, so path-escape protection (`../` blocking) was bypassed. **Fix:** refuse symlink entries during extraction (or resolve and confine every entry's final path inside the destination), and extract with hardened, safe-extraction routines.

## Flag
```
FLAG{t4r-syml1nk-upl04d-byp4ss}
```

## Takeaways
- **Pattern:** unsafe archive extraction that follows symlinks = arbitrary file read.
- **Spotting it:** test archives with symlink entries, not just `../` names.
- **Fixing it:** strip/deny symlinks and confine every extracted path to the target dir.
