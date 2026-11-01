---
title: "NetProbe"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}"
tags: [command-injection, newline-injection, filter-bypass, env-var-leak]
---

# NetProbe

> **TL;DR:** A network-lookup tool ran a shell command on your hostname. Semicolons/pipes were blocked (returning a decoy flag), but a **newline** smuggled a second command through. Argument-bearing commands were blocked, so a no-argument command that prints environment variables leaked the real flag.

## Background (for beginners)
- **OS command injection** happens when user input is placed into a shell command; attacker-added separators run extra commands with the app's privileges.
- Common separators are `;`, `|`, `&&` — but a **newline** is also a command separator in a shell and is often forgotten by naive filters.
- Blocklist filters are fragile: they ban known-bad characters but miss others (newline, whitespace tricks, the shell's **IFS** field separator).
- Dangerous because successful injection typically means arbitrary command execution and secret exfiltration (e.g. from environment variables).

## The Challenge
The tool runs a network-lookup command on a hostname you provide and shows raw output. `;` and `|` are blocked and return a **fake decoy flag**. Tooling: `curl`, a small JSON script.

## Key Insight 💡
The filter caught the obvious separators but not a **newline**. A newline in the input ends the lookup and starts a **second, separate command**. Follow-ups with extra arguments were still blocked, but a command that needs **no arguments** slipped through.

## Solution
1. **Confirm `;`/`|` are filtered** (they return the decoy flag). *Why:* identifies the blocklist and warns the decoy is not the real flag.
2. **Inject a newline** after the hostname to terminate the lookup and begin a new command. *Why:* newline is an unfiltered command separator.
3. **Use a command that takes no arguments** (argument-bearing commands were blocked) that prints the environment. *Why:* the filter's checks keyed on arguments/whitespace, so an argument-free command evades them.
4. **Read the environment output** where the real flag was stored. *Why:* the app leaked its env vars, which held the flag.

> Note: the flag slug `1fs-byp4ss` points at the **IFS/whitespace** angle — filters that rely on spotting spaces or argument tokens can be dodged by abusing the shell's field-separator handling and whitespace, which is why an argument-free command (no filtered whitespace tokens) worked.

## Why It Worked (the vulnerability)
User input reached a shell, and a blocklist that missed newlines (and whitespace/IFS tricks) allowed a second command to run. **Fix:** never build shell strings from user input — execute the lookup binary directly with arguments passed as a list (no shell), and strictly validate hostnames against an allowlist.

## Flag
```
FLAG{c0mm4nd-1nj3ct10n-1fs-byp4ss}
```

## Takeaways
- **Pattern:** input in a shell command + blocklist filter = command injection.
- **Spotting it:** test newline and whitespace separators, not just `;` and `|`; distrust decoy flags.
- **Fixing it:** avoid the shell entirely, pass args as a list, and allowlist inputs.
