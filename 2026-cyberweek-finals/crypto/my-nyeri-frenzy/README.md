---
title: "My Nyeri Frenzy"
event: "CyberWeek 2026"
series: "Standalone"
category: crypto
difficulty: advanced
points: 400
status: solved
flag: "FLAG{cwa_1s_th1s_4_r34lly_s3cur3_3ncrypt10n_a1g0r1thm}"
tags: [vigenere, brute-force, weak-keyspace, classical-cipher]
---

# My Nyeri Frenzy

> **TL;DR:** The encryption was a Vigenere cipher whose key is chosen at random from a fixed list of 100 crypto-themed words; brute-forcing all 100 candidate keys against the ciphertext yielded exactly one readable result under the key "ElGamal".

## Background (for beginners)
- A **Vigenere cipher** shifts each letter of the plaintext forward by a letter of a repeating secret keyword; digits and symbols are left unchanged.
- Decryption reverses it: `plain = cipher - key` for each aligned letter, with the key repeating across the message.
- A **key space** is the set of all possible keys. Security depends on it being huge; if the key is drawn from a small, known list, the cipher is trivially broken.
- **Brute force** means simply trying every possible key — practical here because there are only 100 candidates.

## The Challenge
Provided: the encryption script and one encrypted file (`enc12.txt`). The script implements a Vigenere cipher and selects its key at random from a hard-coded list of 100 crypto-themed words. The task was to recover the plaintext flag.

## Key Insight 💡
The key is not secret in any meaningful sense — it is **one of 100 known words** embedded in the script. That reduces breaking the cipher to trying all 100 and spotting the one that produces readable English.

## Solution
1. **Read the encryption script** and recognize the algorithm as a Vigenere cipher (letters shifted forward by key letters, key repeats, digits/symbols untouched). *Why:* identifying the cipher dictates the inversion formula.
2. **Note that the key is randomly chosen from a fixed list of 100 words** in the script. *Why:* this collapses the key space from astronomical to a trivial 100 candidates.
3. **Write a decryptor** that reverses the shift (`plain = cipher - key`) and run it against `enc12.txt` with each of the 100 candidate keys. *Why:* exhaustive search over a known small key set is guaranteed to find the right key.
4. **Exactly one key — "ElGamal" — produces readable text**, revealing the flag. *Why:* wrong keys yield gibberish, so the single coherent output is the answer.

Illustrative decryptor (pseudocode):
```
for key in WORDLIST_100:
    pt = vigenere_decrypt(ciphertext, key)   # plain = cipher - key, mod 26
    if looks_like_english(pt):
        print(key, pt)   # -> "ElGamal", the flag
```

## Why It Worked (the vulnerability / technique)
Vigenere's strength assumes an unpredictable key. Here the key is drawn from only 100 published words, so the effective key space is tiny and brute force is instant. **Defensive note:** cryptographic strength lives in the key, not the algorithm's obscurity — never draw keys from a small enumerable set, and use vetted modern ciphers with full-entropy keys.

## Flag
```
FLAG{cwa_1s_th1s_4_r34lly_s3cur3_3ncrypt10n_a1g0r1thm}
```

## Takeaways
- A cipher is only as strong as its key space; 100 candidates is no security at all.
- Classical ciphers like Vigenere fall instantly to brute force when the key is constrained.
- "Readable output" is a reliable oracle for identifying the correct key among candidates.
