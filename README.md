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

## 🔒 Live CTFs — hiding flags

Some events are still **running** (e.g. CyLab Academy challenges). Publishing their flags spoils them for others and usually breaks the platform's rules, so this repo hides them:

```bash
python ctf.py live cylabCTF        # mark an event as live (creates cylabCTF/LIVE.md)
python ctf.py                      # hides every flag in live events + rebuilds tables
python ctf.py check                # scan for leaked live flags (exit 1 if any)
python ctf.py install-hook         # run `check` automatically before every commit
python ctf.py reveal cylabCTF      # event over? put the real flags back
```

- Write the **real flag** in your writeup like normal. `python ctf.py` moves it into `.flags.local.json` (git-ignored, only on your machine) and replaces it with `[FLAG HIDDEN]`.
- Index tables show `🔒 hidden (live CTF)` for those challenges.
- One challenge can override its event with `live: true` / `live: false` in its frontmatter.
- Each teammate should run `python ctf.py install-hook` once after cloning — git hooks aren't shared by `git clone`.

> **During a live CTF**, keep rough notes in a `notes.md` next to the writeup and save the challenge files into a `files/` folder (servers go offline when the event ends). Tidy into the writeup afterwards.

## Find a past technique
```bash
grep -rl "ret2libc" --include=README.md .
```

## Events

<!-- AUTO-INDEX:START -->
| Event | Solved | Status |
|---|---|---|
| [CyberWeek 2026](2026-cyberweek-finals/) | 64 / 65 | ✅ finished |
| [cylabCTF](cylabCTF/) | 2 / 3 | 🔒 live — flags hidden |
| [HellBoundHackers](HellBoundHackers/) | 0 / 1 | 🔒 live — flags hidden |
<!-- AUTO-INDEX:END -->
