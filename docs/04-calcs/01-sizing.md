---
doc_id: CGD-CAL-001
title: CellGuard sizing calculations
project: CellGuard
doc_type: Calculation note
version: "0.6"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (voltage range, power path loss and thermal, protection thresholds, short circuit, single-fault analysis, balancing, current and state of charge, quiescent current, CAN and log, precharge, size and mass, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-30'
  author: Amish Chadha
  change: Design for construction (CGD-DDR-003). Gap pad 1.0 mm compressed to 0.7 mm; mass adds the spacers, pillars, screws and copper fuse link; cost adds BOM line 18 and reprices line 17
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Requirement table: R14 relaxed to 0.7 kg and met on paper; R6 and R8 responses decided (CGD-DEC-001); no calculation re-run"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Re-run for the 2026-10-02 decisions: 1.5 mOhm-class switches (R6 now met on paper, R5 junctions lower, short-circuit currents slightly higher); state-of-charge error over five days between prompted full charges (R8 now met on paper with calibration); status light and light pipe in mass and cost; cost USD 159.15, over the value-engineering target"
---

# CellGuard sizing calculations

On paper, CellGuard meets 12 of its 16 requirements and none is failed outright. This version is re-run for the responses Amish decided on 2026-10-02 (CGD-DEC-001). With 1.5 mΩ-class switches the board loses about 3.5 W at 40 A, so **R6 is now met** (it was 4.4 W against 4 W). With the firmware prompting for a full charge after about five days, the state-of-charge error on a 20 Ah pack reaches 8.7 points between prompted full charges against the restated ±10 points, so **R8 is now met on paper**, provided the coulomb counter offset is calibrated at build. R14 was relaxed to 0.7 kg, and the board's 0.664 kg meets it. The estimated parts cost is $159.15: value-engineering target USD 140.00, estimated cost of the constructable design USD 159.15 (USD 19.15 over the target), mainly because the 1.5 mΩ-class switches cost about twice as much as the 2.5 mΩ parts (R16 is reported against the target, not as a failure). Three are **at risk**: cell voltage accuracy at 25 °C (R2), single-fault safety until a suitable protector fuse is confirmed (R4) and the balance resistor hotspot (R7). Two TRL 2 figures were optimistic and are corrected here: sleep current is about 55 µA, not 100 µA, and the prospective short-circuit current is about 0.7 to 5.0 kA, not 1 to 8 kA, once cables and the board are counted.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads part volumes and the envelope from `cad/src/model.py` and costs from `bom/bom.csv`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. Data sheet values were checked on TI's BQ76952 and BQ77216 product pages and the BQ76952 data sheet on 2026-09-25; all other values are assumptions.*

| Input | Value | Basis |
| --- | --- | --- |
| Cell limits (LFP) | 3.65 V maximum, 3.20 V nominal, 2.50 V minimum | Typical LFP data; each build uses its own cell data sheet |
| Reference packs | 16S 20 Ah (3 mΩ cells, 0.3 mΩ links) and 4S or 16S 280 Ah (0.25 mΩ cells, 0.1 mΩ busbars) | CGD-REQ-001 assumptions |
| Load | 40 A continuous, 80 A for 10 s, 40 °C ambient | R5 |
| MOSFETs | 1.5 mΩ class at 25 °C (decided 2026-10-02, CGD-DEC-001; 2.5 mΩ before), +0.67 % per K, 4 in parallel per direction, hottest carries 10 % more than its share | BOM line 4 |
| Shunt | 0.25 mΩ, 1 %, 50 ppm/K | BOM line 5 |
| SCP fuse | 0.40 mΩ | Assumed; no data sheet chosen yet |
| Main fuse, holder and links | 1.0 mΩ | Assumed |
| PCB power copper | 4 layers of 70 µm copper in parallel; positive path 60 mm by 25 mm, negative path 90 mm by 25 mm; 0.05 mΩ per stud joint; 50 °C copper | From the model layout |
| Heat transfer | Plate 8 W/(m²·K) on both faces; PCB under the cover 6 W/(m²·K); half of the PCB copper, shunt and SCP loss reaches the plate | Natural convection plus radiation, still air |
| Package to plate | Top-cooled TOLT 0.5 K/W, or TOLL through the mold 20 K/W; gap pad 1.0 mm compressed to 0.7 mm between the MOSFETs and the plate (CGD-DDR-003), 3 W/(m·K), 1 cm² per FET | Assumed typical values |
| Front end (BQ76952) | 3 to 16 cells; total cell voltage error ±15 mV from −40 to 85 °C, under 10 mV typical; SCD 10 to 500 mV, 15 to 450 µs; OCD 4 to 200 mV, 10 to 425 ms; OCC 4 to 124 mV; SLEEP 41 µA typical with DSG on; SHUTDOWN 1 µA; coulomb counter offset ±1 LSB uncalibrated, under 1 µV typical; gain 130,845 to 132,335 LSB/V; 100 mA maximum balancing current per cell | [TI BQ76952 product page](https://www.ti.com/product/BQ76952) and [data sheet](https://www.ti.com/lit/ds/symlink/bq76952.pdf) |
| Secondary protector (BQ77216) | 3 to 16 cells; overvoltage, undervoltage, open wire and temperature; separate COUT and DOUT outputs; OV accuracy ±10 mV at 25 °C, ±20 mV from 0 to 60 °C; about 1 µA; TSSOP-24 at 0.65 mm pitch | [TI BQ77216 product page](https://www.ti.com/product/BQ77216) |
| Other quiescent loads | Microcontroller stop mode 5 µA, CAN transceiver standby 10 µA, flash 1 µA (all at 3.3 V); buck 70 % efficient at light load with 10 µA quiescent; TVS leakage 1 µA | Assumed typical values |
| Short-circuit loop | 1 µH loop inductance; 10 µs MOSFET turn-off after the trip | Assumed |
| CAN | 250 kbit/s, 135 bits worst-case frame; SwapCell interface v0.3 message rates | SWC-PRC-001 v0.3 |
| State of charge | Anchor detection 2 points; learned capacity 2 %; residual gain error 0.5 % after one-point calibration; 0.5 equivalent full cycles a day (3.5 in 7 days); the firmware prompts for a full charge after 5 days without one (CGD-DEC-001) | Assumed; prompt interval decided 2026-10-02 |

## 2. Voltage range (R1)

A 4S to 16S LFP pack spans 12.8 to 51.2 V nominal and reaches 58.4 V at full charge, below the 60 V ceiling. The 100 V MOSFETs have a margin of 1.71 times at 58.4 V. An NMC profile fits up to 14 cells under 60 V; SwapCell's 13S pack reaches 54.6 V. R1 is met by design review.

## 3. Power path loss and thermal (R5, R6)

**Loss (R6).** With the 1.5 mΩ-class switches decided on 2026-10-02, the MOSFETs lose 1.20 W at 40 A with cold junctions and 1.41 W at the converged junction temperature. The shunt adds 0.40 W, the PCB copper and stud joints (0.569 mΩ at 20 °C, 0.635 mΩ at 50 °C) 1.02 W, and the SCP fuse 0.64 W. The board loss is **3.47 W, and R6 is met on paper** with 0.53 W to spare; without the SCP fuse it would be 2.83 W. The former 2.5 mΩ parts would lose about 0.94 W more, about 4.4 W in all, which is why R6 was not met at v0.5. The external main fuse adds 1.60 W, so the whole power path loses 5.07 W, 99.75 % efficient for a 16S pack at 40 A. The TRL 2 figure of about 3.2 W left out the secondary protector and the temperature rise of the MOSFETs.

**Thermal (R5).** The base plate (0.0484 m² over both faces) rises 10.4 K at 40 A. The hottest MOSFET dissipates 0.213 W, so its junction reaches **51.0 °C** at 40 °C ambient with a top-cooled TOLT package and 55.4 °C with a TOLL package cooled through its mold. The plate holds 234 J/K and has a time constant of 10.1 min, so a 10 s peak at 80 A adds only 0.60 K to it. The hottest MOSFET then dissipates 0.97 W; bounding its junction by the steady-state value gives 54.4 °C (TOLT) or 77.6 °C (TOLL). Both are under the 110 °C limit, so **R5 is met**. The TOLL margin was thin with the 2.5 mΩ parts (99.1 °C), so the BOM specifies a top-side cooled TOLT package (decided, CGD-DDR-002).

## 4. Protection thresholds, short circuit and single faults (R3, R4)

**Thresholds (R3).** On the 0.25 mΩ shunt the front end's steps give the settings in Table 2, all inside its ranges. The 40 A continuous and 80 A for 10 s envelope is longer than the front end's longest hardware delay (425 ms), so the microcontroller enforces it with a current and time limit; the hardware trips in Table 2 back it up without the microcontroller.

*Table 2. Protection settings (decided by Amish, 2026-09-25: go with recommendation; CGD-DDR-002).*

| Protection | Setting | Current | Delay |
| --- | --- | --- | --- |
| Short circuit in discharge (SCD) | 100 mV | 400 A | 15 µs |
| Overcurrent in discharge 2 (OCD2) | 40 mV | 160 A | 20 ms |
| Overcurrent in discharge 1 (OCD1) | 24 mV | 96 A | 320 ms |
| Overcurrent in charge (OCC) | 12 mV | 48 A | Front-end default range |
| Cell overvoltage and undervoltage | 3.65 V and 2.50 V (LFP) | | Configuration file |
| Charge lockout | Below 0 °C | | Configuration file |

The smallest SCD step is 40 A, so the scale is coarse but adequate. The short-circuit trip completes within 25 µs, well inside the 500 µs of R3. **R3 is met on paper.**

**Short circuit.** The board and fuse add 2.97 mΩ to the short-circuit loop (3.47 mΩ with the former 2.5 mΩ switches) and the two power cables 1.72 mΩ. The prospective current is 716 A (4S 20 Ah), 891 A (16S 20 Ah), 2,102 A (4S 280 Ah) and 4,976 A (16S 280 Ah), a little higher than at v0.5 because the lower-resistance switches take less out of the loop. The 10 kA breaking capacity of the pack fuse covers all of them. With a 1 µH loop, current is still rising when the MOSFETs open. At a 15 µs SCD delay the 16S 280 Ah pack reaches 1,129 A at turn-off (about 282 A per MOSFET) and leaves 0.64 J of loop energy for the TVS diode and the MOSFETs' avalanche rating. At the front end's longer 60 µs delay the same pack reaches 2,555 A and 3.26 J. **The SCD delay must therefore be set to its 15 µs minimum**, and the TVS diode and MOSFET avalanche energy must be checked against about 1 J when parts are chosen.

**Single faults (R4).** Table 3 is a first failure mode and effects analysis for the faults R4 names.

*Table 3. Single faults with the secondary protector.*

| Single fault | Detected by | Result |
| --- | --- | --- |
| Microcontroller crash | Front end runs protection on its own | Pack stays protected; no state of charge or CAN until reset |
| Charge MOSFET shorted | Front end sees cell overvoltage but cannot open the charge path | BQ77216 COUT blows the SCP fuse; pack permanently disconnected (safe) |
| Discharge MOSFET shorted | Front end sees cell undervoltage but cannot open the discharge path | BQ77216 DOUT blows the SCP fuse; pack disconnected (safe) |
| Front end failed | BQ77216 monitors cells independently | SCP fuse blows on overvoltage or undervoltage |
| Open sense wire | Front end and BQ77216 open-wire detection | Both FETs open; BQ77216 blows the SCP fuse if the front end does not act |
| Failed temperature sensor | Out-of-range reading in the front end | Treated as over-temperature; FETs open |

With the secondary protector, no single fault in Table 3 leaves the pack able to be overcharged or over-discharged. **R4 is met on paper but at risk** until an SCP fuse rated for 40 A continuous at 60 V DC or more is found; if none exists, a DC contactor or a second MOSFET pair driven by the BQ77216 is the fallback.

## 5. Balancing (R7)

The 33 Ω bleed resistors draw 103 mA at 3.40 V and dissipate 0.350 W each; eight non-adjacent channels at once dissipate 2.80 W. A 1 % imbalance takes 1.9 h to correct on a 20 Ah pack, 9.7 h on 100 Ah and 27.2 h on 280 Ah. R7 limits the 24 h target to packs up to 100 Ah, so the 280 Ah figure is a limitation to publish, not a failure. Under the cover the PCB bulk rises 16.4 K, to 56.4 °C at 40 °C ambient, but a balance resistor's own hotspot reaches about 73.9 °C. **R7 is at risk** on the 70 °C limit; spreading the resistors or balancing at most four channels at once would bring it under.

## 6. Current measurement and state of charge (R8, R9)

**Current (R9).** One coulomb counter step is 7.60 µV, 30.4 mA on the shunt; the typical calibrated offset of 1 µV is 4.0 mA. The front end's gain spread is ±0.57 %, which with the 1 % shunt gives 1.57 % uncalibrated, outside R9. A one-point gain calibration at build leaves about 0.5 %, so the error at 80 A is 0.404 A against a 0.850 A limit. **R9 is met on paper with calibration**, which is now a decided build step (CGD-DDR-002); the build itself is TRL 4 work, on hold.

**State of charge (R8).** After a full charge the error is 5.0 points (2 for anchor detection, 2 for the learned capacity, 1 for gain over one cycle), which just meets the ±5 point target. On 2026-10-02 Amish decided that the firmware prompts for a full charge when about five days pass without one, and restated R8's partial-cycling clause to apply between prompted full charges (CGD-DEC-001). Over five days of partial cycling the error on the 20 Ah reference pack grows to **8.7 points with a calibrated offset**, against the ±10 point target, so **R8 is met on paper with calibration**; it is 6.7 points on 100 Ah and 6.4 points on 280 Ah. Without offset calibration the 20 Ah figure is 24.5 points, so the result depends on calibrating the coulomb counter offset at build. Over five days the offset may be up to 6.2 mA (about 1.5 µV across the shunt) for 10 points on 20 Ah; the calibrated figure assumed here, 4.0 mA, is TI's typical value, not a guaranteed one, and is to be checked in the 4S 20 Ah state-of-charge test decided on 2026-10-02. For comparison, 7 days without a full charge would give 10.1 points on 20 Ah (32.3 uncalibrated), 7.4 on 100 Ah and 7.0 on 280 Ah; the 0.5 mΩ shunt that would have halved the offset is not fitted.

## 7. Quiescent current (R10)

Sleep draws 54.5 µA: the front end 41.0 µA with the discharge FETs held on, the 3.3 V loads through the buck 1.5 µA, the buck itself 10.0 µA, the secondary protector 1.0 µA and TVS leakage 1.0 µA. That is 0.20 % per month of a 20 Ah pack. Ship mode draws 6.0 µA. **R10 is met on estimate.** With SwapCell's INTERLOCK loop (30 µA) a CellGuard used as SwapCell's BMS draws 84.5 µA, inside SwapCell's 100 µA limit. The TRL 2 estimate of about 100 µA double counted the charge pump, which the front end's SLEEP figure already includes.

## 8. Interface and log (R11, R12)

The SwapCell v0.3 message set adds up to 34.1 frames per second between pack and host, a bus load of 1.84 % at 250 kbit/s. **R11 is met by design.** At 32 bytes per record, the 2 MiB flash holds 65,536 records; 2,000 records need 64,000 bytes. **R12 is met.**

## 9. Precharge (R13)

A 100 Ω resistor into 2 mF has a time constant of 0.20 s and reaches 90 % of 58.4 V in 0.46 s, dissipating 3.38 J. Peak current is 0.584 A and peak power 34.1 W, so the precharge switch needs a DPAK-class P-channel MOSFET whose safe operating area covers 35 W for about 0.2 s. Into a shorted load the 1 s timeout limits the energy to 34.1 J. **R13 is met.**

## 10. Size and mass (R14)

The model envelope is 220 x 110 x 33 mm (to the cover screw heads), inside 230 x 120 x 40 mm. The mass, from model volumes and stated densities plus assumed masses for bought parts, is **0.664 kg, and R14 is met on paper** against the 0.7 kg target Amish set on 2026-10-02 (relaxed from 0.6 kg, CGD-DEC-001). The status light and light pipe added on 2026-10-02 weigh well under 1 g together, and the 1.5 mΩ-class switches are in the same package as before, so the total is unchanged. Version 0.3 adds the parts that make the design buildable (CGD-DDR-003): the gap pad, spacers, pillars, screws and nuts (25 g) and the copper fuse link (12 g). The fuse and holder stay at the concept figure of 89 g until the holder is chosen, although the holder is now drawn smaller. The base plate is the largest item at 260 g; the 4 mm plate is kept (decided 2026-10-02), although a 3 mm plate would bring the total to 0.599 kg. The TRL 2 estimate of about 0.5 kg left out the studs' hardware and underestimated the fuse holder.

## 11. Cost (R16)

The BOM has 19 lines, all priced, and totals **$159.15**: $124.00 as at TRL 2, $10.00 for the secondary protector, $2.00 more for the gap pad, spacers, pillars and screws (line 17) and $2.00 for the copper fuse link (line 18, CGD-DDR-003), then, for the decisions of 2026-10-02 (CGD-DEC-001), $20.00 more for the eight 1.5 mΩ-class switches (line 4, $5.00 each in place of $2.50), $0.35 for the three-colour status light (line 15) and $0.80 for the light pipe (new line 19). Value-engineering target: USD 140.00 (`budget_usd: 140` in `project.yaml`, a hypothetical control target, not a limit, set by Amish on 2026-09-25, CGD-DDR-002). Estimated cost of the constructable design: USD 159.15 (USD 19.15 over the target), 113.7 % of it, so **R16 is over the value-engineering target by $19.15**; the unconfirmed SCP fuse price is still to come. Against the former $120 target it would be 32.6 % over.

## 12. Results

*Table 4. Requirement status at TRL 3 (over target and at risk first).*

| ID | Calculated value | Target | Status |
| --- | --- | --- | --- |
| R16 | $159.15; 113.7 % of target | $140 value-engineering target (raised from $120, CGD-DDR-002) | Over the value-engineering target by $19.15 |
| R2 | ±15 mV from −40 to 85 °C; under 10 mV typical at 25 °C | ±10 mV at 25 °C, ±15 mV from −20 to 60 °C | At risk (no guaranteed 25 °C figure) |
| R4 | All single faults in Table 3 end safe with the BQ77216 and SCP fuse | No single fault allows overcharge or over-discharge | At risk (SCP fuse rating unconfirmed) |
| R7 | 103 mA; 9.7 h for 1 % on 100 Ah; PCB 56.4 °C, resistor hotspot 73.9 °C | 100 mA; 24 h; 70 °C | At risk (hotspot) |
| R1 | 12.8 to 58.4 V; 1.71 times MOSFET margin | 4 to 16 LFP cells, under 60 V | Met |
| R3 | Table 2 settings inside front-end ranges; SCD trip within 25 µs | Trip within 500 µs; all thresholds configurable | Met on paper |
| R5 | Junction 51.0 °C (TOLT) or 55.4 °C (TOLL) at 40 A; 77.6 °C bound at 80 A for 10 s (TOLL) | 110 °C or less | Met on paper |
| R6 | 3.47 W board loss at 40 A with 1.5 mΩ-class switches (2.83 W without the SCP fuse; about 4.4 W with the former 2.5 mΩ parts) | 4 W or less | Met on paper (was not met at v0.5) |
| R8 | 5.0 points after a full charge; 8.7 points after 5 days on 20 Ah with a calibrated offset (24.5 uncalibrated); 6.7 on 100 Ah | ±5 points; ±10 points between prompted full charges, about five days (restated, CGD-DEC-001) | Met on paper with calibration (was not met at v0.5) |
| R9 | 0.404 A error at 80 A after calibration; 1.57 % gain error uncalibrated | ±1 % ±50 mA (0.850 A at 80 A) | Met on paper with calibration |
| R10 | 54.5 µA sleep; 6.0 µA ship mode | 300 µA; 10 µA | Met on estimate |
| R11 | 1.84 % bus load at 250 kbit/s; SwapCell v0.3 message set | Published message set on CAN 2.0B, UART, enable | Met by design |
| R12 | 65,536 records of 32 bytes | 2,000 records | Met |
| R13 | 0.46 s to 90 %; 3.38 J | 1 s for 2 mF | Met |
| R14 | 220 x 110 x 33 mm; 0.664 kg | 230 x 120 x 40 mm; 0.7 kg (relaxed from 0.6 kg, CGD-DEC-001) | Met on paper |
| R15 | TQFP-48 at 0.5 mm, TSSOP-24 at 0.65 mm, leaded MOSFET and regulator packages | No BGA; nothing finer than 0.5 mm | Met by design review |

**Responses decided by Amish on 2026-10-02** (CGD-DEC-001): R6, 1.5 mΩ-class switches; R8, a full-charge prompt after about five days, with the target restated to apply between prompted full charges; R14, the target relaxed to 0.7 kg with the 4 mm plate kept. This version (v0.6) is re-run for them: R6, R8 and R14 are now met on paper, and the switches move R16 to $19.15 over the value-engineering target. The options were: R6, choose 1.5 mΩ-class MOSFETs (saves about 0.96 W, bringing the board to about 3.5 W) or mount the SCP fuse beside the main fuse and count it with the external fuse; R8, restate the target for packs of 50 Ah and larger, add a periodic full-charge prompt, or fit a 0.5 mΩ shunt; R14, a 3 mm plate (0.599 kg) or relax the target to 0.65 kg. R16 was closed by the $140 budget (CGD-DDR-002).

## 13. Limits of this note

- Nothing here is measured. Heat transfer coefficients, copper paths, the SCP fuse resistance, loop inductance and the quiescent currents of parts not yet chosen are assumptions.
- Balancing heat and state-of-charge error depend on firmware settings that do not exist yet.
- The TVS diode, MOSFET avalanche energy and SCP fuse need data sheets before TRL 4.

> **Safety:** CellGuard connects directly to lithium cells that can deliver several thousand amperes into a short circuit (about 5.0 kA for a 16S 280 Ah pack by this note). The pack fuse must be DC rated at 80 V or more with a breaking capacity of 10 kA or more, the SCD delay must be set to its 15 µs minimum, and every threshold change must first be tried on a cell simulator or a current-limited bench supply. The secondary protector's SCP fuse is a one-shot device: once blown, the board must be inspected before it is repaired.
