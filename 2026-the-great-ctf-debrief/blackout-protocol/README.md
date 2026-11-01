# ⚡ The Blackout Protocol

A 4-chapter DFIR/network/RE chain. **Each chapter's token unlocks the next chapter's evidence.** Recurring theme: correct clock drift, verify hash-chains/HMACs, and require independent confirmation — so you can tell the real incident from decoys and tampered evidence.

```
Ch1 token ─▶ Ch2 token ─▶ Ch3 token ─▶ Ch4 (final)
```

<!-- AUTO-INDEX:START -->
| Challenge | Difficulty | Tags | Flag |
|---|---|---|---|
| [The First Alert](01-the-first-alert/) | basic | `log-correlation`, `clock-drift`, `integrity-chain`, `decoy-rejection` | `FLAG{BP01_E39F35ADE250}` |
| [The Access Puzzle](02-the-access-puzzle/) | medium | `cache-collision`, `auth-tag-verification`, `access-control`, `path-continuity` | `FLAG{BP02_35C2C90A3900}` |
| [The Broken Handshake](03-the-broken-handshake/) | medium | `reverse-engineering`, `auth-downgrade`, `replay-attack`, `challenge-response` | `FLAG{BP03_8CD2027966B9}` |
| [The Poisoned Evidence](04-the-poisoned-evidence/) | advanced | `prompt-injection`, `ai-security`, `retrieval-poisoning`, `evidence-integrity` | `FLAG{BP04_14D8F1BCE88A}` |
<!-- AUTO-INDEX:END -->
