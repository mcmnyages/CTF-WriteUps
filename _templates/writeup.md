---
title: "<Challenge Name>"
event: "<CTF Name> <Year>"
series: "<series name, or Standalone>"     # chained challenges share a series; otherwise "Standalone"
category: web                               # web | pwn | rev | crypto | forensics | osint | stego | misc | hardware | ai
difficulty: medium                          # easy | medium | hard | insane (your call)
points: 0
status: solved                             # solved | unsolved
solved_with: team                          # solo | team | with-AI
author: "<your name/handle>"               # who wrote this up (handy in a team repo)
date: YYYY-MM-DD
flag: "FLAG{...}"
tags: [sqli, idor]                          # techniques — lets you grep later and fills the Tags column
live: auto                                  # auto = follow the event (LIVE.md) | true = hide flag | false = show flag
---
<!--
  HOW TO USE THIS FILE
  - This is the standard shape for EVERY writeup in the repo, so they all look the same.
  - Fill in the frontmatter block (between the --- lines) — the index tables are built from it.
  - Replace the <...> placeholders. Delete any OPTIONAL section you don't need.
  - LIVE CTF? Write the real flag normally; `python ctf.py` hides it automatically.
  - When done, run `python ctf.py` from the CTFs/ folder to rebuild the indexes.
-->


# <Challenge Name>

> **TL;DR:** <one or two sentences an expert can read and stop. e.g. "Unsanitised `id` → UNION SQLi → dump `secrets` table → flag.">

## Background (for beginners)
<2–4 short bullets explaining the concept in plain words, so a newcomer can follow. Link out instead of writing a textbook.>
- **What is X?** ...
- **Why is it dangerous?** ...

## The Challenge
<What you were given / the setup. Paste the original description and how to reach it (URL / nc / file). Save challenge files into ./files/ — servers go offline after the event.>

## Key Insight 💡
<The single "aha" that cracked it, and the clue that pointed to it. This is the part future-you forgets first.>

## Solution
<Numbered steps. For each: what you did, WHY, and what came out. Show real commands/requests and their output.>
1. ...
2. ...

## Why It Worked (the vulnerability)
<The underlying weakness in one short paragraph, plus a one-line defensive fix.>

## Flag
```
FLAG{...}
```

## Takeaways
- **Learned:** ...
- **Faster next time:** ...

<!-- ===== OPTIONAL SECTIONS — keep what helps, delete the rest ===== -->

## Recon / First Look (optional)
<Great for pwn/rev/forensics. The commands you ran first and what they showed (e.g. `file`, `checksec`, `nmap`, `exiftool`).>

## Dead Ends & Rabbit Holes (optional) 🕳️
<What you tried that DIDN'T work, and why. Often the most useful section for teammates.>

## Solve Script (optional)
<Put the full script in ./solve.py and paste the core here. It should run start-to-finish and print the flag.>
```python
#!/usr/bin/env python3
...
```

## Chain Note (optional)
<For chained challenges: what value/credential came IN from the previous stage, and what this one hands to the next.>
