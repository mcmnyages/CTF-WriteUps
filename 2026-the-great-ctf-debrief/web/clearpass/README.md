---
title: "Clearpass"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: easy
points: 150
status: solved
flag: "FLAG{unb0und-r3s3t-t0k3n-t4k30v3r}"
tags: [password-reset, token-disclosure, account-takeover, information-disclosure]
---

# Clearpass

> **TL;DR:** Requesting a password reset for `admin` returned the reset code *in the HTTP response* instead of only emailing it. We used it to set a new admin password and logged in.

## Background (for beginners)
- A **password reset** flow issues a one-time secret (token/code) that should only reach the account owner, usually by email.
- If the server returns that token to whoever *requested* the reset, anyone can reset *any* account — a total **account takeover**.
- This is a form of **sensitive information disclosure**: the secret ends up in the wrong channel.
- Dangerous because it needs no cracking or guessing — the app simply hands over the keys.

## The Challenge
A login app with a "forgot password" feature. Tooling: `curl`, Python.

## Key Insight 💡
When you request a reset for `admin`, the **response body itself contains the reset code**. The token was never bound to the owner's email-only delivery, so the requester receives it directly.

## Solution
1. **Request a password reset for the `admin` account.** *Why:* this triggers token generation for the target account.
2. **Read the reset code from the response.** *Why:* the app mistakenly returns the secret that should have been emailed only.
3. **Submit the reset with the leaked code to set a new admin password.** *Why:* a valid reset token lets you choose a new password.
4. **Log in as `admin`** with the new password to retrieve the flag. *Why:* full control of the account exposes admin-only content.

## Why It Worked (the vulnerability)
The reset token was disclosed to the requester instead of being delivered solely to the account owner. **Fix:** never return reset tokens in responses; send them only through the owner's verified channel, make them single-use, short-lived, and unpredictable.

## Flag
```
FLAG{unb0und-r3s3t-t0k3n-t4k30v3r}
```

## Takeaways
- **Pattern:** reset secrets leaking into the response = instant takeover.
- **Spotting it:** inspect the reset request's response for codes, links, or tokens.
- **Fixing it:** out-of-band delivery, bound to the account, expiring and single-use.
