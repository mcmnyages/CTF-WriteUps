---
title: "PrefSync"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{g4dg3t-ch41n-c0nf1g-l34k}"
tags: [ssti, template-injection, type-confusion, deserialization]
---

# PrefSync

> **TL;DR:** Settings exported as base64 decoded to a typed object. The importer accepted several data types, one behaving as a text template. A test formula was evaluated server-side, then a template dumped the server's internal settings including the flag — SSTI via a type-confused importer.

## Background (for beginners)
- **Server-Side Template Injection (SSTI)** happens when user input is placed into a template engine that then *evaluates* it, letting attackers run template expressions (and often code).
- A **type-confused importer** trusts a type label inside imported data and instantiates whatever type is named — so an attacker picks a dangerous type the designers didn't intend.
- **Base64 export/import** is just encoding; decoding reveals the real structure (here, a labeled/typed object) you can tamper with.
- Dangerous because template evaluation can leak secrets/config and frequently escalates to remote code execution.

## The Challenge
The site exports settings as **base64**; decoding reveals a labeled object with a type name. The import feature accepts **several data types**, one of which acts like a text template. Tooling: Python, base64.

## Key Insight 💡
The importer chooses behavior from a **type label** in the data. Supplying the "template" type makes the server **evaluate** your string — a test formula came back *calculated*, proving the input is rendered, not stored literally.

## Solution
1. **Decode the exported base64 settings** to reveal the labeled object and its type name. *Why:* exposes the structure and the type field the importer keys on.
2. **Re-import with the template type and a test formula.** *Why:* if the server returns the computed result, the field is template-evaluated (SSTI confirmed).
3. **Replace the test formula with a template expression that reads the server's internal settings.** *Why:* template context often exposes config/secret objects.
4. **Submit and read the printed settings**, which included the flag. *Why:* the engine renders the attacker's expression against server-side data.

Illustrative payload (SSTI probe, not the real one):
```
{{ 7 * 7 }}   # returns 49 if evaluated
```

## Why It Worked (the vulnerability)
The importer let untrusted data select a template type whose values are evaluated by the engine, leaking configuration. **Fix:** never let input choose the deserialized type; use a strict schema/allowlist of safe types, and never render user-controlled data as a template.

## Flag
```
FLAG{g4dg3t-ch41n-c0nf1g-l34k}
```

## Takeaways
- **Pattern:** type-confused import + template evaluation = SSTI / config leak.
- **Spotting it:** decode exports, look for type labels, and probe with `{{ math }}`.
- **Fixing it:** fixed schemas, no input-chosen types, and no templating of user data.
