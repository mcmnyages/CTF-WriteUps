---
title: "The Downlink"
event: "CyberWeek 2026"
series: "BLACKSTAR"
category: forensics
difficulty: basic
points: 150
status: solved
flag: "FLAG{BS01_007161435C98}"
tags: [steganography, lsb, png, image-forensics]
---

# The Downlink

> **TL;DR:** A relay token was hidden in the least-significant bits of a PNG's RGB channels; extracting and concatenating those bits reveals `RELAY_TOKEN=007161435C98`.

## Background (for beginners)
- **Steganography** hides data inside otherwise-normal files so nothing looks suspicious at a glance.
- **LSB (least-significant-bit) stego** flips the lowest bit of each color value. Changing a pixel's red from 200 to 201 is invisible to the eye but carries one bit of secret data.
- Each pixel has R, G, and B channels, so every pixel can smuggle 3 bits. Join enough bits and you reconstruct hidden text.
- It matters because image files are trusted and shared freely, making them an ideal covert channel.

## The Challenge
A downlinked PNG image was captured. Nothing obvious stood out, and the task was to recover the hidden relay token embedded in it.

## Key Insight 💡
The data wasn't appended or in a custom chunk — it was spread across the pixels themselves, one bit per color channel.

## Solution
1. **Checked PNG structure** for extra/hidden chunks or appended data — found none, ruling out the easy hiding spots and pointing to pixel-level stego.
2. **Extracted the lowest bit** of every R, G, and B value across the image, in order — this is where LSB stego stores its payload.
3. **Joined the bits into bytes**, which decoded to the ASCII string `RELAY_TOKEN=007161435C98` (a 12-character hex token).
4. **Wrapped the token** in the flag format to finish.

## Why It Worked (the vulnerability)
LSB encoding is undetectable visually but trivially recoverable once you know to read the low bits — there is no key protecting it. *Defensive fix:* treat embedded data as untrusted and, for sensitive channels, use integrity checks or re-encode/compress images to destroy stego payloads.

## Flag
```
FLAG{BS01_007161435C98}
```

## Takeaways
- Always check both file structure (chunks/trailing data) **and** pixel data when hunting stego.
- Spotting LSB stego: visually clean image + a payload that only appears after reading low bits per channel.

## Chain Note
This is the first stage of the BLACKSTAR chain. **Token out:** `007161435C98` — this relay token feeds directly into Stage 2 (The Uplink) as the AES key material.
