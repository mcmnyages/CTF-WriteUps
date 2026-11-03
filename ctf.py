#!/usr/bin/env python3
"""
ctf.py — the only tool you need for this writeups repo.

  python ctf.py new <event-folder>/<category>/<challenge>
        Create a new challenge writeup from the template, ready to fill in.
        Example:  python ctf.py new 2026-cyberweek-finals/web/my-new-chall

  python ctf.py            (or:  python ctf.py index)
        Rebuild every index/table automatically from the writeups.
        Before building, flags of LIVE events are automatically hidden (see below).

  python ctf.py check
        Scan for real flags inside LIVE events. Exits with an error if any are
        found, so it can block a commit. (`install-hook` runs it on every commit.)

  python ctf.py install-hook
        Install a git pre-commit hook that runs `check` before every commit.

  python ctf.py live <event-folder>
        Mark an event as live/ongoing: its flags get hidden from the repo.

  python ctf.py reveal <event-folder>
        The event has ended / retired: put the real flags back and un-mark it.

LIVE EVENTS (hiding flags of real, still-running CTFs)
  An event folder containing a LIVE.md file is "live". For every writeup in it:
    * the real flag is moved into  .flags.local.json  (git-ignored, stays on
      your machine only), and
    * every copy of the flag in the writeup is replaced with  [FLAG HIDDEN]
    * index tables show "🔒 hidden (live CTF)" instead of the flag.
  You still write the real flag in the writeup as usual — `python ctf.py`
  hides it for you. One challenge can override its event with `live: true`
  or `live: false` in its frontmatter.

Everything in the index tables is read from the little block at the top of
each challenge's README.md (the part between the --- lines). You never edit a
table by hand. If you don't want to run the script yourself, just tell Claude
"rebuild the CTF index" and it will run this for you.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "_templates" / "writeup.md"
LIVE_MARKER = "LIVE.md"
FLAG_STORE = ROOT / ".flags.local.json"
HIDDEN = "[FLAG HIDDEN]"

# Nice headings for known folders; anything else uses the folder name as-is.
FOLDER_TITLES = {
    "heritage-trail": "🗺️ Heritage Trail",
    "blackstar": "🛰️ BLACKSTAR",
    "kivuli": "🕶️ Kivuli",
    "together": "🤝 Together",
    "blackout-protocol": "⚡ The Blackout Protocol",
    "lost-signal": "📻 The Lost Signal",
    "tidebreaker": "🌊 TIDEBREAKER",
    "gridlock": "🔌 GRIDLOCK",
    "invisible-courier": "📦 The Invisible Courier",
    "sc-series": "🔬 SC Series",
    "web": "🌐 Web",
    "forensics": "🧪 Forensics",
    "osint": "🕵️ OSINT",
    "crypto": "🔐 Crypto",
    "pwn": "💥 Pwn",
    "rev": "🔍 Reverse Engineering",
    "reverse-engineering": "🔍 Reverse Engineering",
    "stego": "🖼️ Stego",
    "misc": "🎲 Misc",
}
# Preferred order of folders in the master index; unknown folders go last, A-Z.
FOLDER_ORDER = list(FOLDER_TITLES.keys())

START = "<!-- AUTO-INDEX:START -->"
END = "<!-- AUTO-INDEX:END -->"

# Leading HTML comments (like the template's "how to use" note) are allowed above the block.
FM_RE = re.compile(r"^\s*(?:<!--.*?-->\s*)*---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n", re.DOTALL)
# Anything that looks like a flag: prefix{...}. Used by `check` as a safety net.
FLAG_LIKE = re.compile(r"\b[A-Za-z][A-Za-z0-9_]{1,24}\{[^\s{}]{3,}\}")
PLACEHOLDER_FLAGS = {"", "unsolved", "flag{...}", HIDDEN.lower()}


# ---------------------------------------------------------------- helpers
def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write(p: Path, text: str):
    p.write_text(text, encoding="utf-8")


def parse_frontmatter(readme: Path) -> dict:
    """Read the --- ... --- block at the top of a README into a dict."""
    m = FM_RE.match(read(readme))
    data = {}
    if not m:
        return data
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, val = line.partition(":")
        val = re.sub(r"\s+#.*$", "", val).strip().strip('"').strip("'")  # drop inline comments
        data[key.strip()] = val
    return data


def is_solved(fm: dict) -> bool:
    status = (fm.get("status") or "solved").lower()
    flag = (fm.get("flag") or "").lower()
    return status.startswith("solved") and (flag not in PLACEHOLDER_FLAGS or flag == HIDDEN.lower())


def challenge_readmes(event_dir: Path):
    return sorted(event_dir.glob("*/*/README.md"))


def event_dirs():
    return sorted(d for d in ROOT.iterdir()
                  if d.is_dir() and not d.name.startswith((".", "_")) and any(d.glob("*/*/README.md")))


def is_live(readme: Path, fm: dict) -> bool:
    override = (fm.get("live") or "").lower()
    if override in ("true", "yes"):
        return True
    if override in ("false", "no"):
        return False
    event_dir = readme.parent.parent.parent
    return (event_dir / LIVE_MARKER).exists()


def key_of(readme: Path) -> str:
    return readme.parent.relative_to(ROOT).as_posix()


def load_store() -> dict:
    return json.loads(read(FLAG_STORE)) if FLAG_STORE.exists() else {}


def save_store(store: dict):
    write(FLAG_STORE, json.dumps(store, indent=2, sort_keys=True) + "\n")


# ---------------------------------------------------------------- hiding / revealing
def hide_flag(readme: Path, store: dict) -> bool:
    """Move the real flag out of a writeup into the local store. Returns True if changed."""
    fm = parse_frontmatter(readme)
    flag = fm.get("flag") or ""
    if flag.lower() in PLACEHOLDER_FLAGS:
        return False
    text = read(readme)
    store[key_of(readme)] = flag
    text = text.replace(flag, HIDDEN)
    write(readme, text)
    return True


def reveal_flag(readme: Path, store: dict) -> bool:
    flag = store.get(key_of(readme))
    if not flag:
        return False
    text = read(readme)
    if HIDDEN not in text:
        return False
    write(readme, text.replace(HIDDEN, flag))
    del store[key_of(readme)]
    return True


def hide_live_flags(verbose=True) -> int:
    store, n = load_store(), 0
    for ev in event_dirs():
        for readme in challenge_readmes(ev):
            if is_live(readme, parse_frontmatter(readme)) and hide_flag(readme, store):
                n += 1
                if verbose:
                    print(f"  🔒 hid flag in {key_of(readme)} (saved locally in {FLAG_STORE.name})")
    if n:
        save_store(store)
    return n


def find_leaks():
    """Yield (path, line_no, text) for flag-looking strings in live writeups and their indexes."""
    store = load_store()
    real_flags = set(store.values())
    files = set()
    for ev in event_dirs():
        for readme in challenge_readmes(ev):
            fm = parse_frontmatter(readme)
            if is_live(readme, fm):
                files.add(readme)
                if fm.get("flag", "").lower() not in PLACEHOLDER_FLAGS:
                    real_flags.add(fm["flag"])
    # Index pages anywhere could contain a copy of a live flag.
    index_pages = [ROOT / "README.md"] + [p for ev in event_dirs()
                                          for p in [ev / "README.md", *ev.glob("*/README.md")]]
    for path in sorted(files | {p for p in index_pages if p.exists()}):
        for i, line in enumerate(read(path).splitlines(), 1):
            hits = [f for f in real_flags if f in line]
            if path in files:
                hits += [m.group(0) for m in FLAG_LIKE.finditer(line)
                         if "..." not in m.group(0) and "<" not in m.group(0)]
            if hits:
                yield path, i, sorted(set(hits))


# ---------------------------------------------------------------- index building
def fmt_tags(raw: str) -> str:
    raw = (raw or "").strip().strip("[]")
    tags = [t.strip() for t in raw.split(",") if t.strip()]
    return ", ".join(f"`{t}`" for t in tags[:4])


def flag_cell(fm: dict, live: bool) -> str:
    if not is_solved(fm):
        return "⛔ **unsolved**"
    if live or fm.get("flag") == HIDDEN:
        return "🔒 hidden (live CTF)"
    return f"`{fm['flag']}`"


def table_header() -> str:
    return "| Challenge | Difficulty | Tags | Flag |\n|---|---|---|---|"


def row(name: str, link: str, fm: dict, live: bool) -> str:
    diff = (fm.get("difficulty") or "-").lower()
    return f"| [{name}]({link}) | {diff} | {fmt_tags(fm.get('tags', ''))} | {flag_cell(fm, live)} |"


def write_between_markers(readme: Path, body: str, title_line: str):
    """Insert/replace the AUTO-INDEX block in a README, creating it if needed."""
    block = f"{START}\n{body}\n{END}"
    if readme.exists():
        text = read(readme)
        if START in text and END in text:
            text = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.DOTALL)
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
    else:
        text = f"{title_line}\n\n{block}\n"
    write(readme, text)


def folder_sort_key(name: str):
    return (FOLDER_ORDER.index(name) if name in FOLDER_ORDER else len(FOLDER_ORDER), name)


def rebuild_event(event_dir: Path):
    """Rebuild the event README plus each sub-folder README. Returns (total, solved, live)."""
    groups = {}  # folder_name -> list[(challenge_dir_name, fm, live)]
    for readme in challenge_readmes(event_dir):
        fm = parse_frontmatter(readme)
        groups.setdefault(readme.parent.parent.name, []).append(
            (readme.parent.name, fm, is_live(readme, fm)))
    if not groups:
        return 0, 0, False

    entries = [e for v in groups.values() for e in v]
    total, solved = len(entries), sum(1 for _, fm, _ in entries if is_solved(fm))
    event_live = (event_dir / LIVE_MARKER).exists()

    parts = []
    if event_live:
        parts.append("> 🔒 **Live CTF — flags are hidden.** These challenges are still running, "
                     "so only the method is shared. Solve them yourself! (see `LIVE.md`)\n")
    parts.append(f"**{total} challenges — {solved} solved, {total - solved} unsolved.** "
                 "Tables below are generated by `ctf.py`; don't edit them by hand.\n")
    for folder in sorted(groups, key=folder_sort_key):
        rows = sorted(groups[folder], key=lambda x: x[0])
        title = FOLDER_TITLES.get(folder, folder)
        parts += [f"### {title}", table_header()]
        parts += [row(fm.get("title") or name, f"{folder}/{name}/", fm, live) for name, fm, live in rows]
        parts.append("")
        fbody = table_header() + "\n" + "\n".join(
            row(fm.get("title") or name, f"{name}/", fm, live) for name, fm, live in rows)
        write_between_markers(event_dir / folder / "README.md", fbody, f"# {title}")
    write_between_markers(event_dir / "README.md", "\n".join(parts).rstrip(), f"# {event_dir.name}")
    return total, solved, event_live


def event_title(event_dir: Path) -> str:
    m = re.search(r"^#\s+(.+)$", read(event_dir / "README.md"), re.MULTILINE)
    return m.group(1).strip() if m else event_dir.name


def cmd_index():
    hidden = hide_live_flags()
    rows, grand = [], 0
    for ev in event_dirs():
        total, solved, live = rebuild_event(ev)
        grand += total
        status = "🔒 live — flags hidden" if live else "✅ finished"
        rows.append(f"| [{event_title(ev)}]({ev.name}/) | {solved} / {total} | {status} |")
        print(f"  {ev.name}: {total} challenges indexed{' (live, flags hidden)' if live else ''}")
    body = "| Event | Solved | Status |\n|---|---|---|\n" + "\n".join(rows)
    write_between_markers(ROOT / "README.md", body, "# CTF Writeups")
    print(f"Done. {grand} challenges across {len(rows)} event(s)"
          f"{f', {hidden} flag(s) newly hidden' if hidden else ''}. Review & commit when ready.")


def cmd_check() -> int:
    leaks = list(find_leaks())
    if not leaks:
        print("✅ No live-CTF flags found in the repo.")
        return 0
    print("❌ Possible live-CTF flags found:")
    for path, line, hits in leaks:
        print(f"  {path.relative_to(ROOT).as_posix()}:{line}  {', '.join(hits)}")
    print("\nRun `python ctf.py` to hide them automatically, then commit again.")
    return 1


def cmd_install_hook():
    git_dir = Path(subprocess.check_output(["git", "rev-parse", "--git-dir"], cwd=ROOT, text=True).strip())
    hook = (ROOT / git_dir if not git_dir.is_absolute() else git_dir) / "hooks" / "pre-commit"
    hook.write_text(
        "#!/bin/sh\n"
        "# Installed by `python ctf.py install-hook`: block commits that contain live-CTF flags.\n"
        'cd "$(git rev-parse --show-toplevel)" || exit 1\n'
        "PY=python; command -v python >/dev/null 2>&1 || PY=python3\n"
        "command -v $PY >/dev/null 2>&1 || PY=py\n"
        "$PY ctf.py check\n", encoding="utf-8", newline="\n")
    try:
        hook.chmod(0o755)
    except OSError:
        pass
    print(f"Installed pre-commit hook: {hook}")


def cmd_live(event: str):
    ev = ROOT / event
    if not ev.is_dir():
        sys.exit(f"No such event folder: {ev}")
    (ev / LIVE_MARKER).write_text(
        "# 🔒 Live CTF\n\n"
        "This event is still **running/active**, so the real flags are **hidden** in these writeups.\n"
        "The writeups explain the *method*; please solve the challenges yourself and don't share flags.\n\n"
        "_Maintainer: when the event ends, run `python ctf.py reveal "
        f"{ev.name}` to restore the flags._\n", encoding="utf-8")
    print(f"Marked {ev.name} as live.")
    cmd_index()


def cmd_reveal(event: str):
    ev = ROOT / event
    if not ev.is_dir():
        sys.exit(f"No such event folder: {ev}")
    store, n, missing = load_store(), 0, []
    for readme in challenge_readmes(ev):
        if reveal_flag(readme, store):
            n += 1
        elif HIDDEN in read(readme):
            missing.append(key_of(readme))
    save_store(store)
    if missing:
        print("⚠️  No saved flag for (fill these in by hand):\n  " + "\n  ".join(missing))
    marker = ev / LIVE_MARKER
    if marker.exists():
        marker.unlink()
    print(f"Revealed {n} flag(s) in {ev.name}; it is no longer marked live.")
    cmd_index()


def cmd_new(rel: str):
    dest = ROOT / rel / "README.md"
    if dest.exists():
        sys.exit(f"Already exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(read(TEMPLATE), encoding="utf-8")
    ev = ROOT / Path(rel).parts[0]
    print(f"Created {dest}")
    if (ev / LIVE_MARKER).exists():
        print("🔒 This event is LIVE: write the real flag normally — `python ctf.py` will hide it.")
    print("Fill it in, then run:  python ctf.py")


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):  # emoji-safe output on Windows consoles
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = sys.argv[1:]
    one_arg = {"new": cmd_new, "live": cmd_live, "reveal": cmd_reveal}
    if args and args[0] in one_arg:
        if len(args) != 2:
            sys.exit(f"Usage: python ctf.py {args[0]} <folder>")
        one_arg[args[0]](args[1].rstrip("/\\"))
    elif args == ["check"]:
        sys.exit(cmd_check())
    elif args == ["install-hook"]:
        cmd_install_hook()
    elif not args or args == ["index"]:
        cmd_index()
    else:
        sys.exit(__doc__)
