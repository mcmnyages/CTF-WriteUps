---
title: "Old Sessions"
event: "cylabCTF (CyLab Academy, formerly picoCTF)"
series: "Standalone"
category: web
difficulty: easy
points: 0
status: solved
solved_with: solo
author: "David Gaviria"
date: 2026-11-03
flag: "[FLAG HIDDEN]"
tags: [session-hijacking, session-management, web-exploitation, improper-session-expiration]
---

# Old Sessions

> **TL;DR:** Discovered an exposed `/sessions` endpoint containing persistent session information. The application had improperly configured session expiration, exposing an administrative session and demonstrating insecure session management.

## Background (for beginners)

- **What is a session?** A session maintains a user's authenticated state between requests.
- **What is session hijacking?** It occurs when someone obtains another user's valid session identifier and uses it to access their account.
- **What is session expiration?** Sessions should expire after a reasonable period of inactivity or a configured absolute lifetime.
- **Why is it dangerous?** Permanent sessions can remain usable after a user closes their browser, especially on shared computers.

## The Challenge

**Challenge:** Old Sessions  
**Category:** Web Exploitation  
**Difficulty:** Easy  
**Author:** David Gaviria  
**Platform:** CyLab Academy (formerly picoCTF)

Challenge description:

> Proper session timeout controls are critical for securing user accounts. If a user logs in on a public or shared computer but doesn’t explicitly log out (instead simply closing the browser tab), and session expiration dates are misconfigured, the session may remain active indefinitely.
>
> This then allows an attacker using the same browser later to access the user’s account without needing credentials, exploiting the fact that sessions never expire.

**Target URL:**

http://chatelaine.cylabacademy.net:11951/

## Key Insight 💡

The main clue was a comment from `mary_jones_8992` mentioning a strange `/sessions` page.

Visiting that page revealed two session entries:

1. Admin session:
   - Session ID: `[SESSION ID HIDDEN — live CTF]`
   - `_permanent`: `True`
   - `key`: `admin`

2. Test session:
   - Session ID: `[SESSION ID HIDDEN — live CTF]`
   - `_permanent`: `True`
   - `key`: `test`

The important discovery was that both sessions were marked as permanent.

The administrative session was particularly interesting because its associated key was `admin`.

## Solution

1. **Access the challenge website**

   Opened the provided challenge URL:

   `http://chatelaine.cylabacademy.net:11951/`

2. **Register an account**

   Created an account on the social media platform and logged in successfully.

3. **Explore the application**

   Inspected the website and discovered a comment posted by `mary_jones_8992`.

   The comment mentioned a strange `/sessions` endpoint.

4. **Visit the sessions page**

   Navigated to:

   `http://chatelaine.cylabacademy.net:11951/sessions`

   The page exposed session information, including an administrative session and a test session.

5. **Analyze the exposed sessions**

   Both sessions had `_permanent=True`.

   This indicated that the application was configured to maintain sessions persistently rather than enforcing an appropriate expiration policy.

6. **Identify the administrative session**

   The entry associated with `key=admin` was the important discovery.

   It demonstrated that administrative session information was exposed through the application.

7. **Retrieve the flag**

   Following the session-management vulnerability led to the challenge flag.

## Why It Worked (the vulnerability)

The application had insecure session management.

It allowed sessions to remain permanent and exposed sensitive session information through the `/sessions` endpoint.

Session identifiers function as bearer credentials: anyone who obtains a valid identifier may be able to access the associated account.

**Defensive fix:**
- Configure reasonable session expiration times.
- Implement idle and absolute session timeouts.
- Invalidate sessions when users log out.
- Avoid exposing session identifiers or internal session data.
- Use secure, HTTP-only and SameSite cookie attributes.
- Rotate session identifiers after authentication and privilege changes.

## Flag

```text
[FLAG HIDDEN]
```
