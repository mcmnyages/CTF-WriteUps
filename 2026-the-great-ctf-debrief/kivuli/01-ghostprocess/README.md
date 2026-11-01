---
title: "GhostProcess"
event: "The Great CTF Debrief 2026"
series: "Kivuli (cwa2026 finals)"
category: forensics
difficulty: medium
points: 400
status: solved
flag: "FLAG{cwa2026_finals_5eefb85fb2f96b1f}"
tags: [memory-forensics, fileless-malware, process-injection, xor]
---

# GhostProcess

> **TL;DR:** A fileless implant lives in `svchost.exe`'s memory; its XOR-scrambled C2 URL is recovered by brute-forcing all 256 single-byte keys, and SHA-256 of that URL yields the flag.

## Background (for beginners)
- **Memory forensics** analyzes a RAM snapshot to find malware that may never touch disk.
- **Fileless malware** runs entirely in memory, often **injected** into a trusted process so it blends in.
- A key tell is **executable memory with no backing file** — legitimate code is normally backed by a file on disk.
- **Single-byte XOR** is weak obfuscation: only 256 possible keys, so you can try them all and keep the one producing readable output.

## The Challenge
A memory image was provided. Somewhere in it, malware had hidden a command-and-control (C2) URL, and the flag is derived from that URL.

## Key Insight 💡
`svchost.exe` (PID 1448) had runnable memory with **no backing file** — a hallmark of code injection — and the hidden URL inside was only lightly XOR-obfuscated.

## Solution
1. **Listed readable strings** in the image (processes, scan results, network connections, leftover data) to get oriented.
2. **Flagged `svchost.exe` PID 1448**: runnable memory with no backing file, which had spawned `cmd.exe` and held an open HTTPS connection — classic injection behavior.
3. **Located an injected program** inside that memory block containing a scrambled text segment.
4. **Brute-forced the XOR key**: the scramble used a single one-byte key; trying all 256 produced exactly one valid URL — `https://c2.apt-ke-009.net/beacon/checkin`.
5. **Hashed the URL** with SHA-256 and took the first 16 characters for the flag body.

## Why It Worked (the vulnerability)
Injecting code into a trusted process evades file-based scanners, but the in-memory implant still leaves detectable signatures (no-file executable regions, weak XOR). *Defensive fix:* deploy memory-scanning EDR that flags unbacked executable regions in trusted processes.

## Flag
```
FLAG{cwa2026_finals_5eefb85fb2f96b1f}
```

## Takeaways
- Unbacked executable memory in a system process is a strong fileless-malware indicator.
- Single-byte XOR is brute-forceable in 256 tries — validate hits by looking for readable structure (like a URL).

## Chain Note
Kivuli stage 1. The Kivuli finals set is numbered with gaps (stages 1, 5, 7, 8 appear in this debrief); other stages exist in the wider finals but are not covered here. This stage is standalone and does not emit a token consumed by the others documented here.
