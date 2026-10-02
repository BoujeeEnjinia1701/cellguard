---
doc_id: CGD-DDR-003
title: CellGuard design for construction
project: CellGuard
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish, including the recommendation for A1; A2 carried as a part to confirm"
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendation for A1, which is now decided as recommended and recorded in the design decisions register (CGD-DEC-001). A2 is carried in the register as To confirm item 1. Nothing here changes what CellGuard does, its pitch or its safety case.

## Context

On 2026-09-30 Amish asked for every repo's build plan to show how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model (CGD-DWG-001 Rev P1) showed the right parts in the right places, but several could not be made or fixed as drawn. Checking the model with build123d (overlaps, contacts, clearances and whether each part can reach its place in assembly order) found the eight problems in Table 1.

The changes keep the board's function, electrical design, size class and main interfaces: the same plate, board outline, MOSFET bank, stud positions and order, connectors, fuse rating and cover footprint. Every change is in `cad/src/model.py`, which now runs 46 constructability checks (`python cad/src/model.py --check`): no two parts overlap, 17 pairs of faces that must touch do touch, 14 clearances hold, the gap pad compression and link height match, and each of 12 assembly moves reaches its place without passing through a part already fitted. All 46 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The four board standoffs were drawn as part of the 4 mm plate, 2.8 mm tall. A flat sheet cannot carry them, and nothing held the board to them: the board had no holes and there were no screws. | The plate is flat. The board sits on six bought round aluminium spacers 3 mm tall and is held by six M3 countersunk screws put up through countersunk holes in the plate, so the plate's underside stays flat for mounting. | Bought spacers set the board height exactly; screws from below leave the top free for the pillars and nuts. |
| P2 | The gap between board and plate equalled the MOSFET height plus a 0.5 mm pad, with nothing to take up tolerance: a slightly short MOSFET would not touch the pad, a tall one would lift the board. | A 3.0 mm board-to-plate gap and a 1.0 mm gap pad squeezed to 0.7 mm (30 %) by the 2.3 mm MOSFETs. | A compressible gap pad takes up the tolerance of the MOSFET height and the spacers, so every MOSFET presses on it. Its thermal resistance rises by 40 %, which raises the hottest junction by 0.3 K (CGD-CAL-001 v0.3). |
| P3 | The cover had no fixing. Its connector window and probe lead exit were closed openings, so the cover could not be lowered over the CAN connector, harness or probe leads, which already pass through its walls. | The cover rests on four bought 20 mm M3 pillars that thread onto the board screws at the signal end and beside the precharge resistor and shunt, and is held by four M3 x 6 screws. The connector and probe openings become notches open at the bottom. The walls stand 0.5 mm clear of the plate, so only the pillars carry it. | Uses the board screws again, so no new holes in the plate. With the notches open at the bottom, the cover drops straight down over the connectors and leads. |
| P4 | The two board fixings at the power end, if given a nut or screw head on top, would hit the B+ stud shoulder and the SCP fuse. | They move to 71.5 mm right of centre and 43.5 mm each side, carrying a nyloc nut 2.2 mm clear of the stud and 1.3 mm clear of the SCP fuse. Two new fixings at 48 mm right of centre and 44 mm each side carry the cover's power-end pillars. | Six fixings hold the board at both ends and beside the MOSFET bank, and every head and nut has room. |
| P5 | The pack fuse holder sat on the plate with no fixing, on the centre line, and nothing joined it to the B+ stud: the fuse was a block at a different height from the stud, 33 mm to one side. | The fuse holder moves 33 mm to the B+ side, in line with the B+ stud, and is held by four M4 screws into tapped holes in the plate. A straight copper link, 14 x 3 mm and 41 mm long (new BOM line 18), joins the B+ stud's shoulder to the fuse blade at the holder's inner terminal, both 10.6 mm above the plate. The holder's base height is set so the two faces match. | A straight flat bar is easy to make, carries the full pack current with low resistance and keeps 7.5 mm from the P+ stud's ring lug. A cable with two lugs would not fit in the 27 mm between the studs. |
| P6 | The power studs were drawn as cylinders on the board with no stated way of fixing them. | Bought through-hole power terminals with an M6 male stud and a 13 mm shoulder 6 mm tall, soldered through the board, pins trimmed to 1 mm under the board, 2 mm above the plate. | A soldered terminal block is how a board this size carries 40 A; the shoulder is the face the ring lugs and the link clamp against. |
| P7 | The plate had no way of being fixed to a pack or a vehicle. | Four M4 tapped holes, 30 and 167 mm in from the signal end and 30 mm each side of the centre line; the mounting screws come up from below and stop inside the plate. | No head stands above the plate, so the holes can sit under the board. The hero picture's pack posts move to these holes. |
| P8 | The CAN and UART connector overhung the board edge by 9 mm and crossed the cover wall. | The connector moves so its mating face is flush with the cover's outside face: 5 mm past the board edge, 13 mm on the board, 1.5 mm clear of the pillar. | A right-angle connector this size is supported by its pins and board locks over 13 mm of board. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Line 17 now lists the gap pad (1.0 mm), six spacers, four pillars, screws and nuts: $5.00 to $7.00. New line 18, copper fuse link, $2.00. Line 8 states the holder's footprint, fixing holes and terminal height; line 9 the stud terminal's shoulder. Total $138.00, 98.6 % of the $140 budget, $2.00 margin (was $134.00 and $6.00). | Parts added for construction. |
| Mass | 0.664 kg (was 0.646 kg): gap pad, spacers, pillars, screws and nuts 25 g, copper link 12 g. The fuse and holder stay at the concept figure of 89 g until the holder is chosen. R14 stays not met. A 3 mm plate would now give 0.599 kg. | Parts added for construction. |
| Thermal | Hottest junction 54.0 °C at 40 A (was 53.7 °C); 59.5 °C (TOLT) and 99.1 °C (TOLL) bounds at 80 A for 10 s (were 58.1 °C and 97.7 °C). Board loss unchanged at 4.44 W. R5 stays met, R6 stays not met. | Thicker pad (P2). |
| Size | Envelope 220 x 110 x 33 mm to the cover screw heads (was 32 mm). R14 size still met. | Pillars set the cover height (P3). |
| Drawings | CGD-DWG-001 Rev P2; making sketches CGD-DWG-101 to 105 added. | Follow the model. |
| Documents | CGD-CAL-001 v0.3, CGD-PRC-001 v0.5, CGD-REQ-001 v0.5, CGD-PRB-001 v0.5: figures above. No requirement changed status: 10 met on paper, 3 not met (R6, R8, R14), 3 at risk (R2, R4, R7). | Follow the model. |
| Appearance model | `cad/src/product_model.py` reads the new spacer positions; the photoreal renders made on Amish's Mac still show the concept plate and fuse position. | Renders are made on the Mac. |

*Table 3. Items proposed for Amish; A1 accepted by Amish as recommended on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Accept the changes P1 to P8. | (a) accept; (b) ask for changes. | (a). Accepted by Amish, 2026-10-02. |
| A2 | The estimated cost is $2.00 under the $140 value-engineering target after lines 17 and 18, and the SCP fuse, whose price is not confirmed, could use it up. | Confirm the SCP fuse price first; any overrun is reported as over the value-engineering target, a hypothetical control target, not a limit. | Confirm the SCP fuse price first. Carried as To confirm item 1 in CGD-DEC-001. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CGD-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Open decisions are kept in the design decisions register CGD-DEC-001 (`docs/06-design-decisions.md`). With A1 accepted on 2026-10-02, the changes P1 to P8 stand as made.
- The copper layout of the board is TRL 4 work. It must keep the outline, fixing holes, stud positions and MOSFET positions on CGD-DWG-103.
- The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` show the concept fuse position and plate; they need regenerating on Amish's Mac.
