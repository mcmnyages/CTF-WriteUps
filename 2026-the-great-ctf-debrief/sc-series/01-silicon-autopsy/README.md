---
title: "Silicon Autopsy"
event: "The Great CTF Debrief 2026"
series: "SC Series"
category: rev
difficulty: HARD
points: 450
status: solved
flag: "FLAG{SC01_9FC62E7A8B45}"
tags: [firmware, custom-vm, eeprom, reverse-engineering]
---

# Silicon Autopsy

> **TL;DR:** Reverse a tiny custom-VM firmware whose four stages each transform five payload bytes; descramble the EEPROM wiring, invert each stage's math while carrying a shared latch, and send four correct frames in order to open the capsule.

## Background (for beginners)
- **Firmware reverse engineering** means disassembling low-level code to understand what inputs it will accept.
- A **custom instruction set / VM** is a bespoke bytecode interpreter — you must learn its opcodes before you can read the logic.
- **EEPROM** memory can be **address-scrambled** in hardware (its pins wired in a non-obvious order), so a raw dump's bytes are in the wrong logical positions until you undo the wiring.
- An **invertible per-byte transform** (XOR, add, rotate, substitution) can be run backwards to compute the exact input that yields a desired output.

## The Challenge
Firmware was supplied with an offline test bench. It runs a tiny custom instruction set and dispatches to one of four stages via a stage counter. Each stage checks the five payload bytes of a frame by: XOR with an EEPROM byte, add a rolling latch, rotate left, look up in an EEPROM substitution table, and compare to a fixed target.

## Key Insight 💡
Every stage's byte transform is fully invertible, so the required payload can be computed backwards from the fixed target — *but* only after correcting the physically scrambled EEPROM, and the **shared latch carried between stages** means frames only work together, in order.

## Solution
1. **Disassemble** the firmware with the bench and map the custom VM's opcodes and the four-stage dispatch. *Why: you cannot invert logic you cannot read.*
2. **Model each stage** — XOR with EEPROM byte, add rolling latch, rotate left, EEPROM sub-table lookup, compare to fixed target. *Why: defines the exact transform to invert.*
3. **Descramble EEPROM** — apply the documented address wiring (swap lines A0/A3, invert A5) to read correct logical bytes and the sub-table. *Why: the dump is physically scrambled; wrong bytes give wrong math.*
4. **Invert the math** — work each stage backwards to recover the required payload bytes, carrying the shared latch from one stage into the next. *Why: inversion yields the inputs that pass each check.*
5. **Add CRC-8** per frame, then send four frames in order. *Why: the stage counter and chained latch require the correct sequence; all stages then pass and the capsule opens.*

## Why It Worked (the vulnerability / technique)
Once the custom VM is understood and the EEPROM scrambling undone, each per-byte transform is invertible, so inputs can be synthesized to pass every check. The chained latch is the twist: frames are only valid together and in order. **Defensive note:** obfuscation via scrambled memory and custom VMs slows but does not stop a determined reverser.

## Flag
```
FLAG{SC01_9FC62E7A8B45}
```

## Takeaways
- Map the custom instruction set before anything else.
- Hardware address scrambling must be reversed before EEPROM data makes sense.
- Invertible transforms let you compute required inputs directly — but watch for state (the latch) that chains frames together.

## Chain Note
SC01 of the cross-category **SC Series** (SC01/SC02/SC03), which spans reverse engineering, web, and stego challenges.
