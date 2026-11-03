---
title: "IntroToBurp"
event: "picoCTF 2024"
series: "Standalone"
category: web
difficulty: easy
points: 100
status: solved
solved_with: team
author: "Silas"
date: 2026-03-31
flag: "[FLAG HIDDEN]"
tags: [burpsuite, 2fa, web]
live: auto
---
<!--
  HOW TO USE THIS FILE
  - This is the standard shape for EVERY writeup in the repo, so they all look the same.
  - Fill in the frontmatter block (between the --- lines) — the index tables are built from it.
  - Replace the <...> placeholders. Delete any OPTIONAL section you don't need.
  - LIVE CTF? Write the real flag normally; `python ctf.py` hides it automatically.
  - When done, run `python ctf.py` from the CTFs/ folder to rebuild the indexes.
-->

# IntroToBurp

> **TL;DR:** Register an account, intercept the 2FA/OTP verification request using Burp Suite, and clear out the `otp` parameter value to bypass improper server-side validation and capture the flag.

## Background (for beginners)
- **What is Burp Suite?** An essential web application security testing tool that acts as an intercepting HTTP/HTTPS proxy, letting you view, modify, and replay web traffic between your browser and the target server.
- **Why is Parameter Tampering dangerous?** It occurs when an application blindly trusts user-supplied input or fails to properly handle missing/malformed parameters, allowing attackers to manipulate request fields to bypass authorization checks or multi-factor authentication (2FA).

## The Challenge
The challenge provides a web application featuring a registration form followed by a two-factor authentication (2FA) prompt. The goal is to use Burp Suite to analyze and manipulate the HTTP requests sent during the login/verification process.

## Key Insight 💡
The server-side code handles the 2FA verification poorly. Instead of securely verifying whether a valid numerical OTP was entered and cryptographically checking session states, it fails open or accepts a blank/malformed parameter (`otp=`) without throwing an error, directly returning the flag.

## Solution
1. **Initial Setup and Registration:** Open the target challenge website via your browser (configured to route traffic through Burp Suite proxy). Fill out the registration form with arbitrary details and click **Register**.
2. **Reaching the OTP Page:** You will be redirected to a 2FA prompt asking for a One-Time Password. Enter a dummy code (e.g., `123456`) and submit it, which results in an "Invalid OTP" message.
3. **Intercepting the Request:** Turn **Intercept is ON** in Burp Suite (`Proxy` tab). Re-submit the OTP page request from your browser.
4. **Modifying the Parameters:** In Burp Suite, look at the intercepted `POST` request to `/dashboard`. Locate the `otp=` parameter and remove its value entirely (leave it empty after the equals sign, so it reads `otp=`).
5. **Forwarding and Capturing the Flag:** Forward the modified request to the server. The application fails to validate the missing parameter correctly and responds with the dashboard containing the flag.

## Why It Worked (the vulnerability)
The application suffers from improper input validation and weak logic handling for multi-factor authentication. The backend code fails to enforce a strict check ensuring a non-empty, valid token was provided before granting access.

* **Defensive Fix:** Ensure the server strictly validates that the OTP parameter is present, correctly formatted, and cryptographically verified against the active user session before processing authorization.

## Flag
```
[FLAG HIDDEN]
```

## Takeaways
- **Learned:** How to configure Burp Suite as an intercepting proxy to capture and manipulate live web application requests and parameters.
- **Faster next time:** Immediately test parameter omission, null values, or unexpected data types on authentication/2FA checkpoints when standard client-side flows fail.

<!-- ===== OPTIONAL SECTIONS — keep what helps, delete the rest ===== -->

## Recon / First Look (optional)
- Configured browser proxy settings to point to `127.0.0.1:8080`.
- Verified SSL/TLS certificate installation in Burp Suite to ensure HTTPS traffic interception works without certificate warnings.

## Dead Ends & Rabbit Holes (optional) 🕳️
- Tried bruteforcing the 6-digit OTP code using Burp Intruder, but rate-limiting made it inefficient before discovering the parameter removal bypass.