---
title: "Remote-Access Policy Violation"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: forensics
difficulty: easy
status: solved
flag: "FLAG{6A-3C-9F-1B}"
tags: [soc-triage, access-policy, network-log, policy-compliance]
---

# Remote-Access Policy Violation

> **TL;DR:** Comparing a network activity log against the remote-access policy surfaced four non-compliant connections; mapping each to its device tag and ordering them by time produced the flag.

## Background (for beginners)
- A **remote-access policy** defines which devices, destinations, ports, or time windows are permitted for connecting into or out of a network.
- **SOC triage** often means comparing observed traffic against that policy to spot what should not have happened.
- A **device tag** is a short identifier assigned to each endpoint, letting analysts tie a connection back to a specific machine.
- Violations become meaningful as a sequence — ordering them by time reconstructs the order of events.

## The Challenge
An access policy, a device list, and a network activity log were all provided in a signed-in browser. The task was to find connections that violated the policy and build the flag from them.

## Key Insight 💡
The flag is built only from **rule-breaking** connections. Each violation maps to a **device tag**, and the tags must be read in **time order**.

## Solution
1. **Open the access policy, device list, and network activity log in a signed-in browser.** *Why:* all three are needed — the policy defines "allowed," the log shows "actual," and the device list provides the tags.
2. **Compare each network connection to what the policy permits.** *Why:* only deviations from the policy count as violations.
3. **Identify the four connections that broke the rules.** *Why:* these are the flag-bearing events.
4. **Match each violating connection to its device tag, then sort by timestamp.** *Why:* chronological ordering of the tags yields `6A-3C-9F-1B`.

## Why It Worked (the vulnerability / technique)
This is straightforward policy-vs-traffic comparison, the backbone of SOC monitoring. Any connection outside the permitted set is a candidate incident. **Defensive note:** encode the access policy as automated detection rules so violations alert in real time rather than requiring manual log review.

## Flag
```
FLAG{6A-3C-9F-1B}
```

## Takeaways
- Effective triage requires the policy (expected) and the log (observed) side by side.
- Device tags turn anonymous connections into attributable events.
- Time ordering converts a set of violations into a coherent incident narrative.
