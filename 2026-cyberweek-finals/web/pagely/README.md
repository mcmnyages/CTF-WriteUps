---
title: "Pagely"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: easy
points: 150
status: solved
flag: "FLAG{l0g-p01s0n1ng-lf1-t0-rc3}"
tags: [lfi, local-file-inclusion, path-traversal, information-disclosure]
---

# Pagely

> **TL;DR:** An internal docs viewer loaded pages from a link parameter with no restriction. Point it at a server config/env file instead of a doc and it reveals internal settings — including the flag stored as a hidden setting (LFI).

## Background (for beginners)
- **Local File Inclusion (LFI)** happens when a page loads a file whose path is taken from user input without validation, letting an attacker read files they shouldn't.
- Attackers swap the expected filename for **sensitive paths** (config, environment, or system files) to disclose secrets.
- LFI often chains further: if an attacker can get their input written to a file the app will *execute* (for example a log file — "log poisoning"), it can escalate to **remote code execution (RCE)**.
- Dangerous because one unchecked path parameter can expose source, secrets, or full server control.

## The Challenge
The site loads pages based on a **link parameter**. Tooling: browser.

## Key Insight 💡
The viewer trusted the parameter and would load **whatever file you named**. Instead of a documentation page, point it at a server settings/config file to read values that were never meant to be served.

## Solution
1. **Observe the page-loading parameter** that selects which document to render. *Why:* this is the attacker-controlled path.
2. **Change the parameter to reference other files** beyond the docs directory. *Why:* tests whether the viewer restricts which files it will include.
3. **Point it at a special system/config file** holding the app's internal settings. *Why:* that file contained a hidden setting with the flag.
4. **Read the disclosed settings** from the rendered output. *Why:* the included file's contents are shown directly, revealing the flag.

> Note: the flag name `l0g-p01s0n1ng-lf1-t0-rc3` references the classic **LFI → RCE via log poisoning** escalation. In this solve, the reached impact was configuration/environment **disclosure** through LFI; the flag slug points at the broader log-poisoning-to-code-execution path that the same primitive can enable.

## Why It Worked (the vulnerability)
File paths from user input were included without validation, allowing arbitrary local files to be read. **Fix:** never build file paths from raw input; use an allowlist of permitted pages/IDs and canonicalize/confine paths to a safe directory.

## Flag
```
FLAG{l0g-p01s0n1ng-lf1-t0-rc3}
```

## Takeaways
- **Pattern:** user-controlled file paths = LFI, and sometimes LFI → RCE.
- **Spotting it:** change any "page"/"file"/"include" parameter to a known sensitive path.
- **Fixing it:** allowlist inputs, map to fixed files, and confine includes to a safe root.
