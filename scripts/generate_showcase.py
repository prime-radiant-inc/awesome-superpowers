# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6,<7"]
# ///
"""Generate showcase.yaml from the project entries in README.md."""

import argparse
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
ENTRY = re.compile(r"- \[([^\]]+)\]\((\S+)\) - (.+)")
REPOSITORY = re.compile(r"https?://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)/?")
INLINE_LINK = re.compile(r"\[([^\]]+)\]\(([^\s)]+)\)")
HEADER = "# Generated from README.md; do not edit directly.\n# Run: uv run scripts/generate_showcase.py\n\n"


def parse_readme(text: str) -> list[dict]:
    """Read one-line entries under category headings, keeping README order.

    Contents and Contributing are not project sections. Every nonempty line
    within a category must be an entry; fail rather than silently omit it.
    """
    entries = []
    repositories = set()
    in_category = False
    for number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if line.startswith("## "):
            heading = line[3:].strip()
            if heading == "Contributing":
                break
            in_category = heading != "Contents"
            continue
        if not in_category or not line:
            continue

        match = ENTRY.fullmatch(line)
        if not match:
            raise ValueError(f"Invalid project entry at README.md line {number}")
        name, url, description = (value.strip() for value in match.groups())
        if not name or not description:
            raise ValueError(f"Empty project field at README.md line {number}")
        repository = REPOSITORY.fullmatch(url)
        if not repository:
            raise ValueError(
                f"Expected a GitHub repository URL at README.md line {number}: {url}"
            )
        owner, repo = repository.groups()
        identity = (owner.casefold(), repo.casefold())
        if identity in repositories:
            raise ValueError(f"Duplicate repository at README.md line {number}: {url}")
        repositories.add(identity)
        entries.append({
            "name": name,
            "description": INLINE_LINK.sub(r"\1 (\2)", description),
            "url": url,
            "author": owner,
        })

    if not entries:
        raise ValueError("No projects found in README.md")
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if showcase.yaml is missing or stale; do not write it.")
    args = parser.parse_args()
    try:
        entries = parse_readme((ROOT / "README.md").read_text(encoding="utf-8"))
        generated = HEADER + yaml.safe_dump(entries, sort_keys=False, allow_unicode=True, width=1000)
        output = ROOT / "showcase.yaml"
        if args.check:
            if not output.exists() or output.read_text(encoding="utf-8") != generated:
                print("showcase.yaml is missing or stale. Run: uv run scripts/generate_showcase.py", file=sys.stderr)
                return 1
            print(f"showcase.yaml is up to date ({len(entries)} projects).")
        else:
            output.write_text(generated, encoding="utf-8")
            print(f"Generated showcase.yaml ({len(entries)} projects).")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
