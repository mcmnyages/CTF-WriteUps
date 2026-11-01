# Category-Specific Add-ons

The main `writeup.md` works for every category. Copy the matching block below into
**Section 3 (Recon)** or **Section 5 (Solution)** so you capture the details that matter for that category.

---

## 🌐 Web
- **Stack:** framework, language, server, DB (from headers, errors, `Wappalyzer`)
- **Attack surface map:** endpoints, params, cookies, auth flow
- **Source given?** Point to the vulnerable line: `app.py:42`
- **The request that worked.** Paste the raw HTTP request/response (from Burp), not only "I sent a payload"
- **Payload breakdown.** Explain each part of the payload
- Common tags: `sqli` `xss` `ssti` `ssrf` `lfi` `idor` `jwt` `deserialization` `prototype-pollution` `race-condition` `xxe` `csrf` `cache-poisoning`

```http
POST /api/login HTTP/1.1
Host: chall.ctf.io
Content-Type: application/json

{"username":"admin","password":{"$ne":null}}
```

## 💥 Pwn (Binary Exploitation)
- **`checksec` output** (always include it)
- **Vulnerability:** type plus location (`vuln()` → `gets(buf)` with `buf[64]`)
- **Offsets:** how you found them (`cyclic`, GDB), with the value
- **Leaks:** what you leaked and how (format string, puts@got...)
- **Exploit chain diagram:**
  ```
  [ padding 72 ] [ pop rdi ] [ puts@got ] [ puts@plt ] [ main ]   ← stage 1: leak libc
  [ padding 72 ] [ ret ] [ pop rdi ] [ "/bin/sh" ] [ system ]     ← stage 2: shell
  ```
- **Libc version** and how you identified it (libc.rip / blukat)
- **Local vs remote differences** (alignment, libc, buffering)
- Common tags: `bof` `ret2win` `ret2libc` `rop` `format-string` `heap` `uaf` `tcache` `srop` `ret2dlresolve` `shellcode` `kernel`

## 🔍 Rev (Reverse Engineering)
- **Binary info:** `file`, language (C/Rust/Go/.NET/Python bytecode), packed? (`UPX`, `DIE`)
- **Decompiled snippet** of the key function, **cleaned up and renamed by you**
- **Algorithm in plain words / pseudocode**
- **Approach:** static (Ghidra/IDA), dynamic (GDB/x64dbg), symbolic (angr), z3, patching
- **Anti-debug / obfuscation** found and how you bypassed it
- Common tags: `crackme` `keygen` `vm` `obfuscation` `anti-debug` `z3` `angr` `android` `dotnet` `wasm` `patching`

## 🔐 Crypto
- **Given values:** list them (n, e, c, IV...) and what's unusual about them
- **The math.** Write the weakness out with LaTeX or plain notation:
  > Since e = 3 and m³ < n, then c = m³ (no modular reduction) → m = ∛c
- **Which known attack** it is (name it: Wiener, Håstad, Coppersmith, padding oracle, nonce reuse...)
- **Sage/Python script**
- Common tags: `rsa` `aes-ecb` `aes-cbc` `padding-oracle` `xor` `lcg` `ecc` `lattice` `hash-length-extension` `classical`

## 🧪 Forensics
- **Artifact type:** pcap, memory dump, disk image, logs, docs
- **Tool and exact command** (Volatility plugin names, Wireshark filters)
  ```
  vol -f mem.raw windows.pslist
  tshark -r cap.pcap -Y 'http.request' -T fields -e http.request.uri
  ```
- **Timeline** (if relevant): what happened, in what order
- **Where the flag was hidden** and how you'd spot it next time
- Common tags: `pcap` `memory` `volatility` `disk` `autopsy` `logs` `file-carving` `usb-hid` `registry` `malware`

## 🖼️ Stego
- **Checklist of what you ran.** Even the negatives help next time:
  `file` → `exiftool` → `strings` → `binwalk` → `zsteg` / `steghide` / `stegseek` → `aperisolve` → spectrogram (audio)
- **Which tool or technique hit**, plus the password if one was needed
- Common tags: `lsb` `exif` `appended-data` `spectrogram` `steghide` `polyglot`

## 🕵️ OSINT
- **Pivot chain.** The most important part. Each clue → what it led to:
  ```
  username in image → GitHub profile → old commit email → Strava → home location
  ```
- **Screenshots** (pages change and disappear, so capture them)
- **Tools/sites used** (Google dorks, Wayback, reverse image search, Overpass)
- Common tags: `geoint` `socmint` `dorking` `wayback` `reverse-image` `metadata`

## 🎲 Misc / Jail / Programming
- **Restrictions** (blacklisted chars, builtins removed, length limits)
- **Bypass explained** char by char if needed
- Common tags: `pyjail` `bashjail` `esolang` `scripting` `qr` `encoding` `game`

## ⛓️ Blockchain
- **Contract source** (vulnerable function highlighted), chain, solidity version
- **Attack contract plus deploy/interaction commands** (foundry `cast`/`forge`)
- Common tags: `reentrancy` `delegatecall` `tx-origin` `storage` `integer-overflow` `flashloan`

## 🔌 Hardware / RF / IoT
- **Signal/protocol identification** (logic analyzer, URH, baud rate, UART/SPI/I2C)
- **Decoding steps** with screenshots of waveforms
- Common tags: `uart` `spi` `i2c` `sdr` `firmware` `side-channel`

## 🤖 AI / ML
- **Model/system behaviour** observed, guardrails present
- **Prompt(s) that worked** verbatim, plus the ones that didn't
- Common tags: `prompt-injection` `model-inversion` `adversarial` `pickle`
