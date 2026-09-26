---
doc_id: CGD-DDR-001
title: CellGuard TRL 2 review decisions
project: CellGuard
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and the items that stay open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items 1 to 8 are adopted for TRL 3 work pending Amish's review; items 9 to 15 remain proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed nine items as "Proposed, awaiting Amish", eight of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CellGuard items one by one. Under that instruction, each item that has a recommendation is adopted as recommended for TRL 3, open for his review; items without a recommendation stay open. Budgets are not changed in `project.yaml`: a recommended budget is recorded here as awaiting Amish. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and CGD-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Status and content | Where it now lives |
| --- | --- | --- | --- |
| 1 | Front end | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. TI BQ76952 class (3 to 16 cells, autonomous protection, integrated high-side driver and coulomb counter) | CGD-PRC-001 v0.3, `bom/bom.csv` line 3, CGD-CAL-001 |
| 2 | Microcontroller and firmware base | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Option A: STM32G0B1 class with CAN, building on the Libre Solar BMS firmware (Apache-2.0). How Apache-2.0 code sits in this MIT-licensed repo stays open (item 10) | CGD-PRC-001 v0.3, `bom/bom.csv` line 6 |
| 3 | Secondary protector (safety trade-off) | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Add a BQ77216-class independent protector (overvoltage, undervoltage, open wire, temperature) driving a self-control protector (SCP) fuse in the B+ path, about $10 | CGD-PRC-001 v0.3, `bom/bom.csv` line 14, `cad/src/model.py` part 14, CGD-CAL-001 section 4 |
| 4 | Budget | Recommendation (a), raise `budget_usd` to $140, is **Proposed, awaiting Amish**. `budget_usd` stays at $120 in `project.yaml`. CGD-CAL-001 states the cost against both figures: $134 is 11.7 % over $120 and $6 under $140 | CGD-REQ-001 R16, CGD-CAL-001 section 11 |
| 5 | Current rating | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. 40 A continuous for the first board; a 100 A variant later only if storage users need it | CGD-REQ-001 R5 (unchanged) |
| 6 | Switching side | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. High-side N-channel switching, keeping a common ground for CAN | CGD-PRC-001 v0.3 |
| 7 | Chemistry scope | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Hardware designed for LFP and for an NMC profile (up to 14S under 60 V, which covers SwapCell's 13S), LFP firmware released first. Use as SwapCell's BMS still needs the SwapCell project's agreement. The pitch is unchanged | CGD-REQ-001 R1, CGD-PRB-001 v0.3, CGD-PRC-001 v0.3 |
| 8 | CAN message set | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. CellGuard carries the SwapCell interface v0.3 message set (250 kbit/s, 11-bit identifiers) as a profile, subject to the SwapCell project | CGD-REQ-001 R11, CGD-PRC-001 v0.3, CGD-CAL-001 section 8 |

No pitch or problem rewording was recommended at TRL 2, so `project.yaml` and the README keep their pitch and problem lines.

### Items that remain open

*Table 2. Items still Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| 9 | First test partner (solar installer, e-bike repair shop or makerspace) | Proposed, awaiting Amish. No preference stated |
| 10 | Licensing of Apache-2.0 firmware code in an MIT-licensed repo | Proposed, awaiting Amish. Suggested for his review: keep reused files under Apache-2.0 with their notices in a separate firmware folder and list them in `LICENSE-SOFTWARE`. No choice has been made |
| 11 | Budget figure (item 4) | Proposed, awaiting Amish: $140 recommended |
| 12 | Cover material: printed flame-retardant polycarbonate or sheet aluminium | Proposed, awaiting Amish. No recommendation was made |
| 13 | Low-cost method to check the state-of-charge estimate (for example a calibrated shunt and a bench load) | Proposed, awaiting Amish. No recommendation was made |
| 14 | TRL 3 engineering proposals from CGD-CAL-001: protection thresholds (SCD 100 mV with 15 µs delay, OCD1 24 mV with 320 ms, OCD2 40 mV with 20 ms, OCC 12 mV), a top-side cooled MOSFET package, a DPAK-class precharge switch, one-point current calibration at build | Engineering proposals, awaiting Amish's confirmation |
| 15 | Responses to the requirements CGD-CAL-001 finds not met (R6 board loss, R8 state of charge on small packs, R14 mass, R16 cost): options are listed in CGD-CAL-001 section 12 | Proposed, awaiting Amish. No choice has been made |

## Consequences

- R4 is closed on paper by the secondary protector, but it depends on finding an SCP fuse rated for 40 A at 60 V DC or more; until then R4 is at risk.
- The SCP fuse adds about 0.6 W at 40 A on the board, which pushes the board loss to about 4.4 W against the 4 W of R6.
- Parts cost rises to $134. R16 is not met against the $120 in `project.yaml` and would be met against the recommended $140.
- The SwapCell message set fixes the bus at 250 kbit/s. MotionCore, which plans to read CellGuard faults over CAN, must run its bus at the same rate.
- If CellGuard serves as SwapCell's BMS, it must also carry SwapCell's INTERLOCK wake input (about 30 µA in sleep); CGD-CAL-001 shows sleep stays within SwapCell's 100 µA limit.
- The BQ77216 overvoltage threshold (3.55 to 5.1 V) is chosen by orderable part option, so an LFP build and an NMC build need different part variants.
