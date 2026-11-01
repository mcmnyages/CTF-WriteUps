---
title: "Graphly"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{gr4phql-b0l4-d1d-y0u-m34n}"
tags: [graphql, bola, broken-access-control, authorization]
---

# Graphly

> **TL;DR:** GraphQL introspection was off, but error "did you mean" hints revealed field names. Then querying another user's record — the admin's — returned their private API key with no authorization check (BOLA).

## Background (for beginners)
- **GraphQL** exposes a typed API; **introspection** normally lets clients explore the full schema. Disabling it only hides the map, not the data.
- GraphQL servers often return **helpful error messages** ("did you mean `apiKey`?") that leak valid field names anyway.
- **BOLA (Broken Object-Level Authorization)** means the API returns an object to anyone who asks for it by ID/username, without checking they're allowed to see it.
- Dangerous because hiding the schema is not access control — the real failure is missing per-object authorization.

## The Challenge
A site backed by GraphQL with **introspection disabled** ("explore the schema" turned off). Tooling: browser / API requests.

## Key Insight 💡
Disabled introspection just hides field names — the server still **suggests corrections** in error messages. Guessing field names surfaced a user record with an API key field, and nothing stopped you from requesting *another* user's record directly.

## Solution
1. **Send queries with guessed field names.** *Why:* even without introspection, the API's "did you mean" errors reveal the correct names.
2. **Build a valid user query** exposing the API key field on a user record. *Why:* confirms the data shape and the sensitive field.
3. **Request the admin user's record directly** (by their identifier). *Why:* tests whether object-level authorization is enforced — it is not.
4. **Read the admin's API key** from the response — the flag. *Why:* with no BOLA protection, any user's private data is returned on demand.

## Why It Worked (the vulnerability)
The resolver returned any user object without verifying the caller's authorization for that object (BOLA), and verbose errors defeated the "hidden schema" control. **Fix:** enforce per-object authorization in resolvers, disable field suggestions/verbose errors in production, and never treat hidden introspection as security.

## Flag
```
FLAG{gr4phql-b0l4-d1d-y0u-m34n}
```

## Takeaways
- **Pattern:** GraphQL + missing object authorization = BOLA data exposure.
- **Spotting it:** request objects you shouldn't own; watch error hints for field names.
- **Fixing it:** authorize every object access and silence schema-leaking errors.
