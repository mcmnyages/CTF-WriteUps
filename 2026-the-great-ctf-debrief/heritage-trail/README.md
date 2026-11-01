# 🗺️ Heritage Trail

An 8-part chain themed on Kenyan heritage. It starts as OSINT and turns into a crypto/forensics puzzle where **each chapter's answer becomes an instruction or a key for a later chapter**. Chapters 7 and 8 reuse the six earlier answers to finish.

```
HT1 ROOTS ─┐
HT2 M4A7P2 ├─ six answers collected along the way ──▶ HT7 reads them as instructions
HT3 MONSOON┤                                          └▶ HT8 uses KENYA-HERITAGE as a ZIP password
HT4 ORDER  ┤
HT5 A17F09 ┘ (also names the file used in HT7)
HT6 BICAMERAL
```

<!-- AUTO-INDEX:START -->
| Challenge | Difficulty | Tags | Flag |
|---|---|---|---|
| [Njia Nyingi, Nchi Moja](01-njia-nyingi/) | basic | `osint`, `web-research`, `acrostic`, `museums-kenya` | `FLAG{ROOTS}` |
| [Fuata Njia](02-fuata-njia/) | basic | `osint`, `geolocation`, `map-markers`, `heritage-sites` | `FLAG{M4A7P2}` |
| [Crossroads of the Coast](03-crossroads-of-the-coast/) | basic | `osint`, `steganography`, `pixel-data`, `acrostic` | `FLAG{MONSOON}` |
| [Voices of Resistance](04-voices-of-resistance/) | medium | `osint`, `historical-dating`, `odd-one-out`, `sorting` | `FLAG{ORDER}` |
| [The Archive Room](05-the-archive-room/) | medium | `osint`, `forensics`, `hash-verification`, `pdf-metadata` | `FLAG{A17F09}` |
| [Roads to Self-Government](06-roads-to-self-government/) | advanced | `osint`, `crypto`, `columnar-transposition`, `historical-dating` | `FLAG{BICAMERAL}` |
| [Fragments of a Nation](07-fragments-of-a-nation/) | advanced | `crypto`, `puzzle`, `grid-extraction`, `chained-challenge` | `FLAG{KENYA-HERITAGE}` |
| [Final Chapter](08-final-chapter/) | basic | `forensics`, `aes-zip`, `password-protected-archive`, `chained-challenge` | `FLAG{MANY_PATHS_ONE_LAND}` |
<!-- AUTO-INDEX:END -->
