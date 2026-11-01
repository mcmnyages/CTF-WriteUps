# Adding a writeup (team guide)

Welcome! This repo keeps all our CTF writeups in one consistent shape. Adding one takes ~2 minutes of setup; the rest is just writing up how you solved it.

## The rule: one challenge = one folder

```
<event>/<category-or-series>/<challenge-name>/README.md
```
Lowercase, dashes for spaces. Examples: `2026-some-ctf/web/sneaky-login/`, `2026-some-ctf/blackstar/03-flight-computer/`.

## Steps (copy-paste)

```bash
# 1. get the repo
git clone <repo-url> && cd CTFs
git pull                                   # always start fresh so you don't clash with teammates

# 2. make your writeup folder from the template
python ctf.py new 2026-some-ctf/web/my-challenge

# 3. open the new README.md and fill it in (see "What to fill" below)

# 4. rebuild the index tables (automatic — never edit tables by hand)
python ctf.py

# 5. push it
git add -A
git commit -m "writeup: my-challenge (web)"
git push
```

> Don't hand-edit any index table or the sections between `<!-- AUTO-INDEX -->` markers — `python ctf.py` writes those for everyone.

## What to fill in

1. **The frontmatter block** at the very top (between the `---` lines). These fields feed the index tables, so get them right:
   - `title`, `category`, `difficulty`, `status`, `flag`, `tags` — required-ish
   - `author` — **put your name/handle** so we know who solved it
   - `series` — the series name for chained challenges, else `Standalone`
2. **The writeup body.** Minimum that's still useful: **TL;DR + Key Insight + Solution + Flag**. Add Background (for beginners), Why It Worked, Takeaways when you have time. Optional Recon / Dead Ends / Solve Script sections are there for pwn/rev/crypto.

## Write for two readers
- A **beginner** on the team should be able to follow it.
- An **expert** should be able to skim the TL;DR and solution and move on.
- Save the challenge files into a `files/` folder in your challenge dir — the server dies when the event ends.

## Working as a team during a live CTF
- Agree who takes which challenge (avoid two people doing the same one).
- Keep rough notes in a `notes.md` next to your writeup while you work; tidy it into the README after.
- `git pull` before you `push`. If two people added different challenges and git complains, it's almost always a clean auto-merge; if a conflict is in an index table, just run `python ctf.py` again and it regenerates correctly.

That's it. If in doubt, open any existing writeup in `2026-the-great-ctf-debrief/` and copy its shape.
