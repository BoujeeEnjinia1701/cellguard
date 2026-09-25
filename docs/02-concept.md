---
doc_id: CGD-PRC-001
title: CellGuard design precis
project: CellGuard
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, first-order numbers, safety, media)
---

# CellGuard design precis

## Summary

CellGuard is one open battery management board for LFP packs of 4 to 16 cells in series. A single cell-monitor and protection chip measures every cell, trips the pack's MOSFET switches on its own when a limit is crossed, and balances the cells; a small microcontroller adds the state-of-charge estimate, a state-of-health log and an open CAN and UART interface. Everything sits on an aluminium base plate that spreads heat and also carries the pack fuse, so the whole protection path is one part that other lab projects can bolt on. At TRL 2 the concept meets most of its requirements on estimates, but it misses the $120 budget by about 3 % and has no independent second protection layer (R4 and R16 in CGD-REQ-001).

![CellGuard on a 4S LFP pack](../media/hero.png)

*Figure 1. CellGuard on four posts above a 4S LFP pack of 280 Ah prismatic cells, shown for scale. Concept, not for fabrication.*

## How it works

1. **Measure.** The front end (BOM 3) reads every cell voltage through the balance harness (10), pack current through a 0.25 mΩ shunt (5) and three temperatures (11): two cell probes and one thermistor beside the MOSFETs.
2. **Protect.** The front end compares each reading with thresholds loaded from the configuration file at startup. If a cell goes above 3.65 V it opens the charge MOSFETs; below 2.50 V it opens the discharge MOSFETs; on overcurrent, short circuit or temperature faults it opens both (4). This happens in the front end's own hardware, so a firmware crash in the microcontroller does not stop protection.
3. **Balance.** When the pack is near full and cells differ by more than a set amount (default 10 mV), the front end bleeds up to 100 mA from the higher cells through external balance resistors.
4. **Connect safely.** The discharge path stays off until the host pulls the enable line. The precharge switch and resistor (7) first charge the host's input capacitors, then the main discharge MOSFETs close. The pack fuse (8) is the last line of defense against a short circuit that the MOSFETs cannot clear.
5. **Estimate and report.** The microcontroller (6) counts charge in and out, corrects the count at full charge and near empty, logs every charge and discharge event to flash and publishes status on CAN and UART (12).

![Power path and losses](../media/flow.png)

*Figure 2. Power path for a 16S pack discharging at 40 A. All values are estimates.*

## Main components

Table 1. Main components. Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| BOM | Component | Concept choice | Notes |
| --- | --- | --- | --- |
| 1 | Base plate and heat spreader | 6061 aluminium, 220 x 110 x 4 mm, with PCB standoffs | Takes MOSFET heat through a thermal pad; carries the fuse |
| 2 | Main PCB | 4-layer, 2 oz (70 µm) copper, 150 x 95 mm | Power copper on inner layers; clearances for 60 V |
| 3 | Cell monitor and protection IC | TI [BQ76952](https://www.ti.com/product/BQ76952) class: 3 to 16 cells, cell voltage error under 10 mV typical, integrated high-side N-channel MOSFET driver, coulomb counter, I²C | Proposed, awaiting Amish (alternatives in Key design choices) |
| 4 | Charge and discharge MOSFETs | 8 x 100 V N-channel, about 2.5 mΩ, TOLL package: 4 in parallel for charge, 4 for discharge, back to back | Mounted on the PCB underside, pressed onto the base plate |
| 5 | Current shunt | 0.25 mΩ metal element, 3 W, low side between B- and P- | 10 mV at 40 A |
| 6 | Microcontroller and CAN transceiver | STM32G0B1 class with built-in CAN controller, plus a 3.3 V CAN transceiver | Runs state of charge, log and interface; not in the protection path |
| 7 | Precharge | 100 Ω 10 W aluminium-housed resistor with a P-channel MOSFET, driven by the front end's precharge output | 1 s timeout in firmware |
| 8 | Pack fuse and holder | 60 A, DC rated 80 V or more, breaking capacity 10 kA or more | In the B+ lead, bolted to the base plate |
| 9 | Power terminals | Four M6 studs: B+, B-, P+, P- | Pack side (B) and load or charger side (P) |
| 10 | Balance connector and harness | 17-way connector, 16 sense leads plus B- reference, each lead fused or resistor-protected at the cell end | Unused inputs linked on the board for packs under 16S |
| 11 | Temperature sensors | Three 10 kΩ NTC thermistors: two ring-lug probes on cells, one on the board by the MOSFETs | Charge locked out below 0 °C |
| 12 | CAN and UART connector | Latching 6-way connector: CAN-H, CAN-L, UART TX and RX, enable, ground | Enable keeps the output off until the host is connected |
| 13 | Cover | Flame-retardant polycarbonate (UL 94 V-0 grade), printed or cut and bent | Leaves the studs and fuse reachable |
| 14 | Supporting electronics | 60 V input buck regulator, 16 Mbit SPI flash, TVS diode across P+ and P-, balance resistors, passives | Not shown in the model |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with BOM numbers.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section through the board: MOSFETs (4) under the PCB on the base plate (1), precharge resistor (7), studs (9) and fuse (8), all under or beside the cover (13).*

## Key design choices

Each of these is proposed, awaiting Amish.

1. **One analog front end for 4 to 16 cells.** A single BQ76952-class chip covers the whole cell range on one board and runs protection without the microcontroller. Alternatives: an Analog Devices ADBMS or LTC681x daisy-chain monitor (better for large packs, but needs a separate protection path and more firmware), or a Renesas ISL94202 as on the Libre Solar board (autonomous, but limited to 8 cells). Recommendation: BQ76952 class.
2. **High-side switching.** N-channel MOSFETs in the positive lead keep B- and P- at nearly the same potential, so the CAN and UART ground stays common with the host. Low-side switching is cheaper but breaks the common ground whenever the pack trips. Recommendation: high side.
3. **Microcontroller and firmware base.** Option A: STM32G0B1 class with built-in CAN, building on the open [Libre Solar BMS firmware](https://github.com/LibreSolar/bms-firmware) (Apache-2.0, supports bq769x2 front ends). Option B: ESP32-C6 class with Wi-Fi and Bluetooth for a phone app, at higher idle current. Option C: a new firmware from scratch. Recommendation: A. Apache-2.0 code inside an MIT-licensed repo must keep its own license notices; how to handle that is part of the decision.
4. **40 A continuous rating.** Covers a 30 A vehicle controller and a 400 W inverter on a 12.8 V pack. A 100 A variant would need more MOSFETs, heavier copper and a larger plate. Recommendation: 40 A for the first board.
5. **Passive balancing at 100 mA.** Simple and cheap; adequate for packs up to about 100 Ah. Active balancing is out of scope.
6. **Fuse on the base plate.** Keeps the fuse, switches and sensing together as one tested assembly, at the cost of a longer plate. Recommendation: keep.
7. **CAN message set.** Adopt the SwapCell interface's CAN message set as a CellGuard profile, so SwapCell hosts such as PowerBox and SunSpoke can read a CellGuard pack without changes. Recommendation: adopt, subject to the SwapCell project agreeing.

## First-order numbers

All values are estimates for review and will be checked at TRL 3.

Table 2. First-order estimates.

| Quantity | Estimate | Assumptions |
| --- | --- | --- |
| MOSFET loss at 40 A | about 2.0 W (about 3.0 W hot) | 4 parallel x 2.5 mΩ per direction, two directions in series: 1.25 mΩ; on-resistance about 1.5 times higher at 100 °C |
| Shunt and PCB copper loss at 40 A | about 1.2 W | Shunt 0.25 mΩ (0.4 W); copper and terminals about 0.5 mΩ (0.8 W) |
| Board power path loss at 40 A | about 3.2 W (about 4.2 W hot) | Sum of the two lines above; R6 target 4 W |
| Fuse and busbar loss at 40 A | about 1.6 W | About 1.0 mΩ in the fuse, holder and links |
| Efficiency of the power path, 16S at 40 A | about 99.8 % | 4.8 W of 2,048 W |
| Base plate temperature rise | about 10 K at 40 A continuous | Plate area about 0.048 m², natural convection about 8 W/(m²·K), about 3.2 to 4.2 W |
| MOSFET junction at 40 °C ambient | about 52 °C | Plate rise 10 K plus about 2 K through the case and a 0.5 mm, 3 W/(m·K) pad |
| Peak 80 A for 10 s | about 0.5 K extra plate rise | Losses times four for 10 s into 0.26 kg of aluminium (about 235 J/K) |
| Balancing | 100 mA per cell, about 0.35 W per channel; 8 channels at once about 2.8 W | 33 Ω bleed resistors at 3.3 to 3.6 V |
| Balancing time for 1 % imbalance | 10 h on 100 Ah; 28 h on 280 Ah | R7 met up to 100 Ah only |
| Precharge | 90 % in about 0.46 s; 3.4 J dissipated; 0.58 A peak | 100 Ω into 2 mF at 58.4 V (time constant 0.2 s) |
| Prospective short-circuit current | about 1 kA (16S 20 Ah) to about 8 kA (16S 280 Ah) | Cell internal resistance 0.25 to 3 mΩ, plus busbars and wiring; sets the fuse breaking capacity at 10 kA or more |
| Sleep current | about 100 µA | Front end sleep about 10 µA, microcontroller stop mode about 5 µA, CAN transceiver standby about 10 µA, buck regulator about 25 µA, MOSFET gate charge pump about 40 µA; typical data sheet figures, to be confirmed |
| Self-discharge from sleep current | about 0.07 Ah per month | 0.4 % per month of a 20 Ah pack |
| State-of-charge drift without full charge | about 0.8 Ah in 7 days | 5 mA residual offset after calibration; 4 % of a 20 Ah pack, 0.3 % of 280 Ah; R8 at risk on small packs |
| Log capacity | about 60,000 records | 32-byte event records (the SwapCell record size) in 2 MB of SPI flash; R12 needs 2,000 |
| Size and mass | about 220 x 110 x 32 mm; about 0.5 kg | Plate 0.26 kg, PCB and parts 0.09 kg, cover 0.06 kg, fuse and studs 0.08 kg, connectors 0.04 kg |
| Parts cost | about $124 | `bom/bom.csv`, quantity one, excluding cells; R16 not met by about 3 % |

### State-of-charge method

LFP's flat voltage curve means voltage alone cannot give state of charge in the middle of the range. The concept uses coulomb counting from the front end's integrated coulomb counter, anchored at two points where LFP voltage does change quickly: full (all cells above 3.45 V with charge current tapering below C/20) and near empty (lowest cell below 3.0 V at light load). Between two anchors the firmware learns the usable capacity, which also feeds the state-of-health log. After a rest of two hours or more at the ends of the range, the open-circuit voltage is used as a check. The method, its constants and its error budget will be written up as a calculation note at TRL 3 and published with the firmware.

## Safety

> **Safety:** CellGuard connects directly to lithium cells that can deliver thousands of amperes into a short circuit. Treat every build as live. Use insulated tools, cover exposed terminals and busbars, and fit the pack fuse before connecting any load.

> **Safety:** Connect the balance harness only in the order given by the front-end maker, with the board not yet connected to the power leads, and check every sense lead voltage with a meter first. A wrong or loose sense lead can make the board report a false cell voltage, which can lead to overcharge.

> **Safety:** First power-up and all threshold changes should be tested on a cell simulator or a bench supply with current limiting, not on a full pack. Charge test packs on a non-combustible surface, inside a fire-resistant enclosure where possible, never unattended, with a lithium-rated or Class D extinguisher and sand nearby.

> **Safety:** The MOSFETs cannot always interrupt a hard short from a large pack; the fuse must be sized for the pack's prospective short-circuit current (10 kA or more for large prismatic cells) and rated for DC at 80 V or more. A TVS diode across P+ and P- limits the voltage spike when the MOSFETs open under load.

> **Safety:** With no independent secondary protector in the concept, a single failure (a shorted charge MOSFET or a failed front end) removes overcharge protection, leaving only the charger's own voltage limit (R4 not met). Until a secondary protector is added, use only chargers with a fixed, correct end-of-charge voltage for the pack.

> **Safety:** The precharge resistor would overheat if the load stayed shorted; firmware limits precharge to 1 s and reports a fault.

Maximum pack voltage stays below 60 V DC. CellGuard is a research, educational and prototype design. It is not certified and does not replace a certified BMS where a product must meet a standard.

## Open questions

- [ ] Front end, microcontroller and firmware base (Key design choices 1 and 3). Proposed, awaiting Amish.
- [ ] Add an independent secondary protector (BQ77216 class, 3 to 16 cells, driving a self-control protector fuse), about $10, to meet R4? Proposed, awaiting Amish.
- [ ] Budget: about $124 now, about $134 with a secondary protector, against $120. Proposed, awaiting Amish.
- [ ] NMC profile so that CellGuard can be SwapCell's BMS. Proposed, awaiting Amish and the SwapCell project.
- [ ] Adopt the SwapCell CAN message set as a CellGuard profile. Proposed, awaiting Amish.
- [ ] Cover rating: is a printed flame-retardant cover enough, or should the cover be sheet aluminium?
- [ ] How to test the state-of-charge method without expensive lab equipment (for example, a calibrated shunt and a bench load)?

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html).
