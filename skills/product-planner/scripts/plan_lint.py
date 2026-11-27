#!/usr/bin/env python3
"""Check a product-planner vault before handoff.

Usage: python3 plan_lint.py <vault-path>
Exit code 0 = pass (warnings allowed), 1 = errors found.
Output is short on purpose: one line per problem.
"""
import re
import sys
from pathlib import Path

KEYS = ["title", "created", "tags", "phase", "status", "route", "size", "depends_on", "constraints"]
ROUTES = {"feature", "fullstack-agent-crew"}
SIZES = {"small", "medium", "large"}
STATUSES = {"todo", "in-progress", "done"}
HEADINGS = [
    "## Goal", "## Run this phase", "## Constraints that apply", "## Already decided",
    "## Scope", "## Repo facts", "## Files", "## Tasks", "## Acceptance criteria",
    "## Tests", "## Stop and ask only if", "## Handoff", "## Completion note",
]
CREW_HEADINGS = ["## Contract draft", "## File ownership"]
BANNED_CASE = re.compile(r"\b(TBD|TODO|FIXME)\b|\?\?\?|<<[^<>\n]+>>")
BANNED_PHRASE = re.compile(r"\b(to be decided|to be determined|decide later)\b", re.I)


class _Banned:
    @staticmethod
    def search(text):
        return BANNED_CASE.search(text) or BANNED_PHRASE.search(text)


BANNED = _Banned()
ID_RE = re.compile(r"\b[SCR]-\d+\b")
WIKILINK = re.compile(r"\[\[([^\]\n]+)\]\]")

errors, warnings = [], []


def err(where, msg):
    errors.append(f"ERROR {where}: {msg}")


def warn(where, msg):
    warnings.append(f"WARN  {where}: {msg}")


def frontmatter(text):
    if not text.startswith("---"):
        return None
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return None
    data = {}
    for line in parts[0].splitlines()[1:]:
        m = re.match(r"^([A-Za-z_]+):\s*(.*?)\s*(#.*)?$", line)
        if m:
            data[m.group(1)] = m.group(2)
    return data


def as_list(value):
    inner = value.strip().strip("[]")
    return [x.strip() for x in inner.split(",") if x.strip()]


def main(vault):
    vault = Path(vault).expanduser()
    if not vault.is_dir():
        print(f"ERROR: vault not found: {vault}")
        return 1

    notes = {p.stem for p in vault.rglob("*.md") if ".obsidian" not in p.parts}
    exe = vault / "06-Execution"
    overview = exe / "Plan Overview.md"
    ledger = vault / "04-Reference" / "Constraints.md"
    status = vault / "05-Meta" / "Planning Status.md"
    openq = vault / "00-Inbox" / "Open Questions.md"

    for p in (overview, ledger, status):
        if not p.is_file():
            err(p.name, "missing")
    phases = sorted(exe.glob("Phase *.md")) if exe.is_dir() else []
    if not phases:
        err("06-Execution", "no phase files found")

    # Constraint ledger
    active_ids, known_ids = set(), set()
    if ledger.is_file():
        for line in ledger.read_text().splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 4 and re.fullmatch(r"[SCR]-\d+", cells[0]):
                known_ids.add(cells[0])
                state = cells[3].lower()
                if state == "proposed":
                    err("Constraints", f"{cells[0]} is still 'proposed' (user has not confirmed it)")
                if state != "dropped":
                    active_ids.add(cells[0])

    # Planning status
    if status.is_file():
        st = status.read_text()
        for key in ("open", "asked"):
            m = re.search(rf"^{key}:[ \t]*(.*)$", st, re.M)
            if m and re.search(r"[A-Z]\d+", m.group(1)):
                err("Planning Status", f"'{key}:' still lists items: {m.group(1).strip()}")
        if "not passed" in st:
            err("Planning Status", "a gate is still marked 'not passed'")

    # Open questions
    if openq.is_file():
        n = len(re.findall(r"^\s*- \[ \]", openq.read_text(), re.M))
        if n:
            err("Open Questions", f"{n} open question(s)")

    # Plan overview
    ov_text = overview.read_text() if overview.is_file() else ""
    if ov_text:
        if BANNED.search(ov_text):
            err("Plan Overview", "contains a placeholder or banned word (TBD, TODO, <<field>>, ...)")
        for cid in sorted(active_ids):
            if cid not in ov_text:
                err("Plan Overview", f"constraint {cid} is not in the traceability table")

    # Phase files
    numbers = []
    for p in phases:
        where = p.name
        text = p.read_text()
        m = re.match(r"Phase (\d+) - ", p.name)
        if not m:
            err(where, "file name must be 'Phase NN - Name.md'")
            continue
        num = int(m.group(1))
        numbers.append(num)
        if ov_text and f"[[{p.stem}]]" not in ov_text:
            err(where, "not linked from Plan Overview")

        fm = frontmatter(text)
        if fm is None:
            err(where, "missing frontmatter")
            continue
        for k in KEYS:
            if k not in fm:
                err(where, f"frontmatter key missing: {k}")
        if fm.get("phase", "").isdigit() and int(fm["phase"]) != num:
            err(where, "frontmatter phase does not match file name")
        if fm.get("route") not in ROUTES:
            err(where, f"route must be one of {sorted(ROUTES)}")
        if fm.get("size") not in SIZES:
            err(where, f"size must be one of {sorted(SIZES)}")
        if fm.get("status") not in STATUSES:
            err(where, f"status must be one of {sorted(STATUSES)}")

        for dep in as_list(fm.get("depends_on", "")):
            if not dep.isdigit():
                err(where, f"depends_on has a non-number: {dep}")
            elif int(dep) >= num:
                err(where, f"depends_on {dep} must be lower than {num}")
            elif not any(re.match(rf"Phase 0*{dep} - ", q.name) for q in phases):
                err(where, f"depends_on {dep}: no such phase file")

        lines = text.splitlines()
        heads = {l.strip() for l in lines if l.startswith("## ")}
        need = HEADINGS + (CREW_HEADINGS if fm.get("route") == "fullstack-agent-crew" else [])
        for h in need:
            if h not in heads:
                err(where, f"missing section: {h}")
        if fm.get("route") == "feature" and any(h in heads for h in CREW_HEADINGS):
            warn(where, "has crew sections but route is 'feature'")

        if len(lines) > 200:
            err(where, f"{len(lines)} lines; split the phase (limit 200)")
        elif len(lines) > 150:
            warn(where, f"{len(lines)} lines; aim for about 150")

        if BANNED.search(text):
            err(where, "contains TBD, TODO, 'decide later', or an unfilled <<field>>")

        ids = set(ID_RE.findall(text))
        listed = set(as_list(fm.get("constraints", "")))
        if not listed:
            err(where, "constraints list is empty")
        for cid in sorted(ids | listed):
            if known_ids and cid not in known_ids:
                err(where, f"unknown constraint id: {cid}")
        for cid in sorted(listed):
            if f"- {cid}:" not in text:
                err(where, f"constraint {cid} is listed but its text is not under 'Constraints that apply'")

        for target in WIKILINK.findall(text):
            name = target.split("|")[0].split("#")[0].strip()
            if name and name not in notes:
                err(where, f"broken link: [[{name}]]")

    if numbers and sorted(numbers) != list(range(1, max(numbers) + 1)):
        warn("06-Execution", f"phase numbers are not 1..N without gaps: {sorted(numbers)}")

    for line in errors + warnings:
        print(line)
    print(f"{len(phases)} phase(s) checked: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
