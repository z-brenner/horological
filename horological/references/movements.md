# Mechanical Movements

Use this file to explain how a mechanical watch works, from the mainspring to the hands, and the engineering choices that separate one movement from another.

## Contents
1. The energy path
2. Power: mainspring and barrel
3. Going train and gear ratios
4. Escapements
5. The oscillator: balance and hairspring
6. Regulation systems
7. Winding: keyless works and automatic systems
8. Motion works, setting and date mechanisms
9. Jewels, bearings and shock protection
10. Lubrication
11. Movement architecture and vocabulary
12. Finishing and decoration
13. What makes a movement "good"

## 1. The energy path

Every mechanical watch does the same five things:

1. Store energy in a coiled mainspring inside a barrel.
2. Transmit it through a gear train that multiplies speed.
3. Release it in small, equal steps through the escapement.
4. Govern those steps with an oscillator, the balance wheel and hairspring, which is the actual timekeeper.
5. Display time through the motion works and hands.

A useful mental model: the mainspring is the battery, the gear train the transmission, the escapement the gatekeeper, and the balance the metronome. The escapement does two jobs at once: it lets the train advance one tooth per beat, and it gives the balance a small push each swing to keep it going.

## 2. Power: mainspring and barrel

- The mainspring is a long ribbon of alloy coiled in the barrel. Modern alloys such as Nivaflex resist fatigue and do not "set" the way old carbon-steel springs did.
- The barrel's teeth drive the center wheel. The inner end hooks to the arbor, which is wound; the outer end hooks to the barrel wall.
- Hand-wound movements need a stop to prevent overwinding. Automatic movements use a slipping bridle, a friction end on the outer coil that slips at full wind, so they cannot be overwound.
- Torque falls as the spring unwinds. That changes the balance amplitude and therefore, slightly, the rate. Solutions include long springs used only in their flat middle torque range, multiple barrels in series or parallel, a fusee and chain, and constant-force or remontoir mechanisms.
- Power reserve is set by spring length and thickness, the barrel's gear ratio to the train, and how much energy the oscillator consumes. Higher frequency and bigger balances consume more.
- Modern long-reserve strategies: thinner, longer springs in larger barrels; lower-friction escapements; lighter silicon parts; lower frequency. Examples include Powermatic 80 at 80 hours and 21,600 vph, and Rolex 3235 at about 70 hours.

## 3. Going train and gear ratios

Typical layout in a three-hand watch:

- Barrel drives the center wheel, which turns once per hour and usually carries the cannon pinion for the minute hand.
- Center wheel drives the third wheel.
- Third wheel drives the fourth wheel, which turns once per minute and carries the seconds hand in a small-seconds or indirect central seconds layout.
- Fourth wheel drives the escape wheel pinion.

Worked example, a 28,800 vph movement with a 15-tooth escape wheel, the Swiss lever standard: 28,800 vibrations per hour is 14,400 full oscillations per hour. Each oscillation releases one tooth, so the escape wheel turns 14,400 divided by 15, which is 960 times per hour, or 16 times per minute. The fourth wheel turns once per minute, so the fourth wheel to escape pinion ratio must be 16 to 1. The same logic sizes any train. Use `horocalc.py freq` for frequency conversions.

Seconds layouts:
- Small seconds: the fourth wheel arbor carries the hand directly. Simple and efficient.
- Direct central seconds: the fourth wheel sits at the center of the movement.
- Indirect central seconds: an extra wheel drives a central seconds pinion, often with a friction spring to stop hand flutter. Common in older movements.

## 4. Escapements

| Escapement | Era and use | Character |
|---|---|---|
| Verge with foliot or balance | 13th to 19th century | Recoil, poor accuracy, needs a fusee. |
| Cylinder | 18th to early 20th century | Frictional rest, thin, wears quickly. |
| Duplex | 18th and 19th century | Accurate when new, delicate. |
| Detent or chronometer | Marine chronometers | Very accurate and efficient; can trip or stop under shock, so unsuited to wristwatches. |
| English lever | 19th century English watches | Pointed teeth, ratchet-tooth escape wheel. |
| Swiss lever, club tooth | Standard since the late 19th century | Detached, robust, self-starting, tolerant of wear. |
| Pin pallet or Roskopf | Cheap watches, Timex, alarm clocks | Steel pins instead of jewels, durable, less accurate. |
| Co-axial | Omega since 1999, George Daniels design | Impulse delivered mostly radially by two wheels, cutting sliding friction and lubrication needs. |
| Silicon and other modern variants | 2000s onward | Ulysse Nardin Dual Direct, Grand Seiko dual impulse in the 9SA5, Rolex Chronergy in the 32 series, Rolex Dynapulse in the 7135, Zenith Defy Lab oscillator. |

How the Swiss lever works, in four steps:

1. Lock: an escape wheel tooth rests on the entry pallet stone, holding the train still. Draw, the angle of the locking faces, pulls the lever against its banking pin so a shock does not unlock it.
2. Unlock: the balance's impulse jewel, or roller jewel, swings into the lever's fork and pushes it, freeing the tooth.
3. Impulse: the tooth slides across the pallet's impulse face, pushing the lever, which pushes the balance through the roller jewel.
4. Drop and lock: the escape wheel jumps a small distance until the next tooth locks on the other pallet. The balance then swings freely, detached, until it returns. Each lock-unlock-impulse is one beat, and the tick is the sound of locking and drop.

Detachment is the key idea: for most of its swing the balance touches nothing, which is why the lever escapement is accurate.

## 5. The oscillator: balance and hairspring

- The period of the balance depends on its moment of inertia and the stiffness of the hairspring. Change either and the rate changes.
- Balance wheels: early steel or brass; bimetallic cut balances for temperature compensation in the 19th century; monometallic Glucydur, a beryllium bronze, once self-compensating hairsprings arrived.
- Hairspring alloys: Charles-Édouard Guillaume's Invar and Elinvar, which won him the 1920 Nobel Prize in Physics, led to self-compensating alloys like Nivarox, the industry standard. Silicon hairsprings, marketed under names like Silinvar, Spiromax and Syloxi, are non-magnetic, light, corrosion-proof and can be etched to precise shapes. Rolex Parachrom is a niobium-zirconium alloy, highly resistant to magnetism and shock.
- Hairspring shapes: flat; Breguet overcoil, where the outer coil is raised and curved inward so the spring breathes concentrically, improving isochronism and positional rate; terminal curves calculated by Phillips and Lossier; silicon springs with variable thickness that achieve similar effects in one plane.
- The hairspring attaches to the balance staff by the collet and to the balance cock by the stud.
- Amplitude is how far the balance swings. Healthy modern watches run roughly 270 to 310 degrees dial up at full wind. See `accuracy-and-timing.md`.

## 6. Regulation systems

- Index regulator: two curb pins straddle the hairspring near the stud. Moving the index changes the active length of the spring. Easy to adjust, but the pins can disturb isochronism.
- Fine adjustment indexes: swan-neck, Etachron, Triovis, eccentric screws. They make small adjustments easier.
- Free-sprung balances: no curb pins; rate is adjusted by inertia, using screws or weights on the balance rim. Examples: Rolex Microstella, Patek Gyromax, Omega in co-axial calibers. Free-sprung designs keep their regulation better under shock and over time.
- Beat adjustment: rotating the collet or a movable stud carrier centers the balance's rest position relative to the lever, reducing beat error.

## 7. Winding: keyless works and automatic systems

Keyless works:
- Winding stem, clutch or sliding pinion, winding pinion, crown wheel, ratchet wheel, and click.
- Pulling the crown moves the setting lever and yoke, shifting the clutch to the setting position.
- Positions on a typical date watch: position 0 winding; position 1 quickset date; position 2 time setting.
- Hacking: a lever touches the balance rim when the crown is pulled to set, stopping the seconds hand so it can be synchronized.

Automatic winding:
- Central rotor, either bidirectional through reversers or wheels, as in ETA 2824 and Rolex, or unidirectional as in Valjoux 7750.
- Seiko Magic Lever, 1959: a simple, efficient pawl lever that winds in both directions.
- IWC Pellaton system: cam and pawls, very efficient and robust.
- Micro-rotor: a small rotor set into the movement level for thinness, used in the Calibre 11, Patek 240 and many modern dress watches.
- Peripheral rotor: a ring around the movement edge, leaving the movement fully visible; Carl F. Bucherer, Parmigiani and Vacheron Constantin have used them.
- Bumper or hammer automatics, 1930s to 1950s: a weight swings through an arc between buffer springs. Harwood, Omega and Rolex-adjacent makers used them.
- Ball-bearing rotors are common; ceramic bearings appear in some modern movements.

Most automatics can be wound by hand through the crown. Some cannot, such as many Seiko 7S26 movements and the Calibre 11's early versions. Winding a typical automatic fully by hand takes roughly 30 to 50 crown turns; it varies by caliber.

## 8. Motion works, setting and date mechanisms

- The cannon pinion sits on the center wheel arbor with a friction fit, so the hands can be set without stopping the train.
- The minute wheel steps down to the hour wheel at 12 to 1.
- Date mechanisms:
  - Creeping or slow: the date drifts over hours around midnight.
  - Semi-instant: the date changes over a short period.
  - Instant: a spring is loaded and releases at midnight. Rolex calendars are a classic example.
- Quickset: the date is advanced directly at position 1. Some movements, such as many Seiko and ETA calibers, must not be quickset when the date wheel is engaged, roughly between 9 pm and 3 am; the exact window varies.
- Day and date displays use separate wheels; a day wheel may show two languages.

## 9. Jewels, bearings and shock protection

- Synthetic rubies, corundum, reduce friction and wear at pivots and at the pallet and impulse jewels.
- A simple time-only movement is fully jeweled at about 17 jewels. Automatic winding systems, chronographs and capstones add more. Jewel counts above about 30 often include functional jewels in winding systems, and some old watches added non-functional decorative jewels for marketing. Jewel count is not a quality measure.
- Jewel types: hole jewels; cap stones or end stones; pallet stones; impulse or roller jewel; chatons, gold settings pressed into the plate.
- Shock protection: the balance staff pivots are its weakest point. Spring-loaded jewel settings let the staff move under shock and return. Incabloc, from 1934, is the common lyre spring. Others include KIF, Seiko Diashock and Diafix, Rolex Paraflex, Omega Nivachoc, and Breguet's pare-chute of about 1790 as the historical precursor.

## 10. Lubrication

Modern watches use several specialized lubricants. Watchmakers commonly cite these from the Moebius range:

- Light oils such as 9010 for fast-moving pivots.
- Escapement oils such as 941 and 9415, the latter a grease-like oil for high-frequency pallets.
- Greases such as 8200 for hand-wound mainsprings and 9501 or 9504 for keyless works and high-pressure points.
- Braking greases such as 8217 for the barrel wall where an automatic mainspring's slipping bridle rides.
- Product numbers and recommendations differ by manufacturer service documents; the brand's technical guide wins.
- Epilame treatment: a surface coating that keeps oil from spreading.

Dried, migrated or contaminated oil is the main reason watches need service. Oils degrade, and the result is falling amplitude, rate drift and accelerated wear.

## 11. Movement architecture and vocabulary

- Main plate: the base plate. Bridges hold the wheels from above. A cock is a bridge supported at one end, such as the balance cock.
- Full plate: one top plate, common in old pocket watches.
- Three-quarter plate: one large bridge covering most of the train, a Glashütte signature.
- Lépine or bridge layout: separate bridges for each wheel or group, the modern Swiss norm.
- Caliber or calibre: a movement design, often identified by number.
- Ébauche: a raw movement kit, historically supplied by makers such as ETA, Valjoux, Peseux, Felsa, AS and Unitas to brands that finished it.
- Base caliber and module: a complication may be a stacked module on a base caliber, such as a Dubois-Dépraz chronograph module on an ETA 2892.
- Integrated: complication and base designed together, usually thinner and better engineered.
- Manufacture and in-house: no legal definition. Ask who designed it, who makes the parts, especially hairspring and escapement, and who assembles it.
- Ligne: the old French unit for movement diameter, 2.2558 mm. An 11.5 ligne movement is about 25.9 mm. Use `horocalc.py ligne`.

## 12. Finishing and decoration

| Technique | What it is | Tell for quality |
|---|---|---|
| Côtes de Genève, Geneva stripes | Parallel waves on bridges | Even, crisp, aligned across bridges. |
| Perlage, circular graining | Overlapping circles on plates | Even overlap, also inside recesses. |
| Anglage or beveling | Polished chamfered edges | Hand-done inward angles, which machines cannot cut. |
| Black or mirror polish | Flat polish that looks black off-angle | Perfectly flat, no ripples. |
| Frosting or grenaillage | Matte granular texture | Lange and many independents. |
| Sunburst or snailing | Radial or spiral patterns on wheels | Evenness. |
| Blued screws | Heated or chemically blued | Even color; heat bluing is traditional. |
| Hand engraving | Balance cocks and bridges | German and independent makers. |
| Gold chatons, screwed | Gold settings for jewels | Tradition, especially Lange. |

Decoration can be machine-made at any price. Hand finishing shows in inward angles, polished screw slots and countersinks, and finish in places no one sees.

## 13. What makes a movement "good"

A good movement balances:
- Robustness and serviceability: parts availability, use of standard parts, tolerance of wear. ETA, Sellita, Seiko and Miyota movements win here.
- Chronometric performance: stable rate across positions, temperatures and power reserve.
- Efficiency: power reserve per size and frequency.
- Architecture: integrated over modular for complications, sensible layouts, free-sprung balance.
- Finishing: decoration and attention to detail.
- Innovation: genuinely new solutions, not just new names.

A well regulated, well serviced workhorse often outperforms an exotic caliber in daily use. Exotic movements can be expensive and slow to service.
