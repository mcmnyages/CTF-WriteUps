# 🤝 Together

A 5-portal web chain. **Each portal's loot contains the login for the next portal**, so solve them in order.

```
Gateway ─▶ Mailer ─▶ Vault ─▶ Fetcher ─▶ Core
 SQLi      SSTI      JWT       SSRF       pickle RCE
```

<!-- AUTO-INDEX:START -->
| Challenge | Difficulty | Tags | Flag |
|---|---|---|---|
| [Gateway](01-gateway/) | medium | `sql-injection`, `union-based`, `sqlite`, `string-concat` | `FLAG{sql1-un10n-l00t-th3-g4t3w4y}` |
| [Mailer](02-mailer/) | medium | `ssti`, `jinja2`, `template-injection`, `env-leak` | `FLAG{sst1-rc3-thr0ugh-th3-m41l3r}` |
| [Vault](03-vault/) | medium | `jwt`, `alg-none`, `auth-bypass`, `privilege-escalation` | `FLAG{jwt-n0n3-0p3ns-th3-v4ult}` |
| [Fetcher](04-fetcher/) | medium | `ssrf`, `loopback`, `port-scan`, `localhost-bypass` | `FLAG{ssrf-h1ts-th3-1ntr4n3t}` |
| [Core](05-core/) | hard | `insecure-deserialization`, `pickle`, `rce`, `python` | `FLAG{p1ckl3-d3s3r-0wns-th3-c0r3}` |
<!-- AUTO-INDEX:END -->
