---
doc_id: CGD-REQ-001
title: CellGuard requirements
project: CellGuard
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. R1 adds the NMC profile and R11 the SwapCell v0.3 message set (CGD-DDR-001 items 7 and 8, adopted for TRL 3 pending Amish's review); status from CGD-CAL-001
---

# CellGuard requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised after the lab projects that depend on CellGuard confirm their needs. Status in Table 2 is judged against the TRL 3 calculations in CGD-CAL-001. On paper, 9 of 16 are met; R6, R8, R14 and R16 are not met, and R2, R4 and R7 are at risk. Changes in v0.3 follow CGD-DDR-001, whose items are adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review.

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Cover the lab's LFP packs with one board | 4 to 16 LFP cells in series (12.8 to 51.2 V nominal, 58.4 V maximum), cell count set in a configuration file. The hardware also supports an NMC profile up to 14 cells (under 60 V), covering SwapCell's 13S pack; LFP firmware is released first | Design review against the front-end data sheet |
| R2 | Measure every cell voltage accurately | ±10 mV at 25 °C and ±15 mV from −20 to 60 °C, each cell at least every 100 ms | Data sheet review; later comparison with a calibrated meter |
| R3 | Protect the pack from abuse | Cell overvoltage (default 3.65 V), cell undervoltage (default 2.50 V), charge overcurrent, discharge overcurrent, short-circuit trip within 500 µs, over-temperature, charge lockout below 0 °C; all thresholds in the configuration file | Protection table review; later fault injection on a cell simulator |
| R4 | Stay safe after a single fault | No single failure (microcontroller crash, stuck-on MOSFET, open sense wire, failed sensor) leaves the pack able to be overcharged or over-discharged | Failure mode and effects analysis |
| R5 | Carry the lab's load currents | 40 A continuous and 80 A for 10 s at 40 °C ambient, MOSFET junction at 110 °C or less | Thermal calculation; later bench test |
| R6 | Waste little power in the power path | 4 W or less on the board at 40 A (MOSFETs, shunt and copper), excluding the external fuse | Loss calculation from data sheets |
| R7 | Balance cells | Passive balancing at 100 mA or more per cell; corrects a 1 % capacity imbalance in 24 h of balancing time on packs up to 100 Ah; board stays at 70 °C or less while balancing | Balance power and time calculation |
| R8 | Give a state of charge the user can trust | Documented method; error within ±5 percentage points after a full charge, within ±10 points after 7 days of partial cycling without a full charge | Algorithm note; later cycling test against a lab reference |
| R9 | Measure current | ±1 % of reading ±50 mA from −80 to +80 A | Shunt and front-end error budget |
| R10 | Draw little from an idle pack | 300 µA or less in sleep with outputs on and CAN able to wake; 10 µA or less in ship mode | Quiescent current budget from data sheets |
| R11 | Talk to host devices openly | CAN 2.0B at 250 kbit/s carrying the SwapCell interface v0.3 message set as a CellGuard profile (subject to the SwapCell project); 3.3 V UART at 115,200 baud for logs and configuration; an enable input that keeps the output off until the host is connected | Interface specification review |
| R12 | Keep a state-of-health log | At least 2,000 charge and discharge event records in non-volatile memory, exportable as CSV; fields sufficient for EU Batteries Regulation state-of-health data | Log format review |
| R13 | Precharge the load | Charge up to 2 mF of load capacitance to 90 % of pack voltage within 1 s before closing the discharge path | Precharge calculation |
| R14 | Be small and light | 230 x 120 x 40 mm or smaller, 0.6 kg or less without power cables | Massing model; later weighing |
| R15 | Be buildable and open | No BGA or leadless parts finer than 0.5 mm pitch; assembly with a hot plate or hot-air station; hardware CERN-OHL-S-2.0, firmware MIT | Design review of the parts list |
| R16 | Stay within the concept budget | $120 or less in parts at quantity one, excluding cells | Priced BOM |

Table 2. Status at TRL 3 (CGD-CAL-001; calculations, nothing measured).

| ID | Status | Basis |
| --- | --- | --- |
| R6 | **Not met** | 4.44 W on the board at 40 A, of which 0.64 W is the secondary protector's SCP fuse; 3.80 W without it |
| R8 | **Not met** on the 20 Ah reference pack; met on 100 Ah and larger | 5.0 points after a full charge; after 7 days, 10.1 points on 20 Ah with a calibrated offset (32.3 uncalibrated), 7.4 on 100 Ah |
| R14 | **Not met** (mass) | 220 x 110 x 32 mm meets the size; 0.646 kg exceeds 0.6 kg (0.581 kg with a 3 mm plate) |
| R16 | **Not met** against $120 | $134.00 with the secondary protector, 11.7 % over; $6.00 under the recommended $140 (awaiting Amish) |
| R2 | At risk | Total error ±15 mV from −40 to 85 °C meets the range target; at 25 °C the data sheet gives only a typical figure under 10 mV |
| R4 | At risk | With the BQ77216-class secondary protector and SCP fuse every single fault in the failure analysis ends safe; an SCP fuse rated for 40 A at 60 V DC is not yet confirmed |
| R7 | At risk | 103 mA; 9.7 h for 1 % on 100 Ah; PCB 56.4 °C but a balance resistor hotspot about 73.9 °C at 40 °C ambient |
| R1 | Met | 12.8 to 58.4 V; 100 V MOSFETs with 1.71 times margin; front end rated 3 to 16 cells |
| R3 | Met on paper | Thresholds inside the front-end ranges; short-circuit trip within 25 µs |
| R5 | Met on paper | Junction 53.7 °C at 40 A (top-cooled package), 97.7 °C bound at 80 A for 10 s (TOLL) |
| R9 | Met on paper with calibration | 0.404 A error at 80 A after a one-point gain calibration, against 0.850 A |
| R10 | Met on estimate | 54.5 µA in sleep, 6.0 µA in ship mode |
| R11 | Met by design | SwapCell v0.3 message set; 1.84 % bus load at 250 kbit/s |
| R12 | Met | 65,536 records of 32 bytes in 2 MiB |
| R13 | Met | 90 % in 0.46 s; 3.38 J |
| R15 | Met by design review | TQFP-48 at 0.5 mm, TSSOP-24 at 0.65 mm, no BGA |

## Assumptions

- LFP cell limits are typical defaults (3.65 V maximum and 2.50 V minimum per cell; charge 0 to 45 °C; discharge −20 to 60 °C). Every build must take its limits from the actual cell data sheet.
- Reference packs: 4S 280 Ah (12.8 V, about 3.6 kWh) for storage and 16S 20 Ah (51.2 V, about 1 kWh) for vehicles.
- The 40 A rating covers a 400 W inverter on a 12.8 V pack (about 31 A) and a 30 A vehicle controller. Larger loads need a larger board or a contactor, which is out of scope.
- Prices are indicative single-unit prices from distributors in September 2026 and will change.
- `budget_usd` in `project.yaml` stays at $120. Raising it to $140 is recommended and awaits Amish (CGD-DDR-001 item 4); R16 is judged against $120.
