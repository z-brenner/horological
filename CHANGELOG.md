# Changelog

## 2.2.0, November 2026

- New reference: `brands.md`, a directory of more than 100 brands by country and tier with founding, specialties, ownership and collector shorthand.
- New reference: `workbench.md`, covering fit, straps, spring bars, bracelet sizing, modding, parts compatibility, building a watch, learning watchmaking, tools and legal notes.
- Calculator: added `tachy`, `telemeter`, `pendulum` and `fit`.
- Collection log: added optional wear tracking with `wear` and `rotation`, including days since worn and cost per wear.
- Installable as a Claude Code plugin through the repository's plugin marketplace file.
- Repository: new README with banner, badges, quick install and FAQ; issue and pull request templates; code of conduct; security policy; release workflow that attaches the skill zip to tagged releases.

## 2.1.0, November 2026

- Added an adaptive intake that learns the user's experience level, collection, tastes and goals, using tappable multiple-choice questions where supported.
- Added `collection.py`, a local, append-only collection log with a collector profile, wishlist, sales, trades, services, journal notes, summaries, and Markdown or JSON export and import. Serials and prices are optional and excluded from exports by default.
- Added `references/intake-and-collection.md` with the question bank, adaptation rules, storage behavior by environment, and privacy rules.
- Added unit tests and eval cases for intake and the log.

## 2.0.1, November 2026

- Renamed the skill and repository to Horological. The skill folder and frontmatter name are now `horological`.

## 2.0.0, November 2026

- Rebuilt as a multi-file skill: a lean `SKILL.md` with operating rules, routing and answer workflows, plus 18 reference files.
- New coverage: clocks and atomic time, electronic and quartz watches, authentication, identification and dating by brand, iconic references, caliber specifications and rebadges, industry structure, standards and hallmarks, servicing by symptom, myths, glossary, and a research playbook.
- Facts refreshed through the November 2026 snapshot, including the Glashütte regulation, Baume & Mercier's sale to Damiani, Breitling's House of Brands, the Rolex Land-Dweller and caliber 7135, 2025 and 2026 auction records, and US tariff changes.
- Added `horocalc.py`, a tested calculator for frequency, rate tolerances, moonphase drift, power reserve, beats, water resistance, magnetism, Seiko serials, gold fineness and lignes.
- Added behavioral evals, unit tests, a repository checker and CI.

## 1.0.0, November 2026

- Initial single-file skill.
