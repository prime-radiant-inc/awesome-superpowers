# Contributing

Awesome Superpowers showcases community projects built using Superpowers, not Superpowers skills.

## Project eligibility

Submit a public project with a canonical project URL, sufficient public documentation, and a fit with one of the README categories. The existing candidate-identification process determines whether Superpowers use qualifies; contributors do not need to add evidence links to the README entry.

Choose exactly one primary form for each project:

- Applications
- Plugins & Extensions
- CLI & Developer Tools
- Integrations
- Websites
- Templates & Starter Kits
- Demos & Examples

Secondary capabilities belong in the description, not a second listing.

## Entry format and placement

Write each entry with the project name in brackets, its real canonical URL in parentheses, a dash, and an objective description. Describe the project itself, not this list or Superpowers. Start the description with an uppercase character and end it with a period.

Add new entries at the bottom of the appropriate category. Do not add duplicate entries.

## Quality and maintenance

Do not submit archived, abandoned, deprecated, undocumented, duplicate, or otherwise non-awesome projects. Maintainers may update a moved canonical link and should remove an entry when it is no longer valid or maintained.

## Website showcase

The [Prime Radiant Superpowers page](https://primeradiant.com/superpowers/) uses
`showcase.yaml` from this repository. The README is the editable source for all
projects; the YAML file is generated from it and committed alongside README
changes. Do not edit the YAML directly.

Use one entry per line under a category heading. Use the project's GitHub
repository URL as the entry link so the generator can derive the GitHub owner
label. Additional website links can go in the description. The generator
preserves category and entry order, and turns inline Markdown links in
descriptions into plain text with their URLs for the website cards.

Each generated entry has four required fields:

```yaml
- name: LambChat
  description: An open-source platform for building, running, and sharing AI agents.
  url: https://github.com/Yanyutin753/LambChat
  author: Yanyutin753
```

`author` is the GitHub account or organization that owns the repository, not
necessarily an individual author. Every project in the README is included.

After adding, changing, reordering, or removing a README entry, regenerate the
feed with [uv](https://docs.astral.sh/uv/):

```bash
uv run scripts/generate_showcase.py
```

Include both `README.md` and `showcase.yaml` in the same pull request. CI rejects
missing or stale YAML, malformed entries, and duplicate repository URLs.

After the website enables the showcase, it fetches the feed from this repo's
default branch on each build. Merged updates are picked up by its daily build
at 13:47 UTC, or by manually running **Deploy Blog** in
[the website repository](https://github.com/prime-radiant-inc/prime-radiant-inc.github.io/actions/workflows/deploy.yml).
Invalid or unavailable feed data fails the website build, so keep generation
and validation passing before merging.

## Validation

Run these checks locally and fix any findings before submitting:

```bash
npx awesome-lint
uv run --with pytest --with pyyaml python -m pytest
uv run scripts/generate_showcase.py --check
```

Also manually check the project's relevance, primary form, duplicate status, documentation, and active status.
