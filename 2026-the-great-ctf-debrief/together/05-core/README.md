---
title: "Core"
event: "The Great CTF Debrief 2026"
series: "Together"
category: web
difficulty: hard
points: 400
status: solved
flag: "FLAG{p1ckl3-d3s3r-0wns-th3-c0r3}"
tags: [insecure-deserialization, pickle, rce, python]
---

# Core

> **TL;DR:** A "restore session" feature deserialized a base64 Python pickle; a crafted pickle executed a shell command on load, printing the environment that contained the flag.

## Background (for beginners)
- Python's `pickle` serializes objects, but **unpickling runs code** — a pickle can define a `__reduce__` that executes arbitrary commands when loaded.
- Accepting a pickle from an untrusted source is effectively accepting code to run on the server (remote code execution).
- The safe analogue for user-supplied state is a data-only format like JSON, which does not execute anything.
- Fix in one line: never unpickle untrusted data; use a safe serialization format and sign/validate any stored state.

## The Challenge
The final stage of the Together chain. After logging in with the Portal 4 (Fetcher) credentials, you find a "restore session" feature that accepts a saved blob — a base64-encoded Python pickle — and displays the restored object. Tools: Python.

## Key Insight 💡
Pickle **runs code on load**, so a session blob is not just data — a crafted pickle can execute a command the moment the server restores it.

## Solution
1. **Log in with Portal 4 credentials** and locate the restore-session feature. (WHY: this is the chain's final handoff login.)
2. **Confirm the blob is a base64 pickle** by decoding a legitimate saved session. (WHY: identifies the deserialization sink and its encoding.)
3. **Craft a malicious pickle** whose load triggers a shell command (via the object's reduce hook). (WHY: unpickling executes the embedded command.)
4. **Make the command print the environment and a file listing**; submitting the blob caused the server to load it, run it, and return output with the flag in an env var. (WHY: the flag lives in a server environment variable exposed by the command output.)

Illustrative pseudocode (not the actual payload):
```
class Exploit:
    def __reduce__(self):
        return (os.system, ("<command that prints env>",))
blob = base64(pickle.dumps(Exploit()))
```

## Why It Worked (the vulnerability)
The server called `pickle.loads` on user-supplied data, so loading the blob executed attacker code. **Fix:** never deserialize untrusted input with pickle — use a data-only format (e.g. JSON) and cryptographically verify any state you must round-trip.

## Flag
```
FLAG{p1ckl3-d3s3r-0wns-th3-c0r3}
```

## Takeaways
- "Restore/import" features that accept serialized blobs are prime RCE sinks — check the format first.
- Pickle equals code execution; treat any pickle from a client as hostile.
- Sign and validate round-tripped state, and prefer formats that cannot execute.

## Chain Note
**Together** is a 5-portal chain where each portal hands over the next portal's login. Core receives Portal 4's handoff credentials as input and, as the final stage, outputs the last flag — read from a server environment variable via pickle-driven RCE. Nothing is handed onward.
