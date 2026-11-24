# The Hobbyist Workbench: Straps, Sizing, Modding and Learning Watchmaking

Use this file for hands-on questions: fitting straps and bracelets, sizing, modifying watches, building a watch from parts, and getting started in amateur watchmaking. Safety and value warnings in `servicing-and-care.md` still apply: practice on inexpensive watches, never on anything valuable or sentimental.

## Contents
1. Fit: wrist, case and strap sizing
2. Spring bars and strap changes
3. Bracelet sizing
4. Strap types and what suits what
5. Modding basics
6. Parts compatibility
7. Building a watch from parts
8. Learning watchmaking
9. A starter tool list
10. Legal and resale notes

## 1. Fit: wrist, case and strap sizing

- Measure wrist circumference with a soft tape just above the wrist bone.
- Lug-to-lug length matters more than diameter. A watch generally fits when its lug-to-lug is no longer than the flat top of the wrist. `horocalc.py fit --wrist-mm <circumference>` gives a rough ceiling; it is a rule of thumb, not a rule.
- Thickness and caseback shape change how a watch sits. Tall, flat-backed cases wear larger.
- Strap width equals lug width. A strap one millimeter too narrow leaves visible gaps; one too wide can sometimes be squeezed in with leather but never with rubber or metal.
- Strap length is given as two numbers, such as 120/75 mm for the long and short pieces. Small wrists under about 160 mm often need short straps; wrists over about 190 mm need long ones.
- Taper, such as 20 mm at the lugs narrowing to 16 mm at the buckle, looks dressier and wears more comfortably. Straight straps look sportier.

## 2. Spring bars and strap changes

- A spring bar tool has a forked end for straps and a pin end for drilled lugs and bracelets.
- Tape the lugs before working. Most strap-change scratches happen on the back of the lugs.
- Spring bar types:
  - Double shoulder or double flange: the standard, removable with a fork.
  - Single shoulder or shoulderless: for drilled lugs; removed by pushing through the hole.
  - Fat bars: Seiko divers commonly use 2.5 mm thick bars with larger tips. Standard 1.8 mm bars can be loose in those lug holes.
  - Quick release: a small lever built into the strap; no tool needed.
  - Curved bars: for curved-end straps.
- Measure bar length by the lug width, not overall length.
- Replace bent or weak spring bars. A failed bar drops the watch. Single-pass straps reduce that risk because the watch stays attached if one bar fails.

## 3. Bracelet sizing

- Remove equal links from both sides of the clasp to keep it centered, then fine-tune with the clasp's micro-adjust holes or half links.
- Link fastening types:
  - Screws: use a correctly sized, hollow-ground screwdriver. Screws are sometimes secured with thread locker; gentle heat helps release it. Reapply a low-strength thread locker when reassembling.
  - Push pins or split pins: drive out in the direction of the arrow stamped inside the link.
  - Pin and collar: common on Seiko. A tiny collar sits inside the center or outer link. Losing it makes the pin fall out later. Work over a tray.
  - Tool-free systems on some modern bracelets.
- Aim for a fit where a little finger slides under the clasp. Wrists swell in heat, so on-the-fly adjustment clasps are valuable.
- Keep removed links with the watch. Missing links reduce resale value.

## 4. Strap types and what suits what

| Strap | Best for | Notes |
|---|---|---|
| Steel bracelet | Everyday and sport | Most durable; solid end links and a milled clasp indicate quality. |
| Leather | Dress and casual | Keep away from water and sweat; ages with wear. |
| Rubber and FKM | Diving and heat | FKM fluoroelastomer resists dust and aging better than silicone. |
| Single-pass nylon | Field and dive | Passes under the case, adds height, very secure. |
| Two-piece nylon or sailcloth | Sport | Lower profile than single-pass. |
| Perlon | Summer | Woven, breathable, infinitely adjustable. |
| Mesh, such as Milanese and shark mesh | Vintage dive and dress | Adjustable; check for sharp edges. |
| Elastic fabric | Field and casual | Comfortable, one-piece, hook closure. |
| Tropic and waffle rubber | Vintage divers | 1960s styles reissued by several makers. |

## 5. Modding basics

Modding means changing parts on a watch for looks or function. The Seiko ecosystem is by far the largest, because so many aftermarket parts fit the SKX-style cases and the 7S26, 4R and NH movement families.

Common mods, roughly from easy to hard:
1. Strap or bracelet swap.
2. Bezel insert swap. Inserts are held by adhesive; aluminum, ceramic and sapphire inserts exist.
3. Crystal swap, such as a domed sapphire with anti-reflective coating. Needs a crystal press and a new gasket.
4. Bezel and chapter ring swaps.
5. Hands and dial swap. Needs hand removers, hand setters, and care with the dial and lume.
6. Movement swap, such as replacing a non-hacking 7S26 with an NH36, which adds hacking and hand winding.
7. Case swaps, crown swaps and full custom builds.

Rules that prevent most disasters:
- Work clean. Dust on a dial or under a crystal is the most common flaw. Use a blower and rodico putty, not breath.
- Never touch the dial surface or lume with fingers or metal tweezers.
- Set hands at 12:00 with the date just changed, so the date flips at midnight. Check that the hands clear each other through a full rotation.
- Replace gaskets, lubricate them with silicone grease, and pressure-test before trusting water resistance. A modded watch has unknown water resistance until tested.
- Mods void the manufacturer's warranty and usually lower resale value, except for well-executed builds sold to other enthusiasts.

## 6. Parts compatibility

Check these before buying parts. Sellers list them; confirm against the specific movement and case.

- Dial diameter and dial feet positions. Seiko dials for crown-at-3 cases and crown-at-4 cases have feet in different places. Many aftermarket dials have both sets, or the feet are clipped and the dial is fixed with dial dots.
- Hand hole sizes. Commonly cited sizes: Seiko 7S, 4R and NH families use 1.50 mm hour, 0.90 mm minute and 0.17 mm seconds; ETA 2824-2 and Sellita SW200 use 1.50, 0.90 and 0.25 mm. Hands are not interchangeable between these families. Confirm sizes for any other caliber on its technical sheet.
- Date wheel orientation: crown at 3 or at 4, and date window at 3, 4:30 or 6.
- Stem and crown: stems are movement-specific and must be cut to length for the case. Crown tube diameter and thread must match.
- Movement height and day-date versus date-only versions affect hand clearance and case fit.
- Crystal diameter, thickness and gasket type. A fraction of a millimeter matters.
- Bezel insert inner and outer diameters and whether the insert is flat or sloped.
- Movement holders or spacers must match the case.

## 7. Building a watch from parts

A first build usually combines a case kit, a dial, hands, an NH35 or NH36 movement, a crown and stem, and a strap.

1. Inspect and test the movement before installing anything.
2. Fit the dial to the movement, aligning the feet and securing them.
3. Fit the hands: hour, then minute, then seconds, checking alignment at 12:00 and clearance.
4. Clean the case and crystal interior. Blow out dust.
5. Case the movement with its holder and tighten the case clamps or screws.
6. Mark, cut and file the stem to length, test the fit, then secure the crown with a drop of thread locker.
7. Check winding, setting, date change and hacking.
8. Fit the caseback with a greased gasket. Pressure-test if water resistance matters.
9. Time it over several days and regulate if needed. See `accuracy-and-timing.md`.

Expect the first build to take several hours and to leave a speck of dust somewhere. That is normal.

## 8. Learning watchmaking

A sensible progression:
1. Read and watch: George Daniels' "Watchmaking" and de Carle's "Practical Watch Repairing" are classics; several watchmakers publish detailed teardown videos and online courses.
2. Start with strap changes, bracelet sizing, battery changes and regulation.
3. Disassemble and reassemble a large, simple, inexpensive movement. The usual choice is a Unitas 6497 or 6498 clone such as the Sea-Gull ST36, because the parts are big and replacements are cheap.
4. Learn cleaning and oiling: which lubricant goes where, and how little to use. See `movements.md`.
5. Move to a common automatic such as the NH35 or an ETA 2824 clone.
6. Then vintage watches, where parts sourcing and fault diagnosis become the real skill.

Formal routes: WOSTEP programs in Switzerland and partner schools, the British Horological Institute's distance learning courses, AWCI courses and certification in the United States, NAWCC workshops, and brand-sponsored schools. Local horological societies often run evening classes.

Honest expectations: basic servicing is learnable in months of practice. Hairspring work, balance staff replacement, jeweling, and vintage restoration take years. Do not service a watch you cannot afford to break.

## 9. A starter tool list

For straps, sizing and simple mods:
- Spring bar tool with fork and pin ends.
- Hollow-ground screwdrivers in common sizes, about 0.8 to 2.0 mm.
- Bracelet pin pusher and a small hammer with a link block.
- Caseback opener: a rubber ball for easy backs, a notched wrench or a bench opener for tight ones.
- Case holder.
- Loupe, 5x to 10x.
- Rodico cleaning putty and a dust blower.
- Brass or plastic tweezers.

For dial, hand and movement work, add:
- Hand removers or levers and a dial protector.
- Hand-setting tools.
- Movement holder.
- Finger cots.
- Crystal press with nylon dies.
- Stem cutters and a fine file.
- Demagnetizer.
- Timegrapher.
- Oilers, oil cups and the correct lubricants.
- Pressure tester, or access to a watchmaker who has one.

Buy good screwdrivers and tweezers first. Cheap ones slip and scratch.

## 10. Legal and resale notes

- Modifying your own watch is your business. Selling a modified watch requires honest disclosure of every non-original part.
- Aftermarket dials printed with a brand's logo are counterfeit trademarks in most jurisdictions, even on a genuine movement and case. Selling such watches under the brand name invites legal trouble; brands have pursued modders and customizers.
- Brand service centers may refuse modified watches or insist on replacing aftermarket parts at the owner's cost.
- Keep the original parts. Returning a watch to factory configuration protects its value.
