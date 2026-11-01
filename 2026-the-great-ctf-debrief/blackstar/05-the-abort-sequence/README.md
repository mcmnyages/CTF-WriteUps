---
title: "The Abort Sequence"
event: "The Great CTF Debrief 2026"
series: "BLACKSTAR"
category: forensics
difficulty: advanced
points: 500
status: solved
flag: "FLAG{BS05_8E78738978A1}"
tags: [pcap-carving, packet-reassembly, aes-cbc, gzip]
---

# The Abort Sequence

> **TL;DR:** Carve six real fragments out of a decoy-filled pcap, reorder them by sequence number, AES-256-CBC decrypt with a key derived from the Stage 4 abort key, then gunzip to reveal the final token.

## Background (for beginners)
- A **pcap** is a capture of network traffic; forensics often means separating real payload packets from **decoys**.
- Data split across packets arrives **out of order**; each real fragment carries a **sequence number** so you can reassemble it correctly.
- **AES-256-CBC** needs a key and an IV (initialization vector); here the IV is prepended to the ciphertext.
- Payloads are often **compressed (gzip)** after encryption, so the final step is decompression.

## The Challenge
A packet capture of 20 small UDP packets was provided. Most were decoys; the task was to find the real data, reassemble it, and decrypt the final relay token and flag.

## Key Insight 💡
Only packets marked `BSX1` to port `31337` were real (six of them); the `NTPX`-marked packets were noise meant to waste your time.

## Solution
1. **Read the pcap** and found 20 small UDP packets, most marked `NTPX` as decoys.
2. **Filtered the real fragments** marked `BSX1` destined for port `31337` — six packets, each with a sequence number.
3. **Sorted by sequence number** and concatenated the data to rebuild the encrypted blob (fragments arrived out of order).
4. **Derived the AES key** as SHA-256 of the Stage 4 abort key `14E529E26143`; split the blob into IV + ciphertext and decrypted with AES-256-CBC.
5. **Decompressed** the gzip result, revealing `RELAY_TOKEN=8E78738978A1` plus the final flag.

## Why It Worked (the vulnerability)
Sensitive data was exfiltrated over UDP where ordering and markers could be reconstructed, and the decryption key chained from a recoverable prior-stage value. *Defensive fix:* use authenticated, integrity-protected transport and keys not derivable from captured artifacts.

## Flag
```
FLAG{BS05_8E78738978A1}
```

## Takeaways
- Filter by protocol marker and destination port to cut through decoy traffic fast.
- Classic exfil pipeline to reverse: reassemble → decrypt → decompress.

## Chain Note
BLACKSTAR Stage 5 (final). **Token in:** `14E529E26143` (from Stage 4, the AES key seed). **Token out:** `8E78738978A1` — the final relay token completing the BLACKSTAR chain.
