---
title: "Accountly"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: medium
points: 250
status: solved
flag: "FLAG{m4ss-4ss1gnm3nt-sc0p3-cr33p}"
tags: [mass-assignment, privilege-escalation, broken-access-control, idor]
---

# Accountly

> **TL;DR:** The profile editor let a user update *any* field of their own account record, including permission scopes; adding the admin scope to your own account granted admin access and the flag.

## Background (for beginners)
- **Mass assignment** is when a server blindly binds incoming request fields to a data model, trusting the client to only send fields it's allowed to change.
- If sensitive fields (role, scopes, verified, balance) aren't protected, users can set them directly — privilege escalation.
- The fix is an allowlist of client-editable fields, decided server-side.

## The Challenge
You register a normal account and view your account record, which exposes `role`, `plan`, and permission `scopes` (empty to start). The profile editor states that any field can be updated. An admin report is locked behind an admin permission scope.

## Key Insight 💡
If the editor truly updates "any field," then the permission-scope field is also client-editable — the server does not distinguish between harmless profile fields and security-sensitive ones.

## Solution
1. Register and read your account record; note `scopes` is empty. *Why: identifies the sensitive field and baseline state.*
2. Send a profile-update request that includes the admin permission scope on your own record. *Why: tests whether the server accepts a security-relevant field from the client.*
3. Server accepts the new scope. *Why: confirms mass assignment with no field allowlist.*
4. Open the admin report. *Why: access control keys off the scope you just granted yourself.*

## Why It Worked (the vulnerability)
The update endpoint bound every submitted field to the user record, including permission scopes, with no server-side allowlist — classic mass assignment leading to scope creep. **Fix:** explicitly allowlist editable fields and reject/ignore any privilege-bearing fields in user-facing update endpoints.

## Flag
```
FLAG{m4ss-4ss1gnm3nt-sc0p3-cr33p}
```

## Takeaways
- Any endpoint that "updates your profile" may update fields you can't see in the UI.
- Look for role/scope/flag fields in the account record, then try setting them.
- Defend with explicit field allowlists; never trust client-supplied privilege fields.
