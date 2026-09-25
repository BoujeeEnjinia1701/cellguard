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
