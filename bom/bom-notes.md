# BOM notes

- Line numbers 1 to 14, 17 and 18 match the callouts in `media/exploded.png` and the parts in `cad/src/model.py`. Lines 15 and 16 are not shown in the model. Lines 17 and 18 were changed and added on 2026-09-30 to make the design buildable (CGD-DDR-003).
- Every line is priced. Prices are indicative single-unit prices in USD (September 2026 estimates) and will change. They exclude cells, tools, shipping and taxes.
- Total: $138.00 (checked by `docs/04-calcs/sizing.py`, CGD-CAL-001 section 11). That is $124.00 as at TRL 2, $10.00 for the secondary protector and SCP fuse (line 14), $2.00 more on line 17 (gap pad, spacers, pillars, screws) and $2.00 for the copper fuse link (line 18).
- Against `budget_usd: 140` in `project.yaml` (raised from $120 by Amish on 2026-09-25, CGD-DDR-002) the BOM uses 98.6 % of the budget with a margin of $2.00, so R16 is met. Against the former $120 it would be 15.0 % over.
- Lines 3, 6 and 14 follow the choices decided by Amish on 2026-09-25 (CGD-DDR-001, CGD-DDR-002).
- Line 14: an SCP fuse rated for 40 A continuous at 60 V DC or more is not yet confirmed; the price is an estimate.
- Line 4: a top-side cooled (TOLT) package is specified for the thermal path to the base plate (decided, CGD-DDR-002); 1.5 mΩ-class parts would save about 0.95 W at 40 A (CGD-CAL-001) at a higher price.
