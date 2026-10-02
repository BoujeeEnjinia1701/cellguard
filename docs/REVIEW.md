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

Status update: items 1 to 8 are **Decided by Amish, 2026-09-25: go with recommendation** (CGD-DDR-002). Item 9 has no recommendation and stays Proposed, awaiting Amish.

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

Decided by Amish, 2026-09-25: go with recommendation (first recorded here as adopted for TRL 3, open for his review; confirmed in CGD-DDR-002): BQ76952-class front end; STM32G0B1 with the Libre Solar firmware base; BQ77216-class secondary protector with SCP fuse; 40 A rating; high-side switching; LFP plus NMC-capable hardware with LFP firmware first; SwapCell v0.3 CAN message set as a profile.

### Still awaiting Amish

1. Budget: raise `budget_usd` to $140 (recommended). **Decided by Amish, 2026-09-25: go with recommendation**; now $140.
2. First test partner (no preference stated).
3. Licensing of Apache-2.0 firmware code in the MIT repo. **Decided by Amish, 2026-09-25: go with recommendation** (separate `firmware/third_party/` folder, listed in `LICENSE-SOFTWARE`).
4. Cover material (no recommendation).
5. Low-cost method to check the state-of-charge estimate (no recommendation).
6. TRL 3 engineering proposals: protection thresholds (SCD 100 mV at 15 µs, OCD2 40 mV at 20 ms, OCD1 24 mV at 320 ms, OCC 12 mV), top-cooled MOSFETs, DPAK-class precharge switch, one-point current calibration. **Decided by Amish, 2026-09-25: go with recommendation.**
7. Responses to R6, R8, R14 and R16. R16: **decided** through the $140 budget. R6, R8, R14: no option recommended, still Proposed, awaiting Amish (options in CAL-001 section 12: 1.5 mΩ MOSFETs or moving the SCP fuse off the board; restating R8 for 50 Ah and larger packs, a full-charge prompt or a 0.5 mΩ shunt; a 3 mm plate at 0.581 kg; the $140 budget).

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

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (CGD-DDR-002 v0.1). CGD-DDR-001 moves to v0.2 with the same wording.

### Decisions applied and what changed

| Item | Before | After |
| --- | --- | --- |
| Budget (DDR-001 items 4 and 11) | `budget_usd: 120`; BOM $134.00, 11.7 % over; R16 not met | `budget_usd: 140`; BOM $134.00, 95.7 % of budget, $6.00 margin; R16 met |
| Protection settings (item 14) | Engineering proposal, awaiting Amish | Decided: SCD 100 mV at 15 µs (400 A), OCD2 40 mV at 20 ms (160 A), OCD1 24 mV at 320 ms (96 A), OCC 12 mV (48 A); cited in R3 |
| MOSFET package (item 14) | TOLT preferred, TOLL acceptable | TOLT specified in `bom/bom.csv` line 4 (price unchanged); junction 53.7 °C at 40 A |
| Precharge switch (item 14) | DPAK class proposed | DPAK class decided (already in BOM line 7) |
| Current calibration (item 14) | Proposed build step | Decided build step in R9; the build is TRL 4, on hold |
| Firmware licensing (item 10) | Suggested, awaiting Amish | Decided: reused Apache-2.0 files in `firmware/third_party/` with their notices, listed in `LICENSE-SOFTWARE` (note added; no firmware yet) |
| Items 1 to 3 and 5 to 8 | Adopted for TRL 3, open for review | Decided; wording updated in PRB, PRC, REQ, CAL, BOM notes and README |

No decision changed the geometry, so `cad/src/model.py`, the STEP and STL files and CGD-DWG-001 keep Rev P1; all were regenerated for the domain change. Documents bumped: CGD-PRB-001 0.3 to 0.4, CGD-PRC-001 0.3 to 0.4, CGD-REQ-001 0.3 to 0.4, CGD-CAL-001 0.1 to 0.2, CGD-DDR-001 0.1 to 0.2; CGD-DDR-002 v0.1 is new. `sizing.py` now judges cost against $140 and still prints the former $120 comparison. The pitch and problem lines are unchanged (no rewording was recommended).

The README's "What sparked the idea" now traces the idea to the July 2016 CPSC recall of about 501,000 hoverboards with overheating lithium-ion packs; the earlier text about a portfolio review was removed. All generated files were re-rendered so they show designmolecule.com.

### Requirement status (CGD-CAL-001 v0.2)

10 met on paper, 3 not met, 3 at risk.

| ID | Result | Status |
| --- | --- | --- |
| R6 | 4.44 W board loss at 40 A (3.80 W without the SCP fuse) | **Not met** |
| R8 | 10.1 points after 7 days on 20 Ah (calibrated offset); 7.4 on 100 Ah | **Not met** on small packs |
| R14 | 0.646 kg against 0.6 kg | **Not met** (mass) |
| R2 | ±15 mV guaranteed over temperature; only typical at 25 °C | At risk |
| R4 | Every single fault ends safe; SCP fuse at 40 A and 60 V unconfirmed | At risk |
| R7 | Resistor hotspot 73.9 °C against 70 °C | At risk |
| R16 | $134.00 against $140 | Met (was not met against $120) |
| R1, R3, R5, R9 to R13, R15 | As in CAL-001 Table 4 | Met on paper |

### Still awaiting Amish

1. First test partner (no preference stated).
2. Cover material (no recommendation).
3. Low-cost method to check the state-of-charge estimate (no recommendation).
4. Response to R6 board loss (options listed, none recommended).
5. Response to R8 state of charge on small packs (options listed, none recommended).
6. Response to R14 mass (options listed, none recommended).

### Cross-repo actions

- SwapCell: agree to CellGuard's NMC profile (13S) and the SwapCell v0.3 CAN message set as a CellGuard profile; if CellGuard is SwapCell's BMS, SwapCell's INTERLOCK wake input must be carried (sleep 84.5 µA, inside SwapCell's 100 µA limit). Decided on the CellGuard side; SwapCell not edited.
- MotionCore: state its CAN bit rate and run at 250 kbit/s to share the profile. Not edited.
- FieldNode: needs its own one-cell protector, as CellGuard starts at 4S. Not edited.

### TRL

`trl: 3` and `trl_target: 3` are unchanged. TRL 4 remains on hold by Amish's instruction: the one-point calibration, firmware, schematic, board layout, bench build and tests are decided or planned but not started.


## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; it changes no design value, document, BOM line or drawing.

### What was added

- `cad/src/product_model.py`: `product_parts()` (61 parts: 17 shell, 19 internal, 2 accessory, 23 context), `TITLE` and `RENDER_VIEWS` (hero, exploded and a detail view without the pack). Every main dimension and interface comes from `PARAMS` and `build_parts()` in `cad/src/model.py`.
- Board and enclosure: a clear polycarbonate cover with filleted edges, four fixing screws in bosses, a teal name plate and a warning label; the aluminium base plate with filleted corners and four counterbored mounting holes; brass M6 studs with washers, nuts and thread detail; a bolted 60 A fuse in a dark holder with blades, studs and nuts.
- Populated board, illustrative only (no layout): the model.py chips, shunt and connectors, a finned aluminium-housed precharge resistor, 16 balance resistors, buck, flash, TVS, sleeved capacitors, silkscreen marks and three status lights (green lit), plus the thermal pad and the eight MOSFETs under the board.
- Latching mating plugs on the balance and CAN connectors (accessory).
- Context: an illustrative compact 4S LiFePO4 pack (four prismatic cells about 27 x 148 x 97 mm, not from a data sheet) with busbars, terminal nuts, end plates, woven straps and a label; five balance leads in a braided sleeve, two ring-lug temperature probes, B- and B+ power cables with the fuse link and heat-shrink boots, a CAN cable and a small bench mat.
- `README.md`: hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. Both files are produced later by the render step; they are not in the repo yet.

### Differences from model.py (each Proposed, awaiting Amish)

1. **Cover shown clear.** model.py and the existing media show the cover as dark grey; the BOM says flame-retardant polycarbonate, and the cover material is already an open item. The render uses clear polycarbonate so the board reads through it. Recommendation: adopt a clear UL 94 V-0 polycarbonate cover, since it lets a user see the status lights and board state without opening it; confirm that a clear V-0 grade is available before TRL 4.
2. **Pack beside the board, not under it.** concept_media.py shows the board on posts above a 4S pack of 280 Ah cells. The product render puts a compact illustrative 4S pack beside the board, so the balance harness tail and the two probe leads are rerouted to reach it; the 17-way connector, probe count and exits are unchanged. Recommendation: keep the model.py layout for engineering media and use the beside layout for product renders only.
3. **Cover fixings.** model.py has no cover fixings. The render adds four screws into bosses that stop above the board. Recommendation: accept as an appearance placeholder; the real fixing method belongs with the cover material decision.
4. **Status lights.** The concept does not name any indicator. The render adds three board LEDs (green lit) under BOM line 15. Recommendation: adopt one tri-colour status light as a low-cost aid to fault finding; it would add a few cents to BOM line 15.
5. **Power cables and fuse link drawn.** BOM line 16 cables are not in model.py. The render shows the pack B+ lead to the fuse, a fuse link to the B+ stud and the B- lead to its stud; the fuse holder is split into a holder, blades, studs and nuts inside the model.py fuse envelope. Recommendation: accept; no dimension changes.

### Scope

This is an appearance model only: no tolerances, no PCB layout and no fabrication detail. `trl` and `trl_target` stay at 3, and TRL 4 remains on hold by Amish's instruction.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: design for construction and the prototype build plan (kit 1.7.0)

Done under Amish's 2026-09-30 instruction to bring every repo to the approved build plan format, with outstanding decisions kept in a separate register, and to "fix the design assumptions to match and be physically feasible". TRL stays 3.

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` matches `.kit/CLAUDE.md`.
- `cad/src/model.py`: constructable design; `build_components()` and `checks()` added; `python cad/src/model.py --check` runs 46 constructability checks (overlaps, contacts, clearances, gap pad squeeze, link height, assembly order). All pass.
- `docs/decisions/0003-design-for-construction.md` (CGD-DDR-003 v0.1, Draft): every change below, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (CGD-BLD-001 v0.1) and `docs/06-design-decisions.md` (CGD-DEC-001 v0.1), both in `trl_evidence`; `design_state: constructable` in `project.yaml`.
- `cad/src/build_plan_media.py`: overview, 5 making sketches (CGD-DWG-101 to 105), plate hole layout, 6 joint close-ups, 10 assembly step pictures and a connections diagram, in `docs/05-build-plan/` and `cad/drawings/`. Every picture was looked at and fixed where cluttered.
- `cad/drawings/CGD-DWG-001` Rev P2; STEP and STL regenerated (assembly, base plate, cover and the new fuse link); concept media regenerated, including `media/model.glb`.
- `bom/bom.csv`: line 17 repriced ($5.00 to $7.00) and respecified; new line 18, copper fuse link ($2.00); lines 8 and 9 specify the holder and stud dimensions the design relies on. Total $138.00.
- Calculations re-run: CGD-CAL-001 v0.3; CGD-PRC-001, CGD-REQ-001 and CGD-PRB-001 to v0.5; README figures, links line and "Building the prototype" section.
- `cad/src/product_model.py` reads the new spacer positions so it still runs; its appearance details are otherwise unchanged.

### Design changes made for construction (CGD-DDR-003)

1. Board supports: flat plate, six bought 3 mm spacers and six M3 countersunk screws from below, in place of standoffs drawn as part of the plate with no fixing.
2. Gap under the switches: 3.0 mm, with a 1.0 mm gap pad squeezed to 0.7 mm, in place of a 0.5 mm pad with no squeeze.
3. Cover: carried on four 20 mm pillars and held by four M3 screws; connector and probe openings made into notches open at the bottom; walls 0.5 mm clear of the plate.
4. Board fixings at the power end moved to the corners (71.5, ±43.5 mm) to clear the B+ stud and the protector fuse; two fixings added at (48, ±44 mm) for the cover pillars.
5. Fuse holder moved in line with the B+ stud, fixed by four M4 screws; a straight 14 x 3 mm copper link joins it to the B+ stud at matching heights.
6. Power studs specified as soldered through-hole terminals with an M6 stud and 13 mm shoulder.
7. Four M4 tapped mounting holes in the plate (screws from below); hero picture pack posts moved to them.
8. CAN and UART connector moved so its face is flush with the cover, 5 mm past the board edge (was 9 mm).

### Key results (CGD-CAL-001 v0.3)

- No requirement changed status: 10 met on paper, 3 not met (R6 4.44 W against 4 W; R8 on 20 Ah packs; R14 0.664 kg against 0.6 kg, worse than the 0.646 kg before), 3 at risk (R2, R4, R7).
- Hottest switch junction 54.0 °C at 40 A (was 53.7 °C); 99.1 °C bound at 80 A for 10 s with TOLL (was 97.7 °C).
- Envelope 220 x 110 x 33 mm; estimated parts cost $138.00, $2.00 under the $140 value-engineering target (was $6.00 under).

### Proposed, awaiting Amish

All open items are in the register CGD-DEC-001: accept CGD-DDR-003 (recommended); cover material and colour; responses to R6, R8 and R14; state-of-charge test method; first test partner; the render-session items (status light, pack layout in renders, cover fixing and cables in renders); SwapCell agreement.

### Safety concerns

- The gap pad is the only insulation between the live switch tops and the aluminium plate; it must be rated for at least 100 V and replaced if nicked. The build plan adds an insulation check (S1).
- The copper link and stud shoulders are live at pack potential outside the cover; the link is sleeved and the plan requires boots on the studs before anything is connected.
- Unchanged: up to about 4.7 kA prospective short circuit; 15 µs short-circuit delay; protector fuse rating unconfirmed (R4 at risk).

### Stale media (made on Amish's Mac, not regenerated here)

`media/render-hero.png`, `media/render-exploded.png` and `media/render-detail.png` (referenced by the README, not in this copy), `media/card.png` and `media/social-preview.png` show the concept plate, fuse position and cover fixings. They need regenerating from `cad/src/product_model.py`, which should also adopt the fuse position, copper link and pillar cover fixing.

### Recommended next step

Amish to review CGD-DDR-003 and the register. TRL 4 (board layout, bench build on a cell simulator, first checks) remains on hold by his instruction.

## 2026-10-02: open decisions decided

Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." The recommendations written for this repo's open decisions are recorded as decided.

### Decisions recorded

12 decisions, moved from "Open decisions" to "Decisions made" in the register (CGD-DEC-001 v0.3): design for construction P1 to P8 accepted (CGD-DDR-003, A1); printed flame-retardant polycarbonate cover; opaque prototype cover with a light pipe; 1.5 mΩ-class switches for R6; a full-charge prompt after about five days with R8 restated; R14 relaxed to 0.7 kg; the 4S 20 Ah state-of-charge check; a small off-grid solar installer that builds 16S LFP packs as the first candidate test partner; a three-colour status light; pack beside the board in product renders only; cover fixing and cables kept in renders; SwapCell agreement recorded there once the board envelope question is settled.

### Documents changed

- `docs/06-design-decisions.md`: CGD-DEC-001 v0.3
- `docs/decisions/0001-trl2-review-decisions.md`: CGD-DDR-001 v0.3
- `docs/decisions/0002-recommendations-accepted.md`: CGD-DDR-002 v0.2
- `docs/decisions/0003-design-for-construction.md`: CGD-DDR-003 v0.3 (accepted; status kept Draft)
- `docs/01-problem.md`: CGD-PRB-001 v0.7 (first test partner)
- `docs/02-concept.md`: CGD-PRC-001 v0.7 (key numbers and open questions)
- `docs/03-requirements.md`: CGD-REQ-001 v0.7 (R8 restated, R14 relaxed, status)
- `docs/04-calcs/01-sizing.md`: CGD-CAL-001 v0.5 (requirement table and summary; no calculation re-run)
- `docs/05-build-plan.md`: CGD-BLD-001 v0.2 (mass check against 0.7 kg)
- `README.md` and `bom/bom-notes.md` (not controlled)

### Follow-up actions to carry approved decisions into the design

1. Decision 3: add the light pipe over the status light to the cover in the model, the cover making sketch CGD-DWG-104 and the build plan pictures; state "opaque" in BOM line 13 (model, drawings, pictures, BOM).
2. Decision 4: respecify BOM line 4 as 1.5 mΩ-class TOLT switches and reprice it (BOM).
3. Decision 4: re-run `docs/04-calcs/sizing.py` for the 1.5 mΩ-class switches (board loss, junction temperatures) and update R6 status (calculations).
4. Decision 5: re-run the state-of-charge error for about five days between prompted full charges and update R8 status; the firmware prompt is TRL 4 work (calculations).
5. Decision 7: write the 4S 20 Ah partial-cycling check into the TRL 4 test plan when TRL 4 is opened (docs).
6. Decision 8: approach a small off-grid solar installer that builds 16S LFP packs as the first candidate test partner (docs).
7. Decision 9: add the three-colour status light to BOM line 15 (specification and price) and to the board in the model (BOM, model).
8. Decision 10: regenerate the product renders on Amish's Mac with the pack beside the board (pictures).
9. Decision 11: regenerate the product renders with the four cover pillars and the cables of CGD-DDR-003 (pictures).
10. Decision 12: once the board envelope question is settled, record the agreement to the NMC profile and the v0.3 CAN message set in the SwapCell repo (docs).

### Points found in the review

- SwapCell expects a battery management board about 230 x 58 mm and 10 mm or less thick (SwapCell register, 'To confirm' item 3), and prices it at $120; CellGuard is 220 x 110 x 33 mm and $138. Item 12 cannot be closed as stated until one side changes.
- Option (b) for R6 does not compare like with like: it reduces the counted board loss by redefining the boundary, not by reducing heat.
- The value-engineering margin is $2, and the protector fuse price is still unconfirmed (DDR-003 A2); fitting 1.5 milliohm switches (item 4) will likely put the board over the $140 target.
- The register listed 'decision 4 is (a)' under 'To confirm' item 8 for a clear sheet, but the clear cover is decision 3, not 4. Corrected in CGD-DEC-001 v0.3.
