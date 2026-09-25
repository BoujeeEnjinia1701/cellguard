---
doc_id: CGD-REQ-001
title: CellGuard requirements
project: CellGuard
doc_type: Requirements
version: "0.2"
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
---

# CellGuard requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs. They will be checked by calculation at TRL 3 and revised after the lab projects that depend on CellGuard confirm their needs. Status in Table 2 is judged against the estimates in CGD-PRC-001.

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Cover the lab's LFP packs with one board | 4 to 16 LFP cells in series (12.8 to 51.2 V nominal, 58.4 V maximum), cell count set in a configuration file | Design review against the front-end data sheet |
| R2 | Measure every cell voltage accurately | ±10 mV at 25 °C and ±15 mV from −20 to 60 °C, each cell at least every 100 ms | Data sheet review; later comparison with a calibrated meter |
| R3 | Protect the pack from abuse | Cell overvoltage (default 3.65 V), cell undervoltage (default 2.50 V), charge overcurrent, discharge overcurrent, short-circuit trip within 500 µs, over-temperature, charge lockout below 0 °C; all thresholds in the configuration file | Protection table review; later fault injection on a cell simulator |
| R4 | Stay safe after a single fault | No single failure (microcontroller crash, stuck-on MOSFET, open sense wire, failed sensor) leaves the pack able to be overcharged or over-discharged | Failure mode and effects analysis |
| R5 | Carry the lab's load currents | 40 A continuous and 80 A for 10 s at 40 °C ambient, MOSFET junction at 110 °C or less | Thermal calculation; later bench test |
| R6 | Waste little power in the power path | 4 W or less on the board at 40 A (MOSFETs, shunt and copper), excluding the external fuse | Loss calculation from data sheets |
| R7 | Balance cells | Passive balancing at 100 mA or more per cell; corrects a 1 % capacity imbalance in 24 h of balancing time on packs up to 100 Ah; board stays at 70 °C or less while balancing | Balance power and time calculation |
| R8 | Give a state of charge the user can trust | Documented method; error within ±5 percentage points after a full charge, within ±10 points after 7 days of partial cycling without a full charge | Algorithm note; later cycling test against a lab reference |
| R9 | Measure current | ±1 % of reading ±50 mA from −80 to +80 A | Shunt and front-end error budget |
| R10 | Draw little from an idle pack | 300 µA or less in sleep with outputs on and CAN able to wake; 10 µA or less in ship mode | Quiescent current budget from data sheets |
| R11 | Talk to host devices openly | CAN 2.0B at 250 or 500 kbit/s with a published message set; 3.3 V UART at 115,200 baud for logs and configuration; an enable input that keeps the output off until the host is connected | Interface specification review |
| R12 | Keep a state-of-health log | At least 2,000 charge and discharge event records in non-volatile memory, exportable as CSV; fields sufficient for EU Batteries Regulation state-of-health data | Log format review |
| R13 | Precharge the load | Charge up to 2 mF of load capacitance to 90 % of pack voltage within 1 s before closing the discharge path | Precharge calculation |
| R14 | Be small and light | 230 x 120 x 40 mm or smaller, 0.6 kg or less without power cables | Massing model; later weighing |
| R15 | Be buildable and open | No BGA or leadless parts finer than 0.5 mm pitch; assembly with a hot plate or hot-air station; hardware CERN-OHL-S-2.0, firmware MIT | Design review of the parts list |
| R16 | Stay within the concept budget | $120 or less in parts at quantity one, excluding cells | Priced BOM |

Table 2. Status at TRL 2 (estimates).

| ID | Status | Basis |
| --- | --- | --- |
| R1 | Met by design | Front end rated for 3 to 16 series cells |
| R2 | **At risk** | The front end's data sheet gives better than 10 mV as a typical figure; the worst case over temperature is not yet checked |
| R3 | Met by design | Front-end protections plus firmware thresholds; trip times to be confirmed at TRL 3 |
| R4 | **Not met** | The front end protects independently of the microcontroller, but a shorted charge MOSFET or a failed front end leaves no second layer except the charger's own voltage limit. Closing this needs an independent secondary protector (proposed, awaiting Amish) |
| R5 | Met on estimate, unverified | About 2.0 W in the MOSFETs at 40 A at 25 °C, about 3 W when hot; heat spread into the base plate |
| R6 | Met on estimate, thin margin | About 3.2 W at 40 A (about 4.2 W with hot MOSFETs, which would miss R6) |
| R7 | Met up to 100 Ah; **not met** for 280 Ah cells | 1 Ah at 100 mA takes 10 h; 2.8 Ah on a 280 Ah cell takes 28 h |
| R8 | **At risk** | Depends on coulomb counter offset and how often the pack reaches full charge; unverified |
| R9 | Unverified | Error budget not yet done |
| R10 | Met on estimate | About 100 µA in sleep (estimate from typical data sheet figures) |
| R11 to R13 | Met by design | See CGD-PRC-001 |
| R14 | Met | Massing model about 220 x 110 x 32 mm, about 0.5 kg (estimate) |
| R15 | Met by design | Front end and microcontroller in 0.5 mm pitch quad flat packages |
| R16 | **Not met** | About $124, about 3 % over budget; about $134 with a secondary protector |

## Assumptions

- LFP cell limits are typical defaults (3.65 V maximum and 2.50 V minimum per cell; charge 0 to 45 °C; discharge −20 to 60 °C). Every build must take its limits from the actual cell data sheet.
- Reference packs: 4S 280 Ah (12.8 V, about 3.6 kWh) for storage and 16S 20 Ah (51.2 V, about 1 kWh) for vehicles.
- The 40 A rating covers a 400 W inverter on a 12.8 V pack (about 31 A) and a 30 A vehicle controller. Larger loads need a larger board or a contactor, which is out of scope.
- Prices are indicative single-unit prices from distributors in September 2026 and will change.
