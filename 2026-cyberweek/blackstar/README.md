# 🛰️ BLACKSTAR

A 5-stage relay chain. Each stage reveals a `RELAY_TOKEN` that becomes the key/input for the next, spanning stego → crypto → RE → crypto → forensics.

```
BS1 007161435C98 ─▶ BS2 9402A282B212 ─▶ BS3 0D9E75EA984A ─▶ BS4 14E529E26143 ─▶ BS5 8E78738978A1 (final)
    (AES key seed)     (launch code)        (hash-ext base)      (AES key seed)
```

<!-- AUTO-INDEX:START -->
| Challenge | Difficulty | Tags | Flag |
|---|---|---|---|
| [The Downlink](01-the-downlink/) | basic | `steganography`, `lsb`, `png`, `image-forensics` | `FLAG{BS01_007161435C98}` |
| [The Uplink](02-the-uplink/) | medium | `aes-cbc`, `rsa`, `fermat-factorization`, `key-derivation` | `FLAG{BS02_9402A282B212}` |
| [The Flight Computer](03-the-flight-computer/) | hard | `reverse-engineering`, `binary-analysis`, `strings`, `chained-challenge` | `FLAG{BS03_0D9E75EA984A}` |
| [The Telemetry Gateway](04-the-telemetry-gateway/) | hard | `hash-length-extension`, `sha256`, `mac-forgery`, `privilege-escalation` | `FLAG{BS04_14E529E26143}` |
| [The Abort Sequence](05-the-abort-sequence/) | advanced | `pcap-carving`, `packet-reassembly`, `aes-cbc`, `gzip` | `FLAG{BS05_8E78738978A1}` |
<!-- AUTO-INDEX:END -->
