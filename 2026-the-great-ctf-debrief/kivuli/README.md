# 🕶️ Kivuli (cwa2026 finals)

Challenges from the cwa2026 finals. The set is numbered with gaps — only stages **1, 5, 7, 8** are covered here. Several stages feed carry-over values into later ones.

```
CurveBreaker (7) ──▶ session_secret cafe20261a6b72 ─┐
NestedRequest (5) ──▶ signing_fragment deadbeef12345678 ─┴─▶ PaddingOracle (8) login
```

<!-- AUTO-INDEX:START -->
| Challenge | Difficulty | Tags | Flag |
|---|---|---|---|
| [GhostProcess](01-ghostprocess/) | medium | `memory-forensics`, `fileless-malware`, `process-injection`, `xor` | `FLAG{cwa2026_finals_5eefb85fb2f96b1f}` |
| [NestedRequest](05-nestedrequest/) | advanced | `ssrf`, `url-parser-confusion`, `allowlist-bypass`, `path-traversal` | `FLAG{cwa2026_finals_ssrf_r3binding_bypass}` |
| [CurveBreaker](07-curvebreaker/) | easy | `invalid-curve-attack`, `ecdh`, `p-256`, `sha256-kdf` | `FLAG{cwa2026_finals_inv4lid_curv3_attack}` |
| [PaddingOracle](08-paddingoracle/) | advanced | `padding-oracle`, `aes-cbc`, `cookie-forgery`, `privilege-escalation` | `FLAG{cwa2026_finals_cbc_p4dding_0r4cl3}` |
<!-- AUTO-INDEX:END -->
