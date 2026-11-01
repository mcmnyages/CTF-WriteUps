---
title: "The Poisoned Evidence"
event: "CyberWeek 2026"
series: "The Blackout Protocol"
category: forensics
difficulty: advanced
points: 500
status: solved
flag: "FLAG{BP04_14D8F1BCE88A}"
tags: [prompt-injection, ai-security, retrieval-poisoning, evidence-integrity]
---

# The Poisoned Evidence

> **TL;DR:** A single sealed external note carried a fake "priority instruction" that prompt-injected an automated summarizer into blaming maintenance; treating notes as evidence (never commands) and independently verifying the signed incident chain reveals the real, different incident and yields the token.

## Background (for beginners)
- Prompt injection is when attacker-controlled text that an AI reads is treated as instructions rather than as data, hijacking the AI's behavior.
- Retrieval poisoning is prompt injection delivered through documents an automated system retrieves — a low-trust external file tells the AI to ignore real evidence.
- Golden rule: content you ingest is **evidence to examine**, never an **order to follow**. Verify integrity seals/checksums and provenance before trusting any note.
- This is an AI-security lesson: automated summarizers must not take instructions from the data they summarize.

## The Challenge
The Chapter 3 token unlocks ingested third-party notes, an automated incident-report log, a signed controller event journal, clock offsets, and monitor receipts. One automated report concluded the blackout was "authorised maintenance." Tools: Python stdlib.

## Key Insight 💡
One genuine sealed outside note was **crafted to look like an order to an AI summarizer**, telling it to ignore the real evidence and blame maintenance — and exactly one report had retrieved it and been swayed. The note is poison, not a conclusion.

## Solution
1. **Unlock with the Chapter 3 token** and load every source. (WHY: each chapter's token unlocks the next.)
2. **Treat every retrieved note as evidence to examine, never as an instruction.** (WHY: that discipline is the entire defense against the injection.)
3. **Check each note's ingestion seal/checksum:** most are fine, two are tampered/unsealed, and one is only a quoted training example. (WHY: integrity and provenance determine which notes are even admissible.)
4. **Isolate the one genuine sealed note containing the fake "priority instruction,"** and the one report that retrieved and was misled by it. (WHY: this identifies the poisoned-note / misled-report pair.)
5. **Separately verify every candidate incident chain** — four signed stages with no broken links, clock-corrected timestamps, and independent monitor confirmation — and keep only the one that passes everything and falls in the window. (WHY: the true cause must be established from untainted evidence, independent of the misleading report.)
6. **Note the real incident differs from what the report blamed**, then combine the poisoned-note + misled-report + real-incident IDs + witness confirmation with the formula for the token. (WHY: the formula binds the full picture — the attack and the truth — to the flag.)

## Why It Worked (the vulnerability)
A low-trust external document instructed an automated summarizer to disregard verified evidence and report a false cause — prompt injection via poisoned retrieval. The summarizer failed to separate data from instructions. **Fix:** never let retrieved/ingested content act as instructions; enforce provenance and integrity checks and keep AI summarization strictly subordinate to verified evidence.

## Flag
```
FLAG{BP04_14D8F1BCE88A}
```

## Takeaways
- Retrieved content is data, not commands — the moment an AI obeys it, it is compromised.
- Integrity seals and provenance filter poisoned, tampered, and example notes from real evidence.
- Always establish the true cause from independently verified chains, not from the automated report.

## Chain Note
**The Blackout Protocol** is a chained series where each chapter's token unlocks the next. Chapter 4 takes the Chapter 3 token (`FLAG{BP03_...}`) as input to unlock its evidence set and outputs `FLAG{BP04_...}` as the series' final token.
