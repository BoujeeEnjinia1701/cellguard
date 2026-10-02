---
doc_id: CGD-DDR-001
title: CellGuard TRL 2 review decisions
project: CellGuard
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and the items that stay open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Items 9, 12, 13 and the R6, R8 and R14 parts of item 15 decided by Amish as recommended (CGD-DEC-001)"
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted in part. On 2026-09-25 Amish accepted all recommendations ("i accept all your recommendations, go with them across all repos"). Items 1 to 8, 10, 11 and 14 and the R16 part of item 15 are decided by Amish, 2026-09-25: go with recommendation (see CGD-DDR-002). Items 9, 12, 13 and the R6, R8 and R14 parts of item 15 had no recommendation at TRL 2; recommendations were written for them later, and Amish approved them on 2026-10-02: "i approve your recommendations for all 555 open decisions." (CGD-DEC-001).

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed nine items as "Proposed, awaiting Amish", eight of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CellGuard items one by one. Under that instruction, each item that has a recommendation is adopted as recommended for TRL 3, open for his review; items without a recommendation stay open. Budgets are not changed in `project.yaml`: a recommended budget is recorded here as awaiting Amish. TRL 4 is on hold by Amish's instruction.

Later on 2026-09-25 Amish accepted all recommendations across the portfolio. This v0.2 records every item that had a recommendation as decided and changes the budget to $140; the details and the changes made in the repo are in [CGD-DDR-002](0002-recommendations-accepted.md).

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and CGD-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Items decided (originally adopted for TRL 3 work, confirmed by Amish on 2026-09-25).*

| # | Item | Status and content | Where it now lives |
| --- | --- | --- | --- |
| 1 | Front end | Decided by Amish, 2026-09-25: go with recommendation. TI BQ76952 class (3 to 16 cells, autonomous protection, integrated high-side driver and coulomb counter) | CGD-PRC-001 v0.3, `bom/bom.csv` line 3, CGD-CAL-001 |
| 2 | Microcontroller and firmware base | Decided by Amish, 2026-09-25: go with recommendation. Option A: STM32G0B1 class with CAN, building on the Libre Solar BMS firmware (Apache-2.0). How Apache-2.0 code sits in this MIT-licensed repo is decided under item 10 | CGD-PRC-001 v0.3, `bom/bom.csv` line 6 |
| 3 | Secondary protector (safety trade-off) | Decided by Amish, 2026-09-25: go with recommendation. Add a BQ77216-class independent protector (overvoltage, undervoltage, open wire, temperature) driving a self-control protector (SCP) fuse in the B+ path, about $10 | CGD-PRC-001 v0.3, `bom/bom.csv` line 14, `cad/src/model.py` part 14, CGD-CAL-001 section 4 |
| 4 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Option (a): `budget_usd` raised from $120 to $140 in `project.yaml`; the $134 BOM is $6 under it | `project.yaml`, CGD-REQ-001 R16, CGD-CAL-001 section 11 |
| 5 | Current rating | Decided by Amish, 2026-09-25: go with recommendation. 40 A continuous for the first board; a 100 A variant later only if storage users need it | CGD-REQ-001 R5 (unchanged) |
| 6 | Switching side | Decided by Amish, 2026-09-25: go with recommendation. High-side N-channel switching, keeping a common ground for CAN | CGD-PRC-001 v0.3 |
| 7 | Chemistry scope | Decided by Amish, 2026-09-25: go with recommendation. Hardware designed for LFP and for an NMC profile (up to 14S under 60 V, which covers SwapCell's 13S), LFP firmware released first. Use as SwapCell's BMS still needs the SwapCell project's agreement. The pitch is unchanged | CGD-REQ-001 R1, CGD-PRB-001 v0.3, CGD-PRC-001 v0.3 |
| 8 | CAN message set | Decided by Amish, 2026-09-25: go with recommendation. CellGuard carries the SwapCell interface v0.3 message set (250 kbit/s, 11-bit identifiers) as a profile, subject to the SwapCell project | CGD-REQ-001 R11, CGD-PRC-001 v0.3, CGD-CAL-001 section 8 |

No pitch or problem rewording was recommended at TRL 2, so `project.yaml` and the README keep their pitch and problem lines.

### Items that remain open

*Table 2. Remaining items and their status after 2026-09-25.*

| # | Item | Status |
| --- | --- | --- |
| 9 | First test partner (solar installer, e-bike repair shop or makerspace) | Decided by Amish, 2026-10-02, as recommended: a small off-grid solar installer that builds 16S LFP packs is the first candidate to approach, testing on their bench rather than in a customer system (CGD-DEC-001) |
| 10 | Licensing of Apache-2.0 firmware code in an MIT-licensed repo | Decided by Amish, 2026-09-25: go with recommendation. Reused files keep Apache-2.0 and their notices in `firmware/third_party/` and are listed in `LICENSE-SOFTWARE` |
| 11 | Budget figure (item 4) | Decided by Amish, 2026-09-25: go with recommendation ($140) |
| 12 | Cover material: printed flame-retardant polycarbonate or sheet aluminium | Decided by Amish, 2026-10-02, as recommended: printed flame-retardant polycarbonate, as drawn; sheet aluminium is not used (CGD-DEC-001) |
| 13 | Low-cost method to check the state-of-charge estimate (for example a calibrated shunt and a bench load) | Decided by Amish, 2026-10-02, as recommended: cycle a 4S 20 Ah LFP pack through seven days of partial cycles with a bench supply and a low-cost DC electronic load, count charge with a calibrated reference shunt and meter, then discharge fully to measure the true state of charge (CGD-DEC-001) |
| 14 | TRL 3 engineering proposals from CGD-CAL-001: protection thresholds (SCD 100 mV with 15 µs delay, OCD1 24 mV with 320 ms, OCD2 40 mV with 20 ms, OCC 12 mV), a top-side cooled MOSFET package, a DPAK-class precharge switch, one-point current calibration at build | Decided by Amish, 2026-09-25: go with recommendation |
| 15 | Responses to the requirements CGD-CAL-001 finds not met (R6 board loss, R8 state of charge on small packs, R14 mass, R16 cost): options are listed in CGD-CAL-001 section 12 | R16: decided by the $140 budget (item 11). R6, R8 and R14: decided by Amish, 2026-10-02, as recommended (CGD-DEC-001): 1.5 mΩ-class switches for R6; a full-charge prompt after about five days, with R8 restated to apply between prompted full charges; R14 relaxed to 0.7 kg |

## Consequences

- R4 is closed on paper by the secondary protector, but it depends on finding an SCP fuse rated for 40 A at 60 V DC or more; until then R4 is at risk.
- The SCP fuse adds about 0.6 W at 40 A on the board, which pushes the board loss to about 4.4 W against the 4 W of R6.
- Parts cost rises to $134. With the $140 budget decided on 2026-09-25, R16 is met with a $6 margin.
- The SwapCell message set fixes the bus at 250 kbit/s. MotionCore, which plans to read CellGuard faults over CAN, must run its bus at the same rate.
- If CellGuard serves as SwapCell's BMS, it must also carry SwapCell's INTERLOCK wake input (about 30 µA in sleep); CGD-CAL-001 shows sleep stays within SwapCell's 100 µA limit.
- The BQ77216 overvoltage threshold (3.55 to 5.1 V) is chosen by orderable part option, so an LFP build and an NMC build need different part variants.
