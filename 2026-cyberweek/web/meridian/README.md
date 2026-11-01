---
title: "Meridian"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: easy
points: 150
status: solved
flag: "FLAG{d3bug-m0d3-l34k3d-th3-k3y}"
tags: [information-disclosure, debug-mode, secret-leak, token-forgery]
---

# Meridian

> **TL;DR:** An admin page needed a token derived from the server's secret key. A different endpoint ran in debug mode and leaked that secret in an error page; with the secret, we computed the valid admin token.

## Background (for beginners)
- **Debug mode** in web frameworks shows rich error pages (stack traces, config, variables) to help developers — but it must be off in production.
- Many tokens (session cookies, signed admin tokens) are generated from a **server secret key**. If that key leaks, anyone can forge valid tokens.
- **Information disclosure** of secrets collapses the entire trust model: knowing the key = being the server.
- Dangerous because one leaked value defeats otherwise-strong cryptographic checks.

## The Challenge
An admin-only page requires a secret token that is built from a server secret key. Tooling: `curl`, Python.

## Key Insight 💡
Another part of the site was running in **debug mode**. Triggering an error there rendered a detailed error page that **leaked the server's secret key** — exactly the input needed to forge the admin token.

## Solution
1. **Probe secondary endpoints with bad input** until one returns a verbose debug error page. *Why:* debug error pages often dump configuration and secrets.
2. **Read the server secret key** out of the leaked error details. *Why:* this key is the seed for the admin token.
3. **Compute the admin token locally in Python** using the leaked secret and the token scheme the app expects. *Why:* with the secret, you can produce exactly what the server will accept.
4. **Request the admin page with the forged token.** *Why:* a valid token passes the server's check; the flag is on the admin page.

## Why It Worked (the vulnerability)
Debug mode was enabled in a reachable environment, exposing the application's secret key in error output. **Fix:** disable debug/verbose errors in production and keep secrets out of all responses; rotate any key that was ever displayed.

## Flag
```
FLAG{d3bug-m0d3-l34k3d-th3-k3y}
```

## Takeaways
- **Pattern:** debug mode + error pages = secret disclosure.
- **Spotting it:** force errors and scan responses for stack traces, config, and keys.
- **Fixing it:** ship with debug off, generic error pages, and secrets stored outside the app surface.
