---
title: "MergeMate"
event: "CyberWeek 2026"
series: "Standalone"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{pr0t0typ3-p0llut10n-c0nstruct0r}"
tags: [prototype-pollution, deep-merge, privilege-escalation, filter-bypass]
---

# MergeMate

> **TL;DR:** A server-side deep-merge of a user JSON patch was vulnerable to prototype pollution; a top-level attempt was filtered, but nesting the pollution one level deeper slipped past and set admin flags on every object, making the workspace count as admin.

## Background (for beginners)
- **Prototype pollution** (JS) happens when a recursive merge writes attacker keys like `__proto__`/`constructor.prototype` into the shared base object that all objects inherit from.
- Once polluted, *every* object appears to have the injected property — so an admin flag can leak onto unrelated objects.
- Filters that only block the pollution key at the top level miss it when it's nested deeper in the payload.

## The Challenge
The site takes a JSON settings patch and deep-merges it into your workspace config server-side. A separate admin report unlocks only for an admin workspace. A plain top-level pollution attempt is filtered.

## Key Insight 💡
The filter only inspected top-level keys. A deep-merge recurses, so placing the polluting key one level deeper in the JSON reaches the shared prototype anyway — the recursion does the climbing for you.

## Solution
1. Confirm the patch is deep-merged into config server-side. *Why: deep-merge is the classic pollution sink.*
2. Send a top-level pollution key — blocked. *Why: reveals a top-level-only filter.*
3. Nest the polluting key one level deeper in the JSON patch. *Why: the filter doesn't inspect nested keys, but the recursive merge still writes to the shared base object.*
4. Set admin flags on the prototype so every object (including the workspace check) inherits them. *Why: makes the workspace evaluate as admin.*
5. Open the admin report. *Why: it unlocks for an admin workspace, which you now appear to have.*

## Why It Worked (the vulnerability)
A recursive merge wrote attacker-controlled keys into the object prototype, and the filter only guarded top-level keys, not nested ones. **Fix:** block `__proto__`/`constructor`/`prototype` at every depth, use a null-prototype or `Map` for config, and use a merge library hardened against pollution.

## Flag
```
FLAG{pr0t0typ3-p0llut10n-c0nstruct0r}
```

## Takeaways
- Deep-merge of untrusted JSON is a prototype-pollution magnet.
- Top-level-only key filters are bypassed by nesting the payload deeper.
- Harden merges at every depth and store config on prototype-less objects.
