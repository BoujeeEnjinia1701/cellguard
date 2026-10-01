---
doc_id: CGD-DEC-001
title: CellGuard design decisions register
project: CellGuard
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-09-30'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note, the decision records and the build plan work
---

# CellGuard design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, all proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes (spacers and screws, gap pad, cover pillars and notches, fixing positions, fuse holder in line with B+ and copper link, stud terminals, mounting holes, connector position) | (a) accept; (b) ask for changes | (a) | The whole build plan | CGD-DDR-003, A1 |
| 2 | Budget margin of $2.00 after the parts added for construction | (a) keep $140 and confirm the protector fuse price first; (b) raise `budget_usd` | (a) | Parts buying | CGD-DDR-003, A2 |
| 3 | Cover material | (a) printed flame-retardant polycarbonate, as drawn; (b) sheet aluminium, cut and bent | None made | Cover making (section 3.5, CGD-DWG-104) | CGD-DDR-001 item 12; CGD-DDR-002 |
| 4 | Cover colour: clear or opaque | (a) clear UL 94 V-0 polycarbonate, so the status light and board can be seen; (b) opaque, as the engineering media show | (a), if a clear V-0 grade can be printed or bought | Cover material bought | Review note, 2026-09-26 render session, item 1 |
| 5 | Response to R6, board loss 4.44 W against 4 W | (a) 1.5 mΩ-class switches (about 3.5 W); (b) move the protector fuse off the board and count it with the pack fuse | None made | Switch part number; board layout at TRL 4 | CGD-CAL-001 v0.3 section 12; CGD-DDR-002 |
| 6 | Response to R8, state of charge on 20 Ah packs | (a) restate R8 for 50 Ah and larger packs; (b) a periodic full-charge prompt; (c) a 0.5 mΩ shunt | None made | Shunt part (line 5) if (c) | CGD-CAL-001 v0.3 section 12; CGD-DDR-002 |
| 7 | Response to R14, mass 0.664 kg against 0.6 kg | (a) a 3 mm plate (0.599 kg; tapped M4 holes then have only 3 mm of thread); (b) relax the target to 0.7 kg (0.65 kg was offered before the parts added for construction) | None made | Plate thickness (section 3.2), spacer and screw lengths | CGD-CAL-001 v0.3 section 10; CGD-DDR-002; CGD-DDR-003 |
| 8 | Low-cost method to check the state-of-charge estimate | For example a calibrated shunt and an electronic load cycling a small pack | None made | First checks at TRL 4 | CGD-DDR-001 item 13 |
| 9 | First test partner | Solar installer, e-bike repair shop or makerspace | None made | Not part of the TRL 3 build | CGD-DDR-001 item 9 |
| 10 | Status light on the board | (a) add one three-colour status light to line 15; (b) none | (a) | Board layout at TRL 4 | Review note, 2026-09-26 render session, item 4 |
| 11 | Pack layout in product renders | (a) pack beside the board in renders only, engineering media keep the board above the pack; (b) one layout everywhere | (a) | Not part of the build | Review note, 2026-09-26 render session, item 2 |
| 12 | Cover fixing and power cables shown in the product renders | (a) accept as drawn in the renders, updated to the four pillars of CGD-DDR-003; (b) remove | (a) | Not part of the build | Review note, 2026-09-26 render session, items 3 and 5 |
| 13 | SwapCell project's agreement to the NMC profile and the SwapCell v0.3 CAN message set | Agreement from the SwapCell project | Decided on the CellGuard side (CGD-DDR-002) | Firmware at TRL 4 | CGD-PRC-001 open questions; review note cross-repo actions |

## To confirm when parts are bought

*Table 2. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | A protector fuse rated for 40 A continuous at 60 V DC or more, and its price | R4 depends on it; the $2.00 budget margin may not cover it | CGD-CAL-001 section 4; BOM line 14 |
| 2 | The fuse holder: base no larger than 44 x 32 mm, four M4 fixing holes at the drawn positions, M8 terminal studs, and fuse blade faces 12.6 mm above its mounting face | The copper link is flat only if the blade faces and the B+ stud shoulder are at the same height; the plate holes follow the holder | CGD-DDR-003 P5; BOM line 8 |
| 3 | The fuse and holder mass | The mass result keeps the concept figure of 89 g | CGD-CAL-001 v0.3 section 10 |
| 4 | The stud terminals: M6 male stud, 13 mm shoulder 6 mm tall, through-hole pins | The cable lugs and the link clamp on the shoulder; the shoulder height sets the link height | CGD-DDR-003 P6; BOM line 9 |
| 5 | The power switch package height of 2.3 mm (TOLT) | It sets the gap pad squeeze with 3 mm spacers; a different height needs a different spacer | CGD-DDR-003 P2; BOM line 4 |
| 6 | The gap pad: squeezes from 1.0 to 0.7 mm at a load the board fixings can apply, and insulates to at least 100 V | It is the only insulation between the live switch tops and the plate | CGD-DDR-003 P2; BOM line 17 |
| 7 | The TVS diode and switch avalanche energy against about 1 J | Short-circuit turn-off energy at a 15 µs delay | CGD-CAL-001 section 4 |
| 8 | A printable flame-retardant polycarbonate filament (or clear sheet, if decision 4 is (a)) | The cover is drawn for printing | BOM line 13 |

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | BQ76952-class front end; STM32G0B1-class controller building on the Libre Solar BMS firmware; BQ77216-class secondary protector with protector fuse; 40 A rating; high-side switching; LFP and NMC-capable hardware, LFP firmware first; SwapCell v0.3 CAN message set as a profile | Amish: "i accept all your recommendations, go with them across all repos." | [CGD-DDR-001](decisions/0001-trl2-review-decisions.md), [CGD-DDR-002](decisions/0002-recommendations-accepted.md) |
| 2026-09-25 | Budget raised from $120 to $140 | Amish, same instruction | CGD-DDR-002 |
| 2026-09-25 | Reused Apache-2.0 firmware kept in `firmware/third_party/` with its notices and listed in `LICENSE-SOFTWARE` | Amish, same instruction | CGD-DDR-002 |
| 2026-09-25 | Protection settings (SCD 100 mV at 15 µs, OCD2 40 mV at 20 ms, OCD1 24 mV at 320 ms, OCC 12 mV); top-side cooled TOLT switches; DPAK-class precharge switch; one-point current calibration at build | Amish, same instruction | CGD-DDR-002 |
| 2026-09-30 | Design for construction: the changes P1 to P8 that make the board buildable | Made under Amish's 2026-09-30 instruction ("fix the design assumptions to match and be physically feasible"); open for his review (open decision 1) | [CGD-DDR-003](decisions/0003-design-for-construction.md) |
