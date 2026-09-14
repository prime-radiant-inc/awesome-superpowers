"""Run with: uv run --with pytest --with pyyaml python -m pytest"""

from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from scripts.generate_showcase import parse_readme

README = """# Awesome Superpowers

## Contents

- [Applications](#applications)
- [Websites](#websites)

## Applications

- [LambChat](https://github.com/Yanyutin753/LambChat) - An open-source platform for AI agents.

## Websites

- [Voting Info](https://github.com/bobmonsour/votinginfo) - Voting information; [usvoting.info](https://usvoting.info/)

## Contributing

See [the guide](CONTRIBUTING.md).
"""


def test_projects_keep_readme_order_and_derive_owner_labels():
    assert parse_readme(README) == [
        {
            "name": "LambChat",
            "description": "An open-source platform for AI agents.",
            "url": "https://github.com/Yanyutin753/LambChat",
            "author": "Yanyutin753",
        },
        {
            "name": "Voting Info",
            "description": "Voting information; usvoting.info (https://usvoting.info/)",
            "url": "https://github.com/bobmonsour/votinginfo",
            "author": "bobmonsour",
        },
    ]


@pytest.mark.parametrize("entry", [
    "- [Broken](https://github.com/owner/repo)",
    "- [](https://github.com/owner/repo) - Description.",
    "- [Empty](https://github.com/owner/repo) -   ",
    "- [Wrong URL](javascript:alert) - Description.",
    "- [Website](https://example.com/project) - Description.",
    "- [Profile](https://github.com/owner) - Description.",
])
def test_bad_entries_fail_instead_of_disappearing(entry):
    with pytest.raises(ValueError, match="line 3"):
        parse_readme("## Applications\n\n" + entry + "\n")


def test_empty_catalog_fails_instead_of_hiding_the_showcase():
    with pytest.raises(ValueError, match="No projects"):
        parse_readme("## Contents\n\n- [Applications](#applications)\n")


def test_duplicate_repository_fails_even_with_different_case():
    readme = """## Applications
- [One](https://github.com/owner/repo) - First entry.
- [Two](https://github.com/Owner/Repo/) - Same repository.
"""
    with pytest.raises(ValueError, match="Duplicate"):
        parse_readme(readme)


def test_check_detects_missing_and_stale_yaml_without_rewriting_it(tmp_path):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    script = scripts / "generate_showcase.py"
    shutil.copyfile(Path(__file__).parent / "scripts/generate_showcase.py", script)
    readme = tmp_path / "README.md"
    readme.write_text(README, encoding="utf-8")
    output = tmp_path / "showcase.yaml"

    def run(*args):
        return subprocess.run(
            [sys.executable, str(script), *args], capture_output=True, text=True
        )

    assert run("--check").returncode == 1
    assert not output.exists()
    generated = run()
    assert generated.returncode == 0, generated.stderr
    data = yaml.safe_load(output.read_text(encoding="utf-8"))
    assert [entry["name"] for entry in data] == ["LambChat", "Voting Info"]
    assert run("--check").returncode == 0

    original = output.read_bytes()
    readme.write_text(README.replace("An open-source platform", "An updated platform"), encoding="utf-8")
    assert run("--check").returncode == 1
    assert output.read_bytes() == original
