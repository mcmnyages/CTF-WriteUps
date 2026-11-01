---
title: "Mailer"
event: "CyberWeek 2026"
series: "Together"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{sst1-rc3-thr0ugh-th3-m41l3r}"
tags: [ssti, jinja2, template-injection, env-leak]
---

# Mailer

> **TL;DR:** A notification-template preview rendered user input server-side (Jinja2); a template-injection payload read server environment variables, yielding the flag and the next portal's login.

## Background (for beginners)
- Server-Side Template Injection (SSTI) happens when user input is embedded into a server template that is then evaluated, letting input become template code.
- A quick test: submit a math expression; if the server returns the computed result, it is evaluating your input as a template.
- Jinja2 (Python) SSTI can reach Python objects and, from there, environment variables, files, or code execution.
- Fix in one line: never pass user input as the template itself — render it only as data passed into a static template.

## The Challenge
Portal 2 of the Together chain. Logging in with the credentials recovered from Gateway reveals a notification-template preview feature that renders input **server-side**. Tools: browser automation.

## Key Insight 💡
A small test expression submitted to the preview was **calculated by the server** — the response showed the arithmetic result, confirming the input is evaluated as a template, not printed verbatim.

## Solution
1. **Log in with Gateway's credentials** and open the template-preview feature. (WHY: the chain supplies each portal's login from the previous one.)
2. **Send a math expression** to the preview; the server returned the computed value, confirming SSTI. (WHY: evaluated arithmetic is the canonical SSTI tell.)
3. **Escalate to read environment variables** via a template payload; the response leaked the flag plus the Portal 3 (Vault) login. (WHY: env vars commonly hold secrets and the chained next-portal credentials.)

## Why It Worked (the vulnerability)
User input was concatenated into a Jinja2 template and rendered, so input executed as template code with access to the server runtime. **Fix:** treat user input strictly as rendered data (context variables), never as template source.

## Flag
```
FLAG{sst1-rc3-thr0ugh-th3-m41l3r}
```

## Takeaways
- Any "preview" that reflects evaluated expressions is an SSTI candidate — test with harmless arithmetic first.
- SSTI routinely escalates from a math trick to environment/secret disclosure or full RCE.
- Keep templates static; inject only sanitized context values.

## Chain Note
**Together** is a 5-portal chain where each portal hands over the next portal's login. Mailer receives Gateway's dumped credentials as input and outputs the flag plus Portal 3 (Vault) credentials, read from the server environment via SSTI.
