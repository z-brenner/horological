# Horological

Horological is an Agent Skill that turns Claude into a skeptical, deeply informed horologist. Ask it anything about watches or clocks: how a co-axial escapement works, who really made the first automatic chronograph, whether a timegrapher reading means a service is due, how to date a Seiko from its serial, what "Swiss Made" legally guarantees, or what a vintage Speedmaster should cost. When it does not know, it says so and goes and finds out the right way.

## Why this skill is different

- Accuracy over confidence. Facts are tiered as stable, slow-moving or volatile. Prices, ownership, releases and tariffs are always searched before they are stated, and disputed claims are presented as disputed.
- Engineering over marketing. The skill translates terms like "in-house," "chronometer" and "anti-magnetic" into what they actually guarantee.
- Progressive disclosure. A short `SKILL.md` routes Claude to 19 focused reference files, so it loads only what a question needs.
- Real calculations. A tested, dependency-free calculator handles frequency conversions, rate tolerances, moonphase drift, water pressure, magnetic units, Seiko serial decoding, gold fineness and lignes.
- A research playbook. When the files run out, Claude follows a source map ranked by reliability: Ranfft, Caliber Corner, brand archives, patents, auction results, specialist forums, and more.
- Safety and money sense. It never authenticates from photos, warns about radium lume, and gives buying advice with failure modes instead of hype.
- Knows your collection. An adaptive intake learns what you own, want and have sold, and how experienced you are, using tappable questions where the app supports them. A local, append-only collection log keeps the history, so recommendations account for what is already in your watch box.
- Testable. A set of behavioral eval cases and repository checks ship with the skill.

## Coverage

| Area | File |
|---|---|
| History from water clocks to 2026, national industries, disputed firsts | `history.md` |
| Mechanical movements, escapements, oscillators, winding, lubrication, finishing | `movements.md` |
| Chronographs, GMTs, calendars, moonphases, repeaters, tourbillons | `complications.md` |
| Rate, timegrapher interpretation, COSC, METAS and brand standards | `accuracy-and-timing.md` |
| Quartz, Accutron, Spring Drive, solar, radio and GPS sync, smartwatches | `electronic.md` |
| Cases, materials, crystals, dials, hands, lume, water resistance, bracelets | `cases-and-materials.md` |
| Swiss Made, Glashütte rule, Geneva Seal, ISO standards, hallmarks | `standards.md` |
| Groups, brands, suppliers, distribution, industry data, tariffs | `industry.md` |
| Caliber specifications, lineages, rebadges and clones | `calibers.md` |
| Iconic models and reference numbers | `references-and-models.md` |
| Buying, prices, auctions, value drivers, scams | `collecting-and-market.md` |
| Serial decoding and dating by brand | `identification-and-dating.md` |
| Fakes, frankens, redials, superclones, verification | `authentication.md` |
| Service, care and troubleshooting by symptom | `servicing-and-care.md` |
| Clocks, pendulums, marine chronometers, atomic time | `clocks.md` |
| Myths, glossary and research methods | `myths.md`, `glossary.md`, `research-playbook.md` |
| Intake, collector profile and collection log | `intake-and-collection.md` |

## Installation

The skill lives in the `horological/` folder. Its entry point is `horological/SKILL.md`.

### Claude apps
1. Download `horological.zip` from the latest release or CI run, or build it with `zip -r horological.zip horological`. The zip contains the `horological/` folder with `SKILL.md` inside it.
2. In Claude, open the skills section of settings and upload the zip.
3. Make sure code execution is enabled if you want the calculator to run.

### Claude Code
Copy the folder into your personal or project skills directory:

```bash
# Personal, available in every project
cp -r horological ~/.claude/skills/horological

# Or per project
mkdir -p .claude/skills && cp -r horological .claude/skills/horological
```

### Claude API
Upload the folder as a custom skill through the Skills API and attach it to requests that use code execution. See Anthropic's Agent Skills documentation for the current endpoints.

## Intake and the collection log

Ask Claude something personal, such as "what should I buy next?" or "log my collection," and the skill runs a short intake: experience level, roughly how many watches you have, the styles you like, and what you want help with. Follow-up questions adapt to the answers. A beginner gets plain-language questions about brand and model; a serious collector gets asked about references, calibers, condition, papers and service history.

Everything is saved by `horological/scripts/collection.py` to a single JSON file outside the skill folder:

- `$HOROLOGICAL_HOME/collection.json` if that variable is set, otherwise `~/.horological/collection.json`.
- Every change is recorded in an event log: acquisitions, sales, trades, gifts, services and notes.
- Serial numbers and prices are optional, stay in the local file, and are left out of exports unless you ask for them.

Persistence depends on the environment. In Claude Code the file lives on your machine and persists. In the Claude apps the code sandbox may reset between conversations, so the skill offers a Markdown or JSON export you can keep and re-attach, which it imports with `collection.py import`.

```bash
python3 horological/scripts/collection.py init
python3 horological/scripts/collection.py profile --set experience=enthusiast --set "styles=diver,GMT"
python3 horological/scripts/collection.py add --brand Seiko --model SKX007 --caliber 7S26 --style diver
python3 horological/scripts/collection.py add --status wishlist --brand Tudor --model "Black Bay 58" --priority high
python3 horological/scripts/collection.py dispose seiko-skx007 --how sold --reason upgraded
python3 horological/scripts/collection.py summary
python3 horological/scripts/collection.py export --format md --out my-collection.md
```

## Using the calculator directly

```bash
python3 horological/scripts/horocalc.py freq --vph 28800 --escape-teeth 15
python3 horological/scripts/horocalc.py rate --gain 52 --days 7 --standard all
python3 horological/scripts/horocalc.py moonphase --teeth 59
python3 horological/scripts/horocalc.py water --m 200
python3 horological/scripts/horocalc.py magnet --am 4800
python3 horological/scripts/horocalc.py seiko-serial 7N1234 --from-year 1976 --to-year 1988
python3 horological/scripts/horocalc.py gold --karat 18 --grams 12
python3 horological/scripts/horocalc.py ligne --lignes 11.5
```

Add `--json` before the command for machine-readable output.

## Example prompts

- "Explain the difference between a column-wheel and cam-actuated chronograph, and whether I'd feel it."
- "My Grand Seiko reads +2, 285 degrees and 0.2 ms dial up but -9 crown down. Normal?"
- "What should I check before buying a 1970s Rolex 1675 from a forum seller?"
- "Is a 135-tooth moonphase really accurate for 122 years? Show the math."
- "Why did the Swiss watch industry nearly collapse in the 1970s?"
- "What's actually inside a Breitling B17?"

## Repository layout

```
horological/                 The skill itself
  SKILL.md                Entry point, operating rules and routing
  references/             Knowledge base, one file per domain
  scripts/horocalc.py     Calculator, standard library only
  scripts/collection.py   Local collection log and collector profile
evals/evals.json          Behavioral test prompts with pass criteria
tests/                    Unit tests for the calculator
tools/check_skill.py      Link, frontmatter, style and eval checks
```

## Development

```bash
python3 -m unittest discover -s tests
python3 tools/check_skill.py
```

Both run in CI on every push and pull request.

## Keeping it current

The knowledge snapshot date is in the `SKILL.md` frontmatter. The skill instructs Claude to search for anything volatile, so it stays useful as facts age, but the reference files should be refreshed periodically. Ownership changes, new calibers, standards revisions and auction records are the most common updates. See `CONTRIBUTING.md`.

## Disclaimer

This project is independent and is not affiliated with, endorsed by, or sponsored by any watch brand, group, retailer, auction house or standards body. Brand names, model names and trademarks belong to their owners and are used only for identification. Information is provided for education and is not financial, legal or appraisal advice. Authenticity and value can only be confirmed by physical inspection.

## License

MIT. See `LICENSE`.
