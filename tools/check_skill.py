#!/usr/bin/env python3
"""Repository checks for the Horological skill.

Checks:
  1. SKILL.md has YAML frontmatter with name and description.
  2. Every references/ and scripts/ path mentioned in skill files exists.
  3. Every reference file is reachable from SKILL.md.
  4. No em dashes or en dashes in skill files, per the style guide.
  5. evals.json parses and every "reads" path exists.

Exit code is non-zero if any check fails.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "horological"
SKILL_MD = SKILL_DIR / "SKILL.md"
PATH_RE = re.compile(r"`((?:references|scripts)/[A-Za-z0-9_./-]+)`")
BARE_REF_RE = re.compile(r"`([a-z0-9-]+\.md)`")
FORBIDDEN = {"—": "em dash", "–": "en dash"}


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def main() -> int:
    errors: list[str] = []

    text = SKILL_MD.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail(errors, "SKILL.md: missing frontmatter")
    else:
        fm = m.group(1)
        for key in ("name:", "description:"):
            if key not in fm:
                fail(errors, f"SKILL.md: frontmatter missing {key}")
        desc = re.search(r"^description:\s*(.+)$", fm, re.M)
        # The API allows 1024 characters; some upload paths are stricter, so stay under 200.
        if desc and len(desc.group(1)) > 200:
            fail(errors, "SKILL.md: description over 200 characters")

    ref_files = sorted((SKILL_DIR / "references").glob("*.md"))
    ref_names = {p.name for p in ref_files}
    linked_from_skill = set()

    for path in [SKILL_MD, *ref_files]:
        body = path.read_text(encoding="utf-8")
        for ch, name in FORBIDDEN.items():
            if ch in body:
                line = body[: body.index(ch)].count("\n") + 1
                fail(errors, f"{path.relative_to(ROOT)}:{line}: contains {name}")
        for rel in PATH_RE.findall(body):
            target = SKILL_DIR / rel
            if not target.exists():
                fail(errors, f"{path.relative_to(ROOT)}: broken path {rel}")
            if path == SKILL_MD and rel.startswith("references/"):
                linked_from_skill.add(Path(rel).name)
        if path != SKILL_MD:
            for name in BARE_REF_RE.findall(body):
                if name not in ref_names:
                    fail(errors, f"{path.relative_to(ROOT)}: cross-reference to missing {name}")

    for name in ref_names - linked_from_skill:
        fail(errors, f"references/{name} is not linked from SKILL.md")

    evals_path = ROOT / "evals" / "evals.json"
    try:
        evals = json.loads(evals_path.read_text(encoding="utf-8"))
        for case in evals["cases"]:
            for rel in case.get("reads", []):
                if not (SKILL_DIR / rel).exists():
                    fail(errors, f"evals case {case['id']}: missing {rel}")
    except (OSError, ValueError, KeyError) as exc:
        fail(errors, f"evals.json: {exc}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  {e}")
        return 1
    print(f"OK: {len(ref_files)} reference files, SKILL.md links verified, no dashes, evals valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
