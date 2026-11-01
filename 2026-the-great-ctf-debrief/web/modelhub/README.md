---
title: "Modelhub"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{y4ml-uns4f3-l04d-g4dg3t-byp4ss}"
tags: [yaml-deserialization, rce, blocklist-bypass, insecure-deserialization]
---

# Modelhub

> **TL;DR:** A YAML manifest was parsed unsafely (able to construct Python objects); a blocklist stopped the obvious dangerous names, but the unlisted `os.getenv` passed through and read the flag from an environment variable.

## Background (for beginners)
- **Unsafe YAML deserialization** (e.g. Python `yaml.load` without `SafeLoader`) can instantiate arbitrary objects and call functions via special tags — effectively code execution.
- A **blocklist** of bad names (`system`, `eval`, `exec`, `subprocess`) is incomplete by nature: many other callables remain.
- Even "read-only" functions like `os.getenv`/`os.listdir` are enough to steal secrets.

## The Challenge
You sign in and import a YAML manifest; the server reads it and echoes fields back. Dangerous YAML tags work, showing the manifest is parsed in a way that can build and run Python objects — but a firewall blocks the names `system`, `eval`, `exec`, and `subprocess`. The real flag is in an environment variable.

## Key Insight 💡
The firewall is only a blocklist, so any dangerous-enough callable that isn't on the list works. You don't need command execution — `os.getenv("FLAG")` is harmless-looking, unblocked, and reads exactly the secret you want, returned in the echoed field.

## Solution
1. Import a manifest using a dangerous YAML tag and confirm objects are constructed. *Why: proves unsafe deserialization / code paths.*
2. Try blocked names and confirm the firewall rejects `system`/`eval`/`exec`/`subprocess`. *Why: maps the blocklist.*
3. Test harmless-looking readers like `os.getenv` and `os.listdir` — they pass. *Why: confirms the blocklist is incomplete.*
4. Set a manifest field to call `os.getenv("FLAG")`. *Why: the flag is stored in an env var, and this call is allowed and executed.*
5. Read the echoed field to recover the flag. *Why: the server returns the evaluated value in its response.*

## Why It Worked (the vulnerability)
The manifest was deserialized with an unsafe loader able to call functions, and the only guard was an incomplete name blocklist that omitted `os.getenv`. **Fix:** use a safe loader (`yaml.safe_load`) that cannot instantiate arbitrary objects; never rely on a callable blocklist.

## Flag
```
FLAG{y4ml-uns4f3-l04d-g4dg3t-byp4ss}
```

## Takeaways
- Unsafe YAML loaders are RCE; blocklisting a few names doesn't fix the class.
- "Read-only" functions still exfiltrate secrets — `os.getenv` beats a command blocklist.
- Always parse untrusted YAML with a safe loader.
