---
title: "The Compromised Briefing"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: forensics
difficulty: hard
status: solved
flag: "FLAG{fin_ws_07_jkamau_app_06_sync_cache_net}"
tags: [dfir, evidence-integrity, hash-allowlist, attack-reconstruction]
---

# The Compromised Briefing

> **TL;DR:** Evidence files were validated against an approved-file hash list (two untrusted files discarded), then the attack path was reconstructed across the approved spreadsheet, a marked-up image, and a firewall log to assemble the flag from four pivot points.

## Background (for beginners)
- **DFIR (Digital Forensics & Incident Response)** reconstructs what an attacker did by correlating multiple evidence sources into a single timeline.
- **Evidence integrity** matters first: before trusting a file, verify it matches a known-good hash so you aren't reasoning over tampered or planted data.
- **SHA-256 hashing** produces a fixed fingerprint; comparing it to an official allowlist proves a file is the approved one.
- An **attack path** typically moves from an initial foothold, to a compromised account, to the system used for data theft, and finally to an external exfiltration destination.

## The Challenge
Several evidence files were provided along with an official list of approved files (by hash). The goal was to reconstruct the intrusion and build the flag from the key artifacts — but not every file could be trusted.

## Key Insight 💡
**Verify before you trust.** Two files were not on the approved hash list; treating them as evidence would poison the analysis. Only the approved spreadsheet, image, and firewall log drive the answer.

## Solution
1. **Hash every evidence file with `sha256sum` and compare against the approved list.** *Why:* two files did not match and were discarded as untrustworthy — they were decoys or tampered artifacts.
2. **Using the approved spreadsheet and the analyst's marked-up image, find the first infected computer.** *Why:* this is the initial foothold — `fin_ws_07`.
3. **Trace from that host to the stolen account.** *Why:* the attacker pivoted via a compromised credential — `jkamau`.
4. **Follow the account to the computer used to steal the data.** *Why:* this is the staging/exfil host — `app_06`.
5. **Inspect the approved firewall log for the one destination outside the company network.** *Why:* the lone external destination is the exfiltration endpoint — `sync_cache_net`.
6. **Combine the four pivots in order:** first host, stolen account, second host, external destination. *Why:* that is the flag format, giving `fin_ws_07_jkamau_app_06_sync_cache_net`.

## Why It Worked (the vulnerability / technique)
The exercise rewards disciplined DFIR: integrity verification (a hash allowlist rejecting planted evidence) followed by cross-source attack-path reconstruction. **Defensive note:** maintain cryptographic manifests for evidence chains, and alert on any outbound connection to destinations outside your known network ranges.

## Flag
```
FLAG{fin_ws_07_jkamau_app_06_sync_cache_net}
```

## Takeaways
- Always validate evidence integrity before analysis — untrusted files can mislead the whole investigation.
- Correlating independent sources (spreadsheet, image, firewall log) builds a defensible timeline.
- The single outbound anomaly in a firewall log often marks the exfiltration point.
