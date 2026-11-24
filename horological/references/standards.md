# Standards, Certifications, Origin Rules and Hallmarks

Use this file to explain what a marking, certificate or origin claim actually guarantees. Accuracy certifications, COSC, METAS and brand chronometer standards, are covered in detail in `accuracy-and-timing.md`.

## Contents
1. Origin rules: Swiss Made, Glashütte, Japan, others
2. Quality seals: Geneva Seal, Patek Philippe Seal, Fleurier
3. ISO and industry standards
4. Military specifications
5. Precious metal hallmarks and marks
6. Terms with no legal definition

## 1. Origin rules

### Swiss Made
The Swiss ordinance on the use of the name "Swiss" for watches, tightened from 1 January 2017, requires for a watch:

- A Swiss movement.
- Casing in Switzerland.
- Final inspection by the manufacturer in Switzerland.
- At least 60 percent of manufacturing costs incurred in Switzerland.
- Technical development carried out in Switzerland.

A movement is Swiss when it is assembled and inspected in Switzerland, at least 60 percent of its manufacturing costs are Swiss, components of Swiss manufacture make up at least 50 percent of the value of all components excluding assembly, and its technical development is in Switzerland.

Before 2017 the threshold was 50 percent of the movement's component value with no whole-watch cost test, which allowed many "Swiss Made" watches with largely Asian-made cases, dials and bracelets.

Dial markings:
- "Swiss Made" or "Swiss": meets the rules above.
- "Swiss Movt" or "Swiss Movement": only the movement is Swiss; casing and other parts may be elsewhere.
- "Swiss Parts": ambiguous and generally not a compliant origin claim; treat it skeptically.
- "Swiss Quartz": a quartz watch claiming Swiss origin.
- "T Swiss Made T" and "Swiss T < 25": the T marks indicate tritium lume. See `cases-and-materials.md`.

Even a compliant Swiss Made watch can contain foreign components up to the cost thresholds. That is legal and common.

### Made in Glashütte
- For about a century an unwritten local rule held that at least half of a watch's value had to be created in Glashütte to use the name.
- Since February 2022 the Glashütte Regulation under German trademark law makes this binding: more than 50 percent of the value added in the essential manufacturing stages, and those essential stages themselves, must take place in the defined Glashütte area.
- Brands using it include A. Lange & Söhne, Glashütte Original, Nomos, Moritz Grossmann, Tutima Glashütte, Mühle-Glashütte, Union Glashütte and Wempe Glashütte.
- "Made in Germany" by itself is a broader and looser claim.

### Japan and other markings
- "Made in Japan": generally assembled in Japan. Seiko's domestic market and higher lines often carry it.
- "Movt Japan" or "Japan Movt": a Japanese movement, typically cased and assembled elsewhere, often in China or Malaysia.
- There is no Japanese equivalent of the Swiss cost threshold rules.
- Other origin claims, such as "Made in USA," fall under general national rules. In the US, the Federal Trade Commission expects an unqualified "Made in USA" claim to mean all or virtually all made in the US, which very few watches meet. Many American brands use qualified claims like "assembled in USA."

## 2. Quality seals

### Geneva Seal, Poinçon de Genève
- Created by a Geneva law of 1886, administered by the canton's watchmaking school and inspection office.
- Requires the movement to be assembled, cased and regulated in the canton of Geneva, and to meet strict finishing criteria for every part, including beveled and polished edges, polished screw heads and jewel sinks, and no visible machining marks.
- Since the 2012 revision it covers the whole cased watch and adds functional tests, including water resistance, power reserve and a precision test of at most one minute of deviation after seven days.
- Main users: Vacheron Constantin and Roger Dubuis, plus selected pieces from Cartier, Chopard and Louis Vuitton among others. Patek Philippe left it in 2009 for its own seal.
- The mark is engraved on the movement and, since 2012, also on the case.

### Patek Philippe Seal
- Introduced in 2009 for all Patek Philippe mechanical watches, replacing the Geneva Seal.
- Covers finishing, serviceability and repairability "for life," and accuracy for the cased watch, commonly stated as minus 3 to plus 2 seconds per day for movements of 20 mm or more, with different limits for small movements and tourbillons.
- It is a brand standard, not an independent certification.

### Fleurier Quality Foundation, FQF
- Founded in 2001 by Chopard, Parmigiani Fleurier, Bovet and Vaucher Manufacture.
- Requires entirely Swiss manufacture, COSC certification, a Chronofiable aging and reliability test, the Fleuritest simulated-wear rate test, and finishing criteria.
- Few watches carry it; it is among the most demanding seals.

### Others
- Hallmarks of individual brands, such as Rolex's green Superlative Chronometer tag, Omega's Master Chronometer card, and Grand Seiko Special Standard, are company standards. Explain what each tests rather than treating them as interchangeable.
- Kew certificates, from the Kew Observatory in Britain, were historical precision certificates; Class A was the top grade.

## 3. ISO and industry standards

| Standard | Subject | Key points |
|---|---|---|
| ISO 3159 | Wristwatch chronometers with spring balance oscillator | The basis of COSC testing; see `accuracy-and-timing.md`. |
| ISO 6425 | Divers' watches | Minimum 100 m, testing at 125 percent of rating, time preselection device, legibility in darkness, magnetism, shock and saltwater resistance, individual testing; a saturation diving class. Details in `cases-and-materials.md`. |
| ISO 22810 | Water-resistant watches | General water resistance tests; replaced ISO 2281. |
| ISO 764 | Magnetic resistant watches | Baseline: the watch must withstand 4,800 A/m, about 60 gauss, with limited rate change afterward. The 2020 edition adds an enhanced magnetic resistance class in Annex A and an informative annex on everyday magnetic sources and distances. Confirm the enhanced class values against the standard before quoting them. |
| ISO 1413 | Shock-resistant watches | Defines a drop test, roughly equivalent to a fall from 1 m onto hardwood. |
| NIHS | Swiss watch industry norms | Detailed Swiss technical norms published by the Federation of the Swiss Watch Industry. |
| JIS | Japanese Industrial Standards | Japan's own standards for water resistance and other properties. |

Magnetism comparisons:
- ISO 764 baseline: 4,800 A/m, about 60 gauss.
- Rolex Milgauss: historically 1,000 gauss.
- IWC Ingenieur original: about 80,000 A/m, roughly 1,000 gauss.
- Omega Master Chronometer: 15,000 gauss, about 1.5 tesla.
- Use `horocalc.py magnet` to convert units.

## 4. Military specifications

- US: MIL-W-46374 for general-purpose wristwatches from the 1960s onward, produced by Benrus, Hamilton, Marathon and others, and earlier WWII-era specifications for "hack" watches made by Hamilton, Elgin, Waltham and Bulova. Many specifications required hacking, luminous dials, and later tritium. Look up the exact specification number and revision when dating a military watch.
- UK: the "W.W.W." or "Dirty Dozen" watches of 1945 from twelve Swiss makers; the 1970s Cabot Watch Company and Hamilton dive and general service watches marked with the broad arrow; DEF STAN 66-4 for later issued watches.
- Germany: Beobachtungsuhren or B-Uhr pilot's observation watches of WWII, made by Lange, Wempe, Laco, Stowa and IWC.
- Italy: Panerai for the navy's frogmen.
- Military provenance is heavily faked. Look for matching issue markings, records, and correct period components.

## 5. Precious metal hallmarks and marks

- Switzerland: an official hallmark, the head of a Saint Bernard dog for gold, alongside fineness marks such as 750 for 18k and 950 for platinum. Swiss Made gold cases also often bear the Common Control Mark of the Vienna Convention, a balance scale with the fineness.
- UK: assay office marks such as the leopard's head for London, the anchor for Birmingham, the Yorkshire rose for Sheffield, and the castle for Edinburgh, with a date letter that can date a case precisely.
- France: the eagle's head for 18k gold.
- Common Control Mark: recognized among member states of the Vienna Convention on hallmarking.
- US: no state hallmarking system. Watches are marked with karat or fineness, such as 14K or 585.
- Gold filled and plated:
  - Gold filled or "GF": a layer of gold alloy bonded to base metal, traditionally at least 1/20 of the total weight.
  - Rolled gold plate: a thinner bonded layer.
  - Gold plated or electroplated: very thin; a micron count may be given, such as "20 microns."
  - "Gold capped" or "gold shell" are period terms with varying meanings.
- A case can be solid gold while the caseback or inner case is not, and vice versa. Look at every component's marks.

## 6. Terms with no legal definition

Explain these carefully, because buyers often assume they guarantee more than they do:

- In-house or manufacture: no legal standard. It may mean full in-house design and parts production including hairsprings, or only final assembly of a movement designed elsewhere. Ask who designed it, who makes the escapement and hairspring, and who assembles it.
- Limited edition: may mean 50 pieces or 10,000. Check the number and whether the brand later reissued it.
- Military grade, tactical, aviation: marketing unless tied to a published military specification and an actual contract.
- Anti-magnetic: legally meaningful only when the watch is tested against ISO 764 or a published brand standard.
- Water resistant without a rating: implies splash resistance only.
- Hand-finished or hand-assembled: ranges from fully hand-beveled parts to a human performing final assembly of machine-finished components.
- Heritage or historic: says nothing about whether the brand has continuous history; many names are revived trademarks.
