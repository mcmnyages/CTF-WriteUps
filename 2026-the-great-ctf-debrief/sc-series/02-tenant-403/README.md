---
title: "Tenant 403"
event: "The Great CTF Debrief 2026"
series: "SC Series"
category: web
difficulty: MEDIUM
points: 450
status: solved
flag: "FLAG{SC02_D3025A6B3221_T16}"
tags: [web, idor, path-traversal, tenant-isolation]
---

# Tenant 403

> **TL;DR:** A path-normalization mismatch lets a tenant-scoped export endpoint be tricked with `../` so a "starts-with my tenant" check passes while the fetch walks into another tenant's archive — a cross-tenant IDOR that leaks the audit record holding the flag.

## Background (for beginners)
- **Multi-tenant** apps isolate customers so tenant A cannot read tenant B's data.
- **IDOR** (Insecure Direct Object Reference) is accessing another party's resource by manipulating an identifier or path the server trusts.
- **Path traversal** uses `../` to climb out of an intended directory.
- The bug class here is a **check/lookup mismatch**: the permission check and the file fetch interpret the same path differently (one before, one after normalizing `..`).

## The Challenge
A civic records portal was accessed with team ID `SC02-16` + PIN; the account owned a single tenant `COUNTY-16`. The team's own case memo (`CASE-NOTE.json`), read via export-preview, held a receipt tag `6E09D26077106D5C` and noted the matching audit record lived in a separate archive office `CIVIC-AUDIT` not directly accessible.

## Key Insight 💡
The export-preview permission check only verified the requested `source` path **started with** `tenants/COUNTY-16/`, but the fetch code **normalized the `..` steps first**. A path that starts with the allowed prefix can still resolve into a different tenant.

## Solution
1. **Authenticate and scope** — log in as `SC02-16`, confirm the single tenant `COUNTY-16`. *Why: establishes the legitimate boundary to escape.*
2. **Read the memo** — export-preview `CASE-NOTE.json` to obtain the receipt tag `6E09D26077106D5C` and the pointer to `CIVIC-AUDIT`. *Why: tells you what to find and where.*
3. **Exploit the mismatch** — request `tenants/COUNTY-16/../CIVIC-AUDIT/records/index.json`; it starts with the allowed prefix (check passes) and then `..` walks up into the archive office (fetch resolves it). *Why: the check and lookup disagree about the path.*
4. **Find the right record** — the archive index listed many receipt tags; the one matching the memo pointed to `DOC-1FE944B5947631.json` (the rest were decoys). *Why: the receipt tag ties the memo to its audit record.*
5. **Fetch the flag** — retrieve that document the same traversal way; it is the audit disposition containing the flag. *Why: that is the target record.*

## Why It Worked (the vulnerability / technique)
Broken tenant isolation via a path-normalization mismatch: the authorization check ran on the raw path while the file read ran on the normalized path, enabling a cross-tenant IDOR. **Defensive note:** canonicalize the path *once*, then authorize and fetch using the same canonical value — never check one form and act on another.

## Flag
```
FLAG{SC02_D3025A6B3221_T16}
```

## Takeaways
- Authorize on the exact, canonicalized path you will actually use.
- `starts-with` prefix checks are not isolation — `..` defeats them.
- Receipt-tag correlation cuts through decoys to the one real record.

## Chain Note
SC02 of the cross-category **SC Series** (SC01/SC02/SC03), each a different category under a shared storyline.
