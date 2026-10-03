---
doc_id: CGD-DEC-001
title: CellGuard design decisions register
project: CellGuard
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 12 (CGD-DDR-003 accepted); moved to decisions made; To confirm item 5 and 8 and the value-engineering savings updated"
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Approved follow-ups carried out: switches, status light and light pipe priced; value engineering restated (USD 159.15, USD 19.15 over the target); To confirm items for the switches, status light and light pipe"
---

# CellGuard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 2. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | A protector fuse rated for 40 A continuous at 60 V DC or more, and its price | R4 depends on it; the estimate is already over the value-engineering target, and this price could add to it | CGD-CAL-001 section 4; BOM line 14 |
| 2 | The fuse holder: base no larger than 44 x 32 mm, four M4 fixing holes at the drawn positions, M8 terminal studs, and fuse blade faces 12.6 mm above its mounting face | The copper link is flat only if the blade faces and the B+ stud shoulder are at the same height; the plate holes follow the holder | CGD-DDR-003 P5; BOM line 8 |
| 3 | The fuse and holder mass | The mass result keeps the concept figure of 89 g | CGD-CAL-001 v0.3 section 10 |
| 4 | The stud terminals: M6 male stud, 13 mm shoulder 6 mm tall, through-hole pins | The cable lugs and the link clamp on the shoulder; the shoulder height sets the link height | CGD-DDR-003 P6; BOM line 9 |
| 5 | The power switch package height of 2.3 mm (TOLT), in the 1.5 mΩ class decided on 2026-10-02, and its price of about $5.00 each | It sets the gap pad squeeze with 3 mm spacers (a different height needs a different spacer); the price sets most of the cost over the target | CGD-DDR-003 P2; BOM line 4 |
| 6 | The gap pad: squeezes from 1.0 to 0.7 mm at a load the board fixings can apply, and insulates to at least 100 V | It is the only insulation between the live switch tops and the plate | CGD-DDR-003 P2; BOM line 17 |
| 7 | The TVS diode and switch avalanche energy against about 1 J | Short-circuit turn-off energy at a 15 µs delay | CGD-CAL-001 section 4 |
| 8 | A printable flame-retardant polycarbonate filament (the cover is opaque, decided 2026-10-02); a clear cover only if clear polycarbonate sheet with a V-0 rating at the cover's wall thickness can be bought and formed | The cover is drawn for printing | BOM line 13 |
| 9 | The light pipe: 3 mm round, 19.6 mm below a flange about 6 mm across, and the hole it presses into (drawn 3.2 mm); the status light's package (PLCC-4, 3.5 x 2.8 x 1.9 mm) | The pipe's foot is drawn 0.5 mm above the light; a different length or hole needs the cover or pipe changed | BOM lines 13, 15 and 19 |

## Value engineering

Value-engineering target: USD 140.00 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 159.15 (USD 19.15 over the target).

Main cost drivers (CGD-CAL-001 v0.6, section 11): the eight 1.5 mΩ-class charge and discharge MOSFETs (line 4, $40.00, of which $20.00 is the step up from the 2.5 mΩ parts decided on 2026-10-02), supporting electronics with the status light (line 15, $16.35), the pack fuse and holder (line 8, $12.00), the aluminium base plate, the main PCB and the secondary protector with its SCP fuse (lines 1, 2 and 14, $10.00 each). The secondary protector and the parts added for construction (lines 17 and 18) account for $14.00 of the estimate; the status light and light pipe for $1.15.

Savings worth trying:

- Ask for a quantity price on the switches: power MOSFETs are usually markedly cheaper at quantity 100 or more, and each $1.00 off the unit price saves $8.00 on the board.
- Confirm the SCP fuse price, which may add to the estimate (CGD-DDR-003, A2).
- The status light stays (decided 2026-10-02) and the cover stays printed flame-retardant polycarbonate (decided 2026-10-02), so neither is a saving to try.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | BQ76952-class front end; STM32G0B1-class controller building on the Libre Solar BMS firmware; BQ77216-class secondary protector with protector fuse; 40 A rating; high-side switching; LFP and NMC-capable hardware, LFP firmware first; SwapCell v0.3 CAN message set as a profile | Amish: "i accept all your recommendations, go with them across all repos." | [CGD-DDR-001](decisions/0001-trl2-review-decisions.md), [CGD-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-09-25 | Budget raised from $120 to $140 | Amish, same instruction | CGD-DDR-002 |
| 2026-09-25 | Reused Apache-2.0 firmware kept in `firmware/third_party/` with its notices and listed in `LICENSE-SOFTWARE` | Amish, same instruction | CGD-DDR-002 |
| 2026-09-25 | Protection settings (SCD 100 mV at 15 µs, OCD2 40 mV at 20 ms, OCD1 24 mV at 320 ms, OCC 12 mV); top-side cooled TOLT switches; DPAK-class precharge switch; one-point current calibration at build | Amish, same instruction | CGD-DDR-002 |
| 2026-09-30 | Design for construction: the changes P1 to P8 that make the board buildable | Made under Amish's 2026-09-30 instruction ("fix the design assumptions to match and be physically feasible"). The changes themselves were accepted on 2026-10-02 (below) | [CGD-DDR-003](decisions/0003-design-for-construction.md) |
| 2026-10-02 | Design for construction accepted: the changes P1 to P8 (flat plate with bought spacers and screws, squeezed gap pad, cover pillars and notches, fixing positions, fuse holder in line with B+ and copper link, stud terminals, mounting holes, connector position), as made | Amish: "i approve your recommendations for all 555 open decisions." | [CGD-DDR-003](decisions/0003-design-for-construction.md), A1 |
| 2026-10-02 | Cover material: printed flame-retardant polycarbonate, as drawn (option a); sheet aluminium is not used, since a metal cover would sit a few millimetres from live 58 V studs and nuts | Amish: "i approve your recommendations for all 555 open decisions." | CGD-DDR-001 item 12; CGD-DDR-002 |
| 2026-10-02 | Cover colour: the prototype cover is opaque, with a light pipe over the status light; a clear cover only if clear polycarbonate sheet with a V-0 rating at the cover's wall thickness can be bought and formed | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26 render session, item 1 |
| 2026-10-02 | R6 board loss: fit 1.5 mΩ-class switches in the TOLT package (option a), bringing the board loss to about 3.5 W; the protector fuse stays on the board | Amish: "i approve your recommendations for all 555 open decisions." | CGD-CAL-001 v0.3 section 12; CGD-DDR-002 |
| 2026-10-02 | R8 state of charge: the firmware prompts for a full charge when about five days pass without one (option b), and R8's partial-cycling clause is restated to apply between prompted full charges; the 0.5 mΩ shunt is not fitted | Amish: "i approve your recommendations for all 555 open decisions." | CGD-CAL-001 v0.3 section 12; CGD-DDR-002 |
| 2026-10-02 | R14 mass: target relaxed to 0.7 kg (option b); the 4 mm plate is kept | Amish: "i approve your recommendations for all 555 open decisions." | CGD-CAL-001 v0.3 section 10; CGD-DDR-002; CGD-DDR-003 |
| 2026-10-02 | State-of-charge check: cycle a 4S 20 Ah LFP pack (the worst case for R8) through seven days of partial cycles with a bench supply and a low-cost DC electronic load, count charge independently with a calibrated reference shunt and meter, then discharge fully to measure the true state of charge | Amish: "i approve your recommendations for all 555 open decisions." | CGD-DDR-001 item 13 |
| 2026-10-02 | First test partner: a small off-grid solar installer that builds 16S LFP packs, testing on their bench rather than in a customer system (the first candidate to approach) | Amish: "i approve your recommendations for all 555 open decisions." | CGD-DDR-001 item 9 |
| 2026-10-02 | Status light: one three-colour status light added to the supporting electronics, line 15 (option a) | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26 render session, item 4 |
| 2026-10-02 | Product renders: the pack beside the board in the product renders only; engineering media keep the board above the pack | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26 render session, item 2 |
| 2026-10-02 | Product renders keep the cover fixing and power cables, updated to the four pillars of CGD-DDR-003 | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26 render session, items 3 and 5 |
| 2026-10-02 | SwapCell agreement to the NMC profile and the v0.3 CAN message set: record it in the SwapCell repo as well (Amish owns both), but only after the board envelope question is settled (SwapCell expects about 230 x 58 mm, 10 mm or less thick, at $120; CellGuard is 220 x 110 x 33 mm at $138) | Amish: "i approve your recommendations for all 555 open decisions." | CGD-PRC-001 open questions; review note cross-repo actions |
