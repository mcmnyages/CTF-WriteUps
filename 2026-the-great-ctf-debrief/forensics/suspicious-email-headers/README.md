---
title: "Suspicious Email Headers"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: forensics
difficulty: easy
status: solved
flag: "FLAG{17-44-63}"
tags: [email-security, phishing, spf-dkim-dmarc, header-analysis]
---

# Suspicious Email Headers

> **TL;DR:** Each email was scored against four spoofing warning signs; the three emails with two or more red flags were flagged suspicious, and their case numbers in send order formed the flag.

## Background (for beginners)
- **Email headers** record the real path and identity claims behind a message — the sending domain, the reply-to address, and the results of authentication checks.
- **SPF/DKIM/DMARC** are standard sender-authentication mechanisms; a failure suggests the message may not truly come from the domain it claims.
- **Spoofing and phishing triage** looks for mismatches: a lookalike sender domain, a reply address pointing somewhere unexpected, or failed authentication.
- No single flag is conclusive — analysts weigh multiple signals together before calling a message malicious.

## The Challenge
A set of emails and a list of trusted domains were provided, both viewable in a signed-in browser. The task was to decide which emails were suspicious based on their headers.

## Key Insight 💡
Judge by **accumulated** warning signs, not a single tell. An email with **two or more** of the four red flags is suspicious; one flag alone is noise.

## Solution
1. **Open the email headers and the trusted-domain list in a signed-in browser.** *Why:* the comparison against trusted domains is only meaningful with the allowlist in hand.
2. **Check each email against four warning signs:** a sender domain that looks fake (not on the trusted list), a reply address that doesn't match the sender, and failed sender authentication checks. *Why:* these are the classic indicators of spoofing/phishing.
3. **Mark any email with two or more warning signs as suspicious.** *Why:* the two-flag threshold filters out benign anomalies.
4. **Three emails crossed the threshold; order their case numbers by send time** and concatenate. *Why:* chronological order yields `17-44-63`.

## Why It Worked (the vulnerability / technique)
This mirrors real SOC email triage: SPF/DKIM/DMARC results plus domain and reply-to consistency reveal spoofed senders. **Defensive note:** enforce DMARC with a `reject` policy and alert on reply-to/from mismatches to catch these automatically.

## Flag
```
FLAG{17-44-63}
```

## Takeaways
- Combine signals; a multi-factor threshold reduces false positives.
- Authentication results in headers are among the strongest anti-spoofing evidence.
- Always anchor "looks fake" judgments against an authoritative trusted-domain list.
