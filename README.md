# CTF Writeups

My personal CTF writeups. Every challenge I solve gets a short, readable writeup so I (and anyone reading) can see exactly how it was done — beginner-friendly but with the technical detail experts want.

## The whole system in 30 seconds
- **One challenge = one folder** with a `README.md` inside it.
- Each writeup starts with a small `--- ... ---` info block (category, difficulty, flag, tags). **That block is the source of truth.**
- `ctf.py` reads those blocks and **builds all the index tables automatically**. You never edit a table by hand.
- Open an event's `README.md` to browse; click a challenge to read it.

## Layout

```
CTFs/
├── README.md                 ← this page (list of events)
├── ctf.py                    ← the only tool: makes new writeups + rebuilds all indexes
├── _templates/               ← blank templates (writeup, per-category sections, scratch notes)
└── <YYYY-event-name>/
    ├── README.md             ← auto-built index of the event
    └── <category-or-series>/ ← e.g. web/  or  blackstar/
        └── <challenge-name>/
            └── README.md     ← the writeup
```

## Adding a challenge — two ways, both easy

**A) Let Claude do it.** Just say: *"write up `<challenge>` for `<event>`"* (paste the challenge + how you solved it). Claude creates the folder and runs the rebuild.

**B) Do it yourself.** From this `CTFs/` folder:
```bash
python ctf.py new 2026-some-ctf/web/my-challenge   # makes the folder + a blank writeup
# ... fill in the README.md it created ...
python ctf.py                                       # rebuilds every index table
git add -A && git commit -m "add my-challenge writeup" && git push
```

That's the whole routine. `python ctf.py` with no arguments is safe to run anytime — it just refreshes the tables.

> **During a live CTF**, keep rough notes in a `notes.md` next to the writeup and save the challenge files into a `files/` folder (servers go offline when the event ends). Tidy into the writeup afterwards.

## Find a past technique
```bash
grep -rl "ret2libc" --include=README.md .
```

## Events

| Event | Date | Solved | Writeups |
|---|---|---|---|
| [The Great CTF Debrief 2026](2026-the-great-ctf-debrief/) | 2026 | 64 / 65 | 65 challenges across 14 series/categories |
