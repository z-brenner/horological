# Accuracy, Rate and Timing

Use this file for anything about how accurate a watch is or should be, how to measure it, how to read a timegrapher, and what certifications promise.

## Contents
1. Vocabulary
2. What disturbs a mechanical watch
3. Realistic accuracy expectations
4. Measuring at home
5. Reading a timegrapher
6. Positional regulation tricks
7. Chronometer and accuracy standards
8. Quartz and electronic accuracy

## 1. Vocabulary

- Rate: gain or loss over 24 hours, in seconds per day, written s/d. Plus means fast.
- Mean rate: average over several days or positions.
- Delta or positional variation: the spread between the fastest and slowest positions. A small delta matters more than a perfect average, because the average can be adjusted.
- Isochronism: whether the rate stays the same as amplitude falls through the power reserve.
- Amplitude: how far the balance swings from rest, in degrees.
- Beat error: asymmetry between the two halves of the balance's swing, in milliseconds.
- Positions, by convention:
  - DU dial up, DD dial down: the horizontal or flat positions.
  - CU crown up, CD crown down, CL crown left, CR crown right: the vertical or hanging positions. 6H, 3H, 9H and 12H labeling is also used, naming the dial position that points up.
  - "Adjusted to five positions" usually means DU, DD and three of the vertical positions.

## 2. What disturbs a mechanical watch

- Gravity and position: in vertical positions, a slightly out-of-poise balance runs fast or slow depending on where its heavy spot is. In flat positions, pivot friction on the end stone differs from vertical positions.
- Amplitude and isochronism: rate changes as the mainspring runs down. Most watches drift in the last part of the reserve.
- Temperature: modern alloys are self-compensating, but not perfectly.
- Magnetism: a magnetized hairspring sticks to itself, effectively shortening it, and the watch suddenly runs fast, often by minutes per day. The single most common cause of a sudden large gain.
- Shock: can shift the hairspring, regulator or beat.
- Lubrication: aging oil raises friction, drops amplitude, and worsens positional error.
- Wearing habits: how many hours worn, how active, and how the watch rests overnight all change the daily result. The same watch can measure differently on two owners.

## 3. Realistic accuracy expectations

Manufacturer tolerances, commonly stated. Verify for a specific caliber.

| Category | Typical spec or expectation |
|---|---|
| Entry Japanese automatic, Seiko 4R35 | about minus 35 to plus 45 s/d spec; usually much better in practice |
| Seiko NH35 and Miyota 8215 | about minus 20 to plus 40 s/d spec |
| ETA 2824-2 Standard grade | about plus or minus 12 s/d average, wider maximum |
| ETA Elaboré grade | about plus or minus 7 s/d average |
| ETA Top grade | about plus or minus 4 s/d average |
| COSC chronometer | minus 4 to plus 6 s/d mean, uncased movement |
| METAS Master Chronometer | 0 to plus 5 s/d, cased watch |
| Rolex Superlative Chronometer | minus 2 to plus 2 s/d, cased watch |
| Grand Seiko Special Standard mechanical | minus 3 to plus 5 s/d static |
| Grand Seiko Spring Drive | plus or minus 15 s per month, about plus or minus 0.5 s/d; some calibers plus or minus 10 s per month; Spring Drive U.F.A. calibers plus or minus 20 s per year |
| Standard quartz | about plus or minus 15 s per month |
| Thermocompensated high-accuracy quartz | about plus or minus 5 to 10 s per year |

Rules of thumb:
- A healthy, recently serviced mechanical watch within about plus or minus 10 s/d in wear is normal. Within plus or minus 5 s/d is good.
- A sudden change of more than about 30 s/d points to magnetism, shock, or a fault, not normal drift.
- Watches are usually regulated to run slightly fast, because owners prefer gaining to losing.

## 4. Measuring at home

1. Fully wind the watch, or wear it for a day.
2. Synchronize to a reference, such as time.gov, an atomic-time app, or a phone's network time. Hacking makes this easy.
3. Note the offset at the same time each day for five to seven days, wearing it normally.
4. Compute the average daily rate. Use `horocalc.py rate --gain <seconds> --days <days>`.
5. To test positions, leave the watch in one position overnight and record the change. Repeat for other positions.

Apps such as WatchCheck and Toolwatch automate the logging. Phone-microphone timegrapher apps can give rough rate and beat error but are unreliable for amplitude.

## 5. Reading a timegrapher

A timegrapher listens to the ticks and plots each beat. Settings must match the watch:

- Beat rate: usually auto-detected; confirm it matches the caliber's vph.
- Lift angle: the angle through which the balance is in contact with the lever. Amplitude is calculated from it, so a wrong lift angle gives a wrong amplitude. 52 degrees is the common default for Swiss levers. Some calibers differ, notably Omega co-axials at 38 degrees and some Seiko movements around 53 degrees. Check the caliber's technical sheet.

The three headline numbers:

| Reading | Good | Concerning |
|---|---|---|
| Rate | within plus or minus 10 s/d in each position for an average watch | large rate differences between positions |
| Amplitude, dial up, full wind | about 270 to 310 degrees for most modern movements; older and low-beat watches lower | below about 220 dial up, or below about 200 in vertical positions, often means service is due |
| Beat error | under about 0.5 ms | over about 1.0 ms deserves adjustment |

Amplitude notes:
- Vertical amplitudes are normally 20 to 50 degrees lower than horizontal.
- Readings over about 320 degrees can indicate risk of rebanking, where the impulse jewel strikes the back of the fork; it appears as a sudden large gain. Some movements are designed for high amplitude, so context matters.
- Measure at full wind and again after 24 hours to see how the watch handles reserve decline.

Trace patterns:
- Two straight parallel lines close together: healthy, small beat error.
- Two lines diverging apart: beat error.
- Lines sloping up: running fast. Sloping down: slow.
- Wavy, periodic patterns: often an eccentric or damaged wheel in the train; the wave period tells the watchmaker which wheel.
- Scattered or noisy points: dirty, worn or damaged escapement, or a loose part.
- Sudden jumps: possibly a magnetized or touching hairspring.

## 6. Positional regulation tricks

Owners can use positional rates to fine-tune daily results without opening the watch:

- Log the rate in each position overnight.
- If the watch runs fast in wear, leave it overnight in the position where it runs slowest, and vice versa.
- Example: a watch gaining 4 s/d on the wrist that loses 3 s/d crown up can be rested crown up at night to land near zero.

This is a workaround, not a repair. If deltas are large, the watch needs regulation or service.

## 7. Chronometer and accuracy standards

### COSC, Contrôle Officiel Suisse des Chronomètres
- Governed by ISO 3159.
- Tests the uncased movement over 15 days in five positions and at three temperatures, about 8, 23 and 38 degrees Celsius.
- Main criteria, commonly cited for movements over 20 mm:
  - Average daily rate: minus 4 to plus 6 s/d.
  - Mean variation in rates: 2 s.
  - Greatest variation in rates: 5 s.
  - Difference between flat and hanging: minus 6 to plus 8 s.
  - Largest variation in rates across positions: 10 s.
  - Thermal variation: about plus or minus 0.6 s per degree Celsius.
  - Rate resumption after the test: plus or minus 5 s.
- COSC also certifies quartz chronometers at a much tighter level, about plus or minus 0.07 s/d.
- Important: COSC tests the movement before casing. Casing, the dial and hands, and subsequent handling can change performance.
- "Chronometer" in Switzerland legally requires certification by an official body. Many non-Swiss brands use the word loosely.

### METAS Master Chronometer
- Introduced in 2015 by Omega with the Swiss Federal Institute of Metrology. Also used by Tudor on some models.
- Tests the cased, finished watch after COSC certification.
- Criteria include 0 to plus 5 s/d, resistance to 15,000 gauss, water resistance, power reserve, and performance across positions and two temperatures.

### Rolex Superlative Chronometer
- After COSC, Rolex tests the cased watch in-house. Since 2015 the specification is minus 2 to plus 2 s/d.

### Other brand standards
- Patek Philippe Seal: commonly stated as minus 3 to plus 2 s/d for movements of 20 mm and above, plus finishing and serviceability rules.
- Grand Seiko Special Standard: minus 3 to plus 5 s/d static mechanical, tested over 17 days in six positions and three temperatures.
- Chopard Chronométrie Ferdinand Berthoud and similar brand certifications vary; read the spec.
- Fleurier Quality Foundation: includes a Chronofiable reliability test and a simulated-wear rate test. See `standards.md`.

### Historical observatory trials
- Neuchâtel, Geneva, Kew and Besançon observatories ran precision competitions from the 19th century to the late 1960s. Specially adjusted "observatory chronometers" competed there.
- Swiss quartz prototypes topped the 1967 Neuchâtel trials, and Seiko entered mechanical and quartz pieces in the late 1960s. The competitions ended soon after.

## 8. Quartz and electronic accuracy

- Standard quartz: about plus or minus 15 s per month, mainly because crystal frequency varies with temperature.
- Thermocompensated quartz measures temperature and corrects the count: Breitling SuperQuartz, Citizen Caliber 0100 at plus or minus 1 s per year, Grand Seiko 9F at plus or minus 10 s per year, Longines VHP and Seiko 8F.
- High-frequency quartz: Bulova Precisionist at 262 kHz. A higher frequency alone does not guarantee better long-term stability.
- Radio-controlled and GPS-synced watches are as accurate as their last sync. Signal coverage matters. See `electronic.md`.
- Spring Drive sits between: a mechanical power train regulated against a quartz reference.
