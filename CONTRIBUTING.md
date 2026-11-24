# Contributing

Corrections and additions are welcome. Accuracy is the whole point of this skill, so contributions are held to a sourcing standard.

## Ground rules

1. Every new or changed fact needs a source in the pull request description. Prefer primary sources: patents, brand archives, original catalogs, official standards, legal texts, and auction catalogs. Specialist books and long-running reference sites are acceptable. Forum posts are acceptable for practical ownership knowledge, not for history or specifications.
2. Mark uncertainty. If a claim is commonly stated but unproven, say "commonly stated." If credible sources disagree, present both.
3. Do not add current prices to reference files. Prices go stale immediately; the skill searches for them. Historical auction records with dates are fine.
4. Date volatile facts. Ownership changes, discontinuations and tariffs should carry a month and year.
5. Keep `SKILL.md` lean. Detailed knowledge belongs in `references/`. Add a routing row to `SKILL.md` for any new reference file.

## Style

- Plain, direct prose. No em dashes or en dashes; the checker enforces this.
- Lead with the fact, then the explanation.
- Use units consistently: mm, vph, Hz, s/d, bar, gauss.
- Tables for comparisons and specs; prose for explanations.
- Cross-reference other files with backticked file names, such as `calibers.md`.

## Before opening a pull request

```bash
python3 -m unittest discover -s tests
python3 tools/check_skill.py
```

If you change behavior, add or update a case in `evals/evals.json`.

## Updating the snapshot

When doing a broad refresh, update `metadata.knowledge_snapshot` and `metadata.version` in the `SKILL.md` frontmatter and add an entry to `CHANGELOG.md`.

## Calculator changes

`horological/scripts/horocalc.py` must stay standard-library only. Add a unit test for every new command or formula.
