---
title: "Notifly"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{jinja2-sst1-rc3-g4dg3t}"
tags: [ssti, jinja2, rce, blocklist-bypass, string-concatenation]
---

# Notifly

> **TL;DR:** A server-rendered message template was vulnerable to Jinja2 SSTI; a keyword blocklist that only matched exact words was bypassed by concatenating blocked words from harmless pieces, reaching an object that runs system commands and leaking the flag from the environment.

## Background (for beginners)
- **SSTI (Server-Side Template Injection)** happens when user input is placed into a template that the server evaluates as code, not just data.
- If the engine executes expressions, an attacker can walk the language's object graph to reach functions that run OS commands — full RCE.
- Keyword blocklists are weak: if they only match exact strings, the same words can be rebuilt at runtime from fragments.

## The Challenge
A notification tool lets you write a message template with placeholders rendered on the server. A math placeholder (e.g. an arithmetic expression) came back *calculated*, proving the server evaluates real code rather than simple variable substitution. A filter blocked obvious attack words and returned a fake decoy flag when they appeared.

## Key Insight 💡
The filter checked for *exact* blocked words. In Jinja2 you can build any string from concatenated pieces (`'sys'+'tem'`), so none of the dangerous keywords ever appear literally in the input — yet the template engine assembles and uses them at evaluation time.

## Solution
1. Submit a math expression as a placeholder and confirm it is computed. *Why: confirms a real evaluating engine (SSTI), identified as Jinja2.*
2. Probe attack words and observe the decoy flag. *Why: reveals a blocklist and that it matches exact words.*
3. Rebuild each blocked word by joining smaller harmless substrings inside the template. *Why: the literal keyword never appears, so the filter never fires.*
4. Traverse from a base object through the class hierarchy to the core builtins and reach a function that executes system commands. *Why: this is the standard Jinja2 gadget chain to RCE.*
5. Run a command that reads the server's environment variables, where the real flag is stored. *Why: the flag lives in an env var, not a file.*

## Why It Worked (the vulnerability)
User input reached a Jinja2 template that evaluates expressions, and the only defence was an exact-match keyword blocklist defeated by string concatenation. **Fix:** never render user input as a template; use a sandboxed/logic-less renderer and pass user data strictly as context variables.

## Flag
```
FLAG{jinja2-sst1-rc3-g4dg3t}
```

## Takeaways
- If a placeholder does math, you are probably in a real template engine — try SSTI.
- Exact-match blocklists die to concatenation and other runtime string building.
- Treat templates as code: separate template from user data, sandbox, and drop blocklists.
