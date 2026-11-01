---
title: "Invoicer"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: easy
points: 150
status: solved
flag: "FLAG{xx3-l34ks-th3-l1c3ns3-k3y}"
tags: [xxe, xml-external-entity, file-disclosure, xml-parsing]
---

# Invoicer

> **TL;DR:** The invoice upload parsed XML with external entities enabled. A crafted entity told the server to read its own license file and echo it back — XXE local file disclosure.

## Background (for beginners)
- **XML** can define **entities** — shortcuts that expand into other content, including, when misconfigured, the contents of **external files**.
- **XXE (XML External Entity)** injection abuses this to make the server read local files, reach internal services, or cause denial of service.
- It happens when an XML parser is left with external entity resolution enabled on untrusted input.
- Dangerous because it turns a data-upload feature into an arbitrary file reader on the server.

## The Challenge
The site accepts invoice data as **XML** uploads. Tooling: `curl`, crafted XML.

## Key Insight 💡
If the parser resolves external entities, you can declare an entity that points at a **local file path** and have its contents substituted into a field the app echoes back — so the server reads the file *for* you.

## Solution
1. **Confirm the upload accepts XML** and that parsed fields are reflected in the response. *Why:* reflection gives a channel to exfiltrate file contents.
2. **Craft an XML document declaring an external entity** that references the server's own license file, then reference that entity inside a returned field. *Why:* the parser expands the entity into the file's contents.
3. **Upload the crafted XML with `curl`.** *Why:* submitting it triggers server-side parsing and entity resolution.
4. **Read the license file contents from the response** — the flag was inside. *Why:* the expanded entity places the file's data where the app renders it back.

## Why It Worked (the vulnerability)
The XML parser resolved external entities on attacker-supplied input, allowing local file reads. **Fix:** disable external entities and DTD processing in the XML parser (use hardened/safe parser settings), and avoid XML for untrusted input where possible.

## Flag
```
FLAG{xx3-l34ks-th3-l1c3ns3-k3y}
```

## Takeaways
- **Pattern:** XML upload + external entities enabled = file disclosure (XXE).
- **Spotting it:** test whether XML entities expand and whether fields reflect back.
- **Fixing it:** turn off DTDs/external entities in every XML parser handling user input.
