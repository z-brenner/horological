# Changelog

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
