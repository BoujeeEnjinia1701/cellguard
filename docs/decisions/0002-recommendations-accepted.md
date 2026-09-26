---
doc_id: CGD-DDR-002
title: CellGuard recommendations accepted
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
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted

## Context

CGD-DDR-001 v0.1 recorded the TRL 2 review items as adopted for TRL 3 work, open for Amish's review, and left the budget, the firmware licensing rule and the TRL 3 engineering proposals as proposed, awaiting Amish. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item that carried a recommendation is therefore decided as recommended. Where a recommendation offered several options, the recommended option is the decision. Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, and the project stays at TRL 3 with a TRL 3 target.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 and TRL 3 sessions), CGD-DDR-001 and CGD-CAL-001 section 12. They are not repeated here.

## Decision

*Table 1. Items decided by Amish, 2026-09-25: go with recommendation.*

| # (DDR-001) | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | Front end | TI BQ76952 class | Wording only: CGD-PRC-001 v0.4, `bom/bom.csv` line 3 note |
| 2 | Microcontroller and firmware base | STM32G0B1 class building on the Libre Solar BMS firmware | Wording only: CGD-PRC-001 v0.4, `bom/bom.csv` line 6 note |
| 3 | Secondary protector | BQ77216-class protector with SCP fuse | Wording only: CGD-PRC-001 v0.4, `bom/bom.csv` line 14 note |
| 4 and 11 | Budget | Option (a): raise `budget_usd` from $120 to $140 | `project.yaml` `budget_usd: 140`; CGD-REQ-001 v0.4 R16 target $140; CGD-CAL-001 v0.2 section 11 and `sizing.py` judge cost against $140 ($134.00, 95.7 %, $6.00 margin); README budget line; R16 moves from not met to met |
| 5 | Current rating | 40 A continuous | Wording only: CGD-PRB-001 v0.4, CGD-PRC-001 v0.4 |
| 6 | Switching side | High-side N-channel switching | Wording only: CGD-PRC-001 v0.4 |
| 7 | Chemistry scope | LFP and NMC-capable hardware, LFP firmware first | Wording only; still needs the SwapCell project's agreement (cross-repo action in `docs/REVIEW.md`) |
| 8 | CAN message set | SwapCell interface v0.3 message set as a CellGuard profile | Wording only; still needs the SwapCell project's agreement (cross-repo action) |
| 10 | Apache-2.0 firmware in an MIT repo | Reused files keep Apache-2.0 and their notices in `firmware/third_party/` and are listed in `LICENSE-SOFTWARE` | Note added to `LICENSE-SOFTWARE` and to the README licenses section; CGD-PRC-001 v0.4 choice 3; CGD-REQ-001 v0.4 R15. No firmware is written (TRL 4, on hold) |
| 14a | Protection settings | SCD 100 mV at 15 µs, OCD2 40 mV at 20 ms, OCD1 24 mV at 320 ms, OCC 12 mV | CGD-CAL-001 v0.2 Table 2 marked decided; CGD-REQ-001 v0.4 R3 cites them as defaults |
| 14b | MOSFET package | Top-side cooled TOLT package | `bom/bom.csv` line 4 spec (TOLL no longer listed; price unchanged at $2.50); CGD-PRC-001 v0.4 Table 1; README key components. The model already represents the packages as blocks of the same size, so the geometry, STEP, STL and drawing CGD-DWG-001 are unchanged (stays Rev P1) |
| 14c | Precharge switch | DPAK-class P-channel MOSFET | `bom/bom.csv` line 7 note; CGD-PRC-001 v0.4 Table 1 (already the specified part) |
| 14d | Current calibration | One-point gain calibration at build | CGD-REQ-001 v0.4 R9; CGD-CAL-001 v0.2 section 6. Decided but on hold: the build and calibration are TRL 4 work |
| 15 (R16 part) | Response to R16 | The recommended $140 budget | Covered by item 4 |

## Items still open

*Table 2. Items without a recommendation: Proposed, awaiting Amish.*

| # (DDR-001) | Item | Status |
| --- | --- | --- |
| 9 | First test partner (solar installer, e-bike repair shop or makerspace) | Proposed, awaiting Amish. No preference stated |
| 12 | Cover material: printed flame-retardant polycarbonate or sheet aluminium | Proposed, awaiting Amish. No recommendation was made |
| 13 | Low-cost method to check the state-of-charge estimate | Proposed, awaiting Amish. No recommendation was made |
| 15 (R6) | Board loss 4.44 W against 4 W: 1.5 mΩ-class MOSFETs or the SCP fuse moved off the board | Proposed, awaiting Amish. No option was recommended |
| 15 (R8) | State of charge on 20 Ah packs: restate R8 for 50 Ah and larger, a full-charge prompt, or a 0.5 mΩ shunt | Proposed, awaiting Amish. No option was recommended |
| 15 (R14) | Mass 0.646 kg against 0.6 kg: a 3 mm plate (0.581 kg) or relax the target to 0.65 kg | Proposed, awaiting Amish. No option was recommended |

## Consequences

- Requirement status on paper moves from 9 met, 4 not met and 3 at risk to 10 met, 3 not met (R6, R8, R14) and 3 at risk (R2, R4, R7).
- `budget_usd` is $140. The $134.00 BOM leaves a $6.00 margin, which the unconfirmed SCP fuse price (line 14) could use up.
- Specifying the TOLT package fixes the thermal result at 53.7 °C junction at 40 A; the TOLL fallback figure (61.4 °C, 97.7 °C bound at 80 A for 10 s) is kept in CGD-CAL-001 for reference only.
- Items 7 and 8 still depend on the SwapCell project, and MotionCore must run its CAN bus at 250 kbit/s to share the profile. These are listed as cross-repo actions in `docs/REVIEW.md`; no other repo was edited.
- The one-point calibration and all firmware are TRL 4 work and remain on hold by Amish's instruction. `trl` and `trl_target` stay at 3.
