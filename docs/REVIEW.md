# Review note: CellGuard

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CGD-PRB-001 v0.2): problem with cited fire statistics and regulation, prior work (foxBMS, diyBMS, Libre Solar BMS), users and context, constraints, out of scope, open questions.
- `docs/03-requirements.md` (CGD-REQ-001 v0.2): 16 measurable requirements (R1 to R16) with targets, a status table and assumptions.
- `docs/02-concept.md` (CGD-PRC-001 v0.2): how it works, 14 numbered components, seven key design choices, first-order numbers with assumptions, state-of-charge method, safety, open questions.
- `cad/src/concept_media.py`: massing model of the board assembly (base plate, PCB, front end, MOSFET bank, shunt, microcontroller, precharge, fuse, studs, balance harness, temperature sensors, connector, cover) on posts above a 4S pack of 280 Ah LFP cells for scale.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with BOM callouts 1 to 13, `cutaway.png`, `flow.png` (power path losses at 40 A, estimates), `model.glb` and `viewer.html`.
- `bom/bom.csv`: 16 lines with indicative prices, lines 1 to 13 matching the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; concept rationale, burning platform, industry and region tables and origin expanded with cited sources; concept, key components and safety brought in line with the precis.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Cell range | 4 to 16 LFP cells (12.8 to 51.2 V nominal, 58.4 V maximum) | R1 met by design |
| Board power path loss at 40 A | about 3.2 W (about 4.2 W with hot MOSFETs) | R6 met, thin margin |
| MOSFET junction at 40 A, 40 °C ambient | about 52 °C | R5 met on estimate |
| Balancing time for 1 % imbalance | 10 h on 100 Ah; 28 h on 280 Ah | R7 met to 100 Ah only |
| Precharge of 2 mF to 90 % | about 0.46 s | R13 met |
| Sleep current | about 100 µA | R10 met on estimate |
| Prospective short circuit | about 1 to 8 kA depending on pack | Fuse breaking capacity 10 kA or more |
| Size and mass | about 220 x 110 x 32 mm, about 0.5 kg | R14 met |
| Parts cost | about $124 | **R16 not met, about 3 % over** |

Requirements not met or at risk:

- **R4 (single-fault safety) not met:** the front end protects independently of the microcontroller, but a shorted charge MOSFET or a failed front end leaves only the charger's voltage limit. An independent secondary protector would close this.
- **R16 (cost) not met:** about $124 against $120; about $134 with a secondary protector.
- **R7 not met for 280 Ah cells:** 100 mA passive balancing is slow on large storage cells.
- **R2 at risk:** the front end's cell voltage accuracy is a typical figure; the worst case over temperature is unchecked.
- **R8 at risk:** state-of-charge drift on small packs that rarely reach full charge (about 4 % of a 20 Ah pack in 7 days, estimate).
- **R6 at risk when hot:** about 4.2 W against a 4 W target.

### Proposed, awaiting Amish

1. **Front end.** Options: TI BQ76952 class (3 to 16 cells, autonomous protection), ADI daisy-chain monitor, Renesas ISL94202 (8 cells maximum). Recommendation: BQ76952 class.
2. **Microcontroller and firmware base.** Options: (A) STM32G0B1 class building on the Libre Solar BMS firmware (Apache-2.0), (B) ESP32-C6 class with wireless, (C) new firmware. Recommendation: A, with a decision on how Apache-2.0 code sits in this MIT-licensed repo.
3. **Secondary protector (safety trade-off).** Add a BQ77216-class independent protector driving a self-control protector fuse, about $10, to meet R4. Recommendation: add.
4. **Budget.** `budget_usd` is unchanged at $120. Options: (a) raise to $140 to cover the secondary protector and margin; (b) keep $120 and drop to 6 MOSFETs and a 30 A rating; (c) keep $120 and count power cables as pack parts. Recommendation: (a).
5. **Current rating.** 40 A continuous first; a 100 A variant later if storage users need it. Recommendation: 40 A.
6. **High-side switching** to keep a common ground for CAN. Recommendation: high side.
7. **Chemistry scope.** Add an NMC profile so CellGuard can serve as SwapCell's 13S BMS, or keep LFP only as the pitch states. Recommendation: design the hardware for both, release LFP firmware first; needs agreement with the SwapCell project. The pitch is unchanged.
8. **CAN message set.** Adopt the SwapCell interface message set as a CellGuard profile. Recommendation: adopt, subject to the SwapCell project.
9. **First test partner** (solar installer, e-bike repair shop or makerspace).

`project.yaml` was not changed: pitch and problem remain accurate.

### Safety concerns

- Very high prospective short-circuit current (about 1 to 8 kA, estimate): DC-rated fuse with 10 kA breaking capacity, insulated tools, covered terminals.
- Sense lead connection order and loose leads can cause false readings and overcharge; first tests on a cell simulator or bench supply only.
- No independent second protection layer yet (R4).
- Voltage spike when the MOSFETs open under load: TVS diode across the output.
- Precharge resistor overheating into a shorted load: 1 s firmware timeout.
- Not certified; research and prototype use only. Must not be presented as meeting UL 2271, AIS-156 or similar.

### Problems and notes

- The hero render shows a 4S pack for scale; the board supports 16S, which is stated in the key figures. Main power cables between pack and studs are not modeled.
- FieldNode uses a single LFP cell, below CellGuard's 4S minimum; it needs its own one-cell protector. No sibling README currently names CellGuard as a dependency.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 3 and 4. If approved, run `/advance-trl3` to check the loss, thermal, balancing, short-circuit and state-of-charge estimates by calculation, write the protection threshold table and failure mode analysis, and produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Done under Amish's 2026-09-25 instruction for this batch ("you know the drill, nothing gets past TRL 3"). He has not reviewed the CellGuard TRL 2 items one by one, so the recommendations are adopted for TRL 3 work, open for his review. TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CGD-DDR-001 v0.1): items 1 to 3 and 5 to 8 adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review; the budget and seven other items left open.
- `docs/04-calcs/01-sizing.md` (CGD-CAL-001 v0.1) and `docs/04-calcs/sizing.py`, which prints every quoted number and writes `docs/04-calcs/results.csv`: voltage range, power path loss and thermal, protection thresholds, short circuit, single-fault table, balancing, current and state-of-charge error budget, quiescent current, CAN load and log, precharge, size and mass, cost.
- `cad/src/model.py`: parametric build123d model (14 parts, key dimensions in `PARAMS`, clash check clean) exporting `cad/step/` and `cad/stl/` for the assembly, base plate and cover. `cad/src/concept_media.py` now builds from it.
- `cad/src/sheets.py` and `cad/drawings/CGD-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps its number CGD-DWG-010, so DWG-001 was free.
- `bom/bom.csv`: 17 lines, all priced, with supplier types; new line 14 for the secondary protector and SCP fuse. `bom/bom-notes.md` updated.
- Docs bumped to v0.3 with revision rows: CGD-PRB-001, CGD-PRC-001, CGD-REQ-001 (R1 adds the NMC profile, R11 the SwapCell v0.3 message set at 250 kbit/s; status table from CAL-001).
- `media/`: all concept media regenerated from the model; every image checked. Flow diagram now shows the SCP fuse loss. Temporary `media/_views*` folders removed.
- `README.md`: TRL badge, links to the drawing and calculations, concept numbers, key components and safety brought in line with CAL-001. Pitch and problem lines unchanged (no rewording was recommended).
- `project.yaml`: `trl: 3`, `trl_target: 3`, evidence listed. `budget_usd` unchanged at 120.

### Requirements (CGD-CAL-001)

9 met on paper, 4 not met, 3 at risk.

| ID | Result | Status |
| --- | --- | --- |
| R6 | 4.44 W board loss at 40 A (0.64 W is the SCP fuse); 3.80 W without it | **Not met** |
| R8 | 10.1 points after 7 days on a 20 Ah pack with a calibrated offset (32.3 uncalibrated); 7.4 on 100 Ah | **Not met** on small packs |
| R14 | 220 x 110 x 32 mm; 0.646 kg against 0.6 kg | **Not met** (mass) |
| R16 | $134.00: 11.7 % over $120; $6.00 under the recommended $140 | **Not met** against $120 |
| R2 | ±15 mV guaranteed over temperature; only typical under 10 mV at 25 °C | At risk |
| R4 | Every single fault ends safe with BQ77216 and SCP fuse; SCP rating for 40 A at 60 V unconfirmed | At risk |
| R7 | 103 mA, 9.7 h for 1 % on 100 Ah; resistor hotspot 73.9 °C against 70 °C | At risk |
| R1, R3, R5, R9 to R13, R15 | See CAL-001 Table 4 (junction 53.7 °C at 40 A; sleep 54.5 µA; CAN load 1.84 %; precharge 0.46 s) | Met on paper |

Corrections to TRL 2 figures: board loss was about 3.2 W (now 4.44 W with the SCP fuse and warm MOSFETs); sleep about 100 µA (now 54.5 µA, the charge pump was double counted); prospective short circuit 1 to 8 kA (now 0.7 to 4.7 kA with cables and board resistance); mass about 0.5 kg (now 0.646 kg); cost $124 (now $134 with the protector).

### Decisions recorded (CGD-DDR-001)

Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: BQ76952-class front end; STM32G0B1 with the Libre Solar firmware base; BQ77216-class secondary protector with SCP fuse; 40 A rating; high-side switching; LFP plus NMC-capable hardware with LFP firmware first; SwapCell v0.3 CAN message set as a profile.

### Still awaiting Amish

1. Budget: raise `budget_usd` to $140 (recommended); unchanged at $120 meanwhile.
2. First test partner (no preference stated).
3. Licensing of Apache-2.0 firmware code in the MIT repo.
4. Cover material (no recommendation).
5. Low-cost method to check the state-of-charge estimate (no recommendation).
6. TRL 3 engineering proposals: protection thresholds (SCD 100 mV at 15 µs, OCD2 40 mV at 20 ms, OCD1 24 mV at 320 ms, OCC 12 mV), top-cooled MOSFETs, DPAK-class precharge switch, one-point current calibration.
7. Responses to R6, R8, R14 and R16 (options in CAL-001 section 12: 1.5 mΩ MOSFETs or moving the SCP fuse off the board; restating R8 for 50 Ah and larger packs, a full-charge prompt or a 0.5 mΩ shunt; a 3 mm plate at 0.581 kg; the $140 budget).

### Cross-repo notes

- SwapCell (interface v0.3): CAN at 250 kbit/s, 11-bit identifiers and 32-byte log records are consistent. As SwapCell's BMS, CellGuard would need the INTERLOCK wake input; sleep then rises to 84.5 µA, inside SwapCell's 100 µA limit. SwapCell's BMS spec says 30 A continuous FETs, which CellGuard's 40 A covers. The SwapCell project has not yet agreed to either profile.
- MotionCore plans to read CellGuard faults over CAN; its bus must run at 250 kbit/s to share the SwapCell profile. No conflict recorded yet, but VESC-class controllers often default to 500 kbit/s, so MotionCore should state its rate.
- FieldNode, CrossSafe and TwinKit do not use CellGuard at this stage; no interface conflict.

### Safety concerns

- Prospective short-circuit current up to about 4.7 kA (16S 280 Ah); fuse 60 A, DC 80 V or more, 10 kA breaking capacity.
- SCD delay must be the 15 µs minimum; at 60 µs a large pack reaches about 2.5 kA and 3.2 J of loop energy before the MOSFETs open. TVS and MOSFET avalanche energy must be checked against about 1 J.
- The SCP fuse is one-shot and not yet sourced at 40 A and 60 V; until it is, use chargers with a fixed, correct end-of-charge voltage.
- Precharge switch sees a 34 W peak; a small SOT-23 MOSFET would fail.
- Not certified; research and prototype use only.

### Problems and notes

- Citations: none were flagged as unchecked. The TI BQ76952 and BQ77216 figures used in CAL-001 were checked with WebFetch on the TI product pages and the BQ76952 data sheet. WebSearch is exhausted.
- Assumed values without a data sheet: SCP fuse resistance, MOSFET package thermal resistances, buck and CAN quiescent currents, loop inductance. They are listed in CAL-001 Table 1.
- The kit's cutaway cuts near the origin; the model is centered close to the origin, so the section passes through the PCB, MOSFETs and studs as intended.
- No TRL 4 material exists in the repo (`build-log/` holds only its README).

### Recommended next step

Review CGD-DDR-001 and decide the budget and the responses to R6, R8, R14 and R16. TRL 4 is on hold by Amish's instruction. When it is released, TRL 4 would need: data sheets for the SCP fuse, MOSFETs, TVS and buck; a schematic and board layout; a bench build on a cell simulator; and a lab test report (TST) of protection trips, losses, balancing and sleep current, with build-log entries.
