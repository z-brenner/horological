# Intake and the Collection Log

This file covers two linked features:

1. Intake: a short, adaptive interview that learns who the user is as a watch person: what they own, what they like, what they want, and how experienced they are.
2. The collection log: a running record of watches owned, wanted, sold, traded and serviced, kept in a local file the user controls, so later answers can use it.

## Contents
1. When to run intake
2. How to ask: tappable questions first
3. Round 1: the core questions
4. Adapting to experience level
5. Round 2: the collection itself
6. Round 3: taste and goals
7. Saving the results
8. Where the log lives, by environment
9. Keeping the log current
10. Using the profile in answers
11. Privacy and safety
12. Command reference

## 1. When to run intake

Run intake when:
- The user asks for it: "set up my profile," "log my collection," "get to know my watches."
- The user asks for personalized help, such as "what should I buy next," "what's missing from my collection," or "what would suit me," and no collection file or profile exists yet.
- The user mentions watches they own and has no log yet. Offer intake in one line; do not force it.

Do not run intake when:
- The question is general knowledge, such as how a tourbillon works.
- The user declines or wants a quick answer. Answer first, then offer intake once.

At the start of any personalized conversation, check for an existing log with `python3 scripts/collection.py summary`. If it exists, use it and do not repeat questions it already answers.

## 2. How to ask: tappable questions first

Intake should feel like a quick form, not an interrogation.

- If the environment has a tool for tappable multiple-choice questions, such as `AskUserQuestion` in Claude Code or a question widget in the Claude apps, use it. Ask up to four questions per round with short options. Users can always type their own answer.
- If the environment can render an interactive widget or artifact, a single intake form with chips, checkboxes and short text fields is a good alternative for the collection round. Have it submit back into the chat.
- If neither exists, ask in plain text, in short numbered rounds of three to four questions, and accept loose answers like "a Seiko diver and an old Omega."
- Never ask more than three rounds before giving the user something useful back, such as a summary of their collection and one observation.
- Let the user skip anything. Treat "skip" as an answer.

## 3. Round 1: the core questions

Ask these first. They decide everything else.

1. Experience. "How would you describe yourself with watches?"
   - Just curious
   - New to it, own one or two
   - Enthusiast, I read and buy regularly
   - Serious collector
   - Watchmaker or industry professional
2. Collection size. "Roughly how many watches do you have?"
   - None yet
   - One to three
   - Four to ten
   - More than ten
3. What draws you in. Multi-select. "What kinds of watches do you like?"
   - Dive and sports
   - Dress and classic
   - Field, pilot and military
   - Chronographs and racing
   - GMT and travel
   - Vintage
   - Independent and high horology
   - Japanese, German, or other regional makers
   - Smartwatches and digital
4. What brings you here today. "What would help most?"
   - Logging what I have
   - Finding my next watch
   - Learning more
   - Help with a specific watch

Map experience answers to the stored levels: curious, beginner, enthusiast, collector, expert, watchmaker.

## 4. Adapting to experience level

Adjust vocabulary, depth and which follow-up questions to ask.

| Level | Ask about | Avoid | Tone |
|---|---|---|---|
| Curious or beginner | Brand and model, what they wear it for, what they like about it, rough budget | Reference numbers, calibers, condition grading | Plain language, define terms the first time, suggest how to find model names on the caseback or papers |
| Enthusiast | Model and reference if known, movement type, size, how they bought it, what they would change | Deep provenance questions | Normal horology vocabulary |
| Collector or expert | Reference, year, caliber, condition, box and papers, service history, provenance, purchase source and price if they want to track value | Explaining basics | Peer-level, terse, precise |
| Watchmaker | Calibers, modifications, service records, tools and work in progress | Explaining basics | Technical |

Other adaptive rules:
- If they own nothing, skip Round 2 and go to taste and goals.
- If they own more than ten, ask them to list the watches in one message or paste a list, then confirm the parsed entries in a table rather than asking one by one.
- If they mention vintage, ask about service history and originality.
- If they mention smartwatches only, ask whether they are curious about mechanical watches before going deeper.
- If an answer reveals a different level than they chose, adapt quietly.

## 5. Round 2: the collection itself

For each watch, collect what the user knows. Never pressure for details.

Minimum: brand, model, status.
Useful: reference, year, caliber or movement type, size, style, condition, box and papers, where and when acquired, price paid, last service, and what they like or dislike about it.
Optional: serial number. Ask only if the user wants an insurance-style record, and say it stays in the local file only.

Ask for wanted watches as well:
- "Anything you're hunting for, or eyeing?" Status wishlist or considering, with a rough target price and priority.

Ask for past watches:
- "Any watches you've sold, traded or given away that you want in the history?" These matter for taste: why someone sold a watch is often more revealing than why they bought it.

After the round, show a compact table of what you captured and ask for corrections before saving.

## 6. Round 3: taste and goals

Ask only what the earlier rounds did not answer:
- Wrist size, or a watch that fits them well, to infer comfortable lug-to-lug.
- Budget range for the next purchase.
- Daily wear versus occasions, and lifestyle factors like swimming or travel.
- Dislikes: sizes, materials, brands, or features they avoid.
- Goals: build a three-watch collection, find a grail, learn to service, collect a theme.

## 7. Saving the results

Confirm with the user before saving. Then write the data with `scripts/collection.py`:

```bash
python3 scripts/collection.py init
python3 scripts/collection.py profile --set experience=enthusiast --set "styles=diver,field,GMT" --set "budget=USD 1,000 to 3,000" --set wrist_mm=170
python3 scripts/collection.py add --brand Seiko --model "SKX007" --reference SKX007 --caliber 7S26 --movement-type automatic --style diver --year 2015 --source "grey dealer"
python3 scripts/collection.py add --status wishlist --brand Tudor --model "Black Bay 58" --price 4000 --priority high
python3 scripts/collection.py add --status sold --brand Hamilton --model "Khaki Field" --notes "sold, too small"
```

Then run `summary` and give the user a short readout: what they own, the pattern you see, gaps relative to their goals, and one suggestion. Offer the Markdown export if they want a copy.

## 8. Where the log lives, by environment

The log is a single JSON file. Its location is `--file`, else `$HOROLOGICAL_HOME/collection.json`, else `~/.horological/collection.json`. It is separate from the skill folder, so updating or reinstalling the skill never erases it.

Persistence depends on where the skill runs. Be honest with the user about which case applies.

| Environment | What persists | What to do |
|---|---|---|
| Claude Code or any agent with a real local filesystem | The file persists on the user's machine between sessions | Use the default location. This is the best case. |
| Claude apps with a sandboxed code environment | The sandbox may be reset between conversations, so the file may not survive | Save the file during the session, then send it to the user, or export Markdown or JSON, and ask them to re-attach it next time. If the conversation can reach the user's computer through a file bridge, write it to a folder they choose. If the app has a memory feature, offer to save a short summary there with their permission. |
| Claude API with code execution | Depends on the integrator | Use `--file` with a path the integrator persists, or pass exported JSON back in. |
| No code execution | Nothing is written by the script | Keep the collection in the conversation, produce a Markdown or JSON block the user can save, and import it next time. |

When a user re-attaches an exported JSON, run `python3 scripts/collection.py import <file>`.

## 9. Keeping the log current

Update the log when the user says so in passing, after a quick confirmation:
- "I just picked up a Speedmaster": add as owned, or acquire it if it was on the wishlist.
- "I sold my Explorer": dispose with how=sold, and ask the price and reason only if they track them.
- "Got my Seamaster serviced": record a service.
- "I want a Grand Seiko eventually": add to wishlist.

Do not nag. A gentle check-in is fine when it helps, such as noting a mechanical watch with no service record in seven or more years. Never invent entries.

## 10. Using the profile in answers

Use the log when it changes the answer:
- Buying advice: avoid duplicating what they own, respect stated dislikes and wrist size, and stay inside the budget unless asked.
- Collection gaps: compare styles, movement types and use cases owned against their goals.
- Servicing: flag watches due for service when they ask about care.
- Explanations: pitch depth to their level, and use their own watches as examples, such as explaining a caller GMT using the GMT they own.
- Valuation: if asked, search current prices for their references and compare with what they paid. Mark these as estimates.

Do not bring up the collection on unrelated general questions.

## 11. Privacy and safety

- The log stays local. The skill never sends it anywhere.
- Purchase prices, totals and serial numbers are sensitive. Collect them only if the user wants them recorded, store them only in the local file, and leave serials out of exports unless asked with `--include-serials`. `show` hides serials unless `--reveal-serial` is passed.
- Advise against posting full serial numbers publicly, since they can be used to clone papers for counterfeits.
- If the user's environment has a separate memory feature, never copy prices or serials into it; at most a high-level summary, and only with permission.
- The user can delete everything by deleting the file. Tell them where it is with `python3 scripts/collection.py path`.

## 12. Command reference

| Command | Purpose |
|---|---|
| `path` | Show where the file lives |
| `init` | Create the file |
| `profile --set key=value` | Set experience, styles, interests, budget, wrist_mm, goals, dislikes, preferred_sizes, notes, name |
| `add` | Add a watch with any status: owned, wishlist, considering, sold, traded, gifted, lost |
| `update <id>` | Change fields or status |
| `acquire <id>` | Move a wishlist watch to owned |
| `dispose <id> --how sold` | Record a sale, trade, gift or loss |
| `service <id>` | Record a service |
| `note <id> "text"` | Add a dated journal note |
| `list --status owned` | List watches |
| `show <id>` | One watch with full history |
| `log` | Chronological event log |
| `summary` | Counts, brands, styles, spend, wishlist, service flags |
| `export --format md` | Markdown or JSON export |
| `import <file>` | Merge an exported JSON file |
