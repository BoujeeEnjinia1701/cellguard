# BOM notes

- Line numbers 1 to 14 match the callouts in `media/exploded.png` and the parts in `cad/src/model.py`. Lines 15 to 17 are not shown in the model.
- Every line is priced. Prices are indicative single-unit prices in USD (September 2026 estimates) and will change. They exclude cells, tools, shipping and taxes.
- Total: $134.00 (checked by `docs/04-calcs/sizing.py`, CGD-CAL-001 section 11). That is $124.00 as at TRL 2 plus $10.00 for the secondary protector and SCP fuse (line 14).
- Against `budget_usd: 120` in `project.yaml` the BOM is 11.7 % over, so R16 is not met. Raising the budget to $140 is recommended and remains proposed, awaiting Amish; against $140 the margin is $6.00.
- Lines 3, 6 and 14 follow the choices adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review (CGD-DDR-001).
- Line 14: an SCP fuse rated for 40 A continuous at 60 V DC or more is not yet confirmed; the price is an estimate.
- Line 4: a top-side cooled (TOLT) package is preferred for the thermal path to the base plate; 1.5 mΩ-class parts would save about 0.95 W at 40 A (CGD-CAL-001) at a higher price.
