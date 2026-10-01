---
doc_id: CGD-PRB-001
title: CellGuard problem statement
project: CellGuard
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-10-01'
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
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Chemistry scope and current rating adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review (CGD-DDR-001); budget note
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-30'
  author: Amish Chadha
  change: Design for construction (CGD-DDR-003); figures follow CGD-CAL-001 v0.3
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
---

# CellGuard problem statement

Small builders of lithium iron phosphate (LiFePO4, LFP) packs have no open, documented battery management system (BMS) they can read, check and repair, so they either trust a closed board with unknown limits or leave the pack unprotected. Both routes end in damaged packs and, in the worst case, fires.

## The problem

A BMS keeps every cell of a pack inside its voltage, current and temperature limits, balances the cells so that the weakest one does not set the pack's capacity, and reports how much charge is left. It is the main safety layer of any lithium pack. The US Consumer Product Safety Commission's 2026 proposed safety standard for micromobility batteries puts it plainly: to keep each cell within its specifications during charge and discharge, "a robustly designed micromobility product electrical system uses a BMS" ([CPSC notice of proposed rulemaking, Federal Register, 24 June 2026](https://www.federalregister.gov/documents/2026/06/24/2026-12749/safety-standard-for-lithium-ion-batteries-used-in-micromobility-products-and-electrical-systems-of)).

The consequences of weak or missing protection are visible in fire statistics:

- The same CPSC notice counts 227 micromobility battery incidents from 2019 to 2023 in the United States, associated with 39 deaths and 181 injuries ([Federal Register](https://www.federalregister.gov/documents/2026/06/24/2026-12749/safety-standard-for-lithium-ion-batteries-used-in-micromobility-products-and-electrical-systems-of)).
- New York City recorded 268 lithium-ion battery fires and 18 deaths in 2023, and 277 fires and 6 deaths in 2024 ([FDNY, March 2025](https://www.nyc.gov/site/fdny/news/03-25/fdny-commissioner-robert-s-tucker-significant-progress-the-battle-against-lithium-ion)).
- London Fire Brigade attended 206 e-bike and e-scooter fires in 2025, a record, up from 171 in 2024 ([London Fire Brigade, January 2026](https://www.london-fire.gov.uk/news/2026-news/january/record-number-of-e-bike-and-e-scooter-fires-across-london-in-2025-as-brigade-calls-for-regulation-to-be-introduced)).

Most of these fires involve lithium-ion chemistries other than LFP, and many involve poor chargers, damage or modified packs rather than a BMS fault alone. The point for this project is narrower: builders who make their own packs, which is common in the lab's vehicles, storage and field kits, need a protection board whose thresholds, firmware and failure behavior are published and testable.

What builders can buy today falls into three groups:

1. **Low-cost closed boards.** Widely sold 4S to 16S boards are cheap, but their firmware, thresholds, accuracy and failure modes are undocumented, and their state-of-charge figures cannot be checked.
2. **Open research platforms.** [foxBMS](https://foxbms.org/) from Fraunhofer IISB is open and aimed at functional safety, but it is a large, multi-board platform for vehicle-scale packs rather than a single garage-buildable board.
3. **Open small-pack projects.** [diyBMS](https://github.com/stuartpittaway/diyBMSv4) uses one small module per cell with a separate controller, and the [Libre Solar BMS 8S50 IC](https://libre.solar/hardware/bms-8s50-ic.html) covers 3 to 8 LFP cells with CAN and [open firmware](https://github.com/LibreSolar/bms-firmware). Neither covers 4 to 16 cells on one board with a documented state-of-charge method and a log that other lab projects can rely on.

LFP adds a specific difficulty: its open-circuit voltage is almost flat over most of the charge range, so the cell voltage says little about state of charge and simple voltage-based gauges mislead the user ([Applied Energy, 2025, on state-of-charge estimation in the LFP voltage plateau](https://www.sciencedirect.com/science/article/abs/pii/S0306261925014850)).

Regulation is moving toward the BMS as a source of record. The EU Batteries Regulation requires batteries for light means of transport, stationary storage and electric vehicles to hold data for determining state of health and expected lifetime in their BMS, applicable from 18 August 2024 ([Regulation (EU) 2023/1542](https://eur-lex.europa.eu/eli/reg/2023/1542/oj/eng); [summary, Crowell and Moring](https://www.crowell.com/en/insights/client-alerts/the-eu-batteries-regulation-taking-stock-of-the-new-eu-battery-requirements)). India amended its traction battery standard AIS-156 with added requirements on cells, the BMS and thermal propagation after fires in electric two-wheelers, effective 1 October 2022 ([Press Information Bureau, Government of India](https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=1856114&reg=3&lang=2)).

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Lab projects (SwapCell, PowerBox, SunSpoke, MotionCore) | One protection layer with known limits and a documented interface, instead of a new BMS in each design | 12.8 to 51.2 V LFP packs, 20 to 280 Ah |
| Small pack builders and makers | A board they can build, configure for their cell count and check against a bench test | Garages, makerspaces, small workshops |
| Off-grid and backup storage users | A protected 12, 24 or 48 V battery bank whose state of charge they can trust | Solar home systems, clinics, shops, telecom sites |
| Repair shops and technicians | Readable fault codes, logs and thresholds so a pack can be diagnosed rather than scrapped | E-bike and solar repair |
| Educators and students | A complete, readable reference design for teaching battery safety | Vocational training, university labs |

Operating context assumed for the concept: LFP prismatic or cylindrical cells in 4S to 16S (12.8 to 51.2 V nominal, up to 58.4 V at 3.65 V per cell), continuous currents up to 40 A, ambient temperature from −20 to 50 °C (−4 to 122 °F), indoors or inside a vehicle or enclosure, not immersed.

## Constraints

- Garage-buildable prototype with a value-engineering target of about $140 USD in parts (`project.yaml`, a hypothetical control target, not a limit), excluding cells, raised from $120 by Amish on 2026-09-25 (CGD-DDR-002). CGD-CAL-001 v0.3 prices the board at $138 with the secondary protector and the parts added to make it buildable (CGD-DDR-003).
- One board design covers 4 to 16 series cells, set by configuration, not by different boards.
- Parts that a small workshop can solder: no ball grid arrays, no leadless packages finer than 0.5 mm pitch, assembly with a hot plate or hot-air station.
- Maximum pack voltage below 60 V DC, so the design stays in the extra-low-voltage range.
- Open hardware (CERN-OHL-S-2.0) and open firmware (MIT); every threshold readable and changeable in a plain configuration file.
- Research, educational and prototype use. CellGuard is not a certified BMS and does not replace a certified one where a product must meet a standard such as UL 2271 or AIS-156.

## Out of scope

- Firmware for chemistries other than LFP in the first release. The hardware also supports an NMC profile of up to 14 cells, so it could serve as SwapCell's 13S BMS (decided by Amish, 2026-09-25, subject to the SwapCell project).
- Single-cell and 2S to 3S packs, such as FieldNode's single LFP cell, which need a simpler one-cell protector.
- Packs above 16S or above 60 V, and currents above 40 A continuous.
- Active (energy-transferring) balancing.
- Certification testing.

## Open questions

- NMC profile for SwapCell's 13S pack: decided by Amish, 2026-09-25: go with recommendation (hardware for both, LFP firmware first). The SwapCell project's agreement is still needed.
- Current rating: 40 A continuous, decided by Amish, 2026-09-25: go with recommendation; a 100 A variant only if storage users need it.
- Which partner should supply real packs and use cases for first testing (a solar installer, an e-bike repair shop or a makerspace)? Proposed, awaiting Amish.
