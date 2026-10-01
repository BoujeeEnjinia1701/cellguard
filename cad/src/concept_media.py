"""CellGuard concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the board (power end at +X, signal end at -X), Y across, Z up. Units mm.
Geometry comes from cad/src/model.py, so the media match the STEP files and drawing
CGD-DWG-001. Flow values are printed by docs/04-calcs/sizing.py (CGD-CAL-001).
For scale the hero render shows the board on four posts above a 4S LiFePO4 pack of
280 Ah prismatic cells (173.9 x 71.7 x 207.2 mm each, EVE LF280K class).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Cylinder, Pos
from concept import Part, render_all
from model import PARAMS, build_parts


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def rod(x, y, z0, z1, r):
    """Vertical cylinder from z0 to z1."""
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


PACK_TOP = -25.0                # top face of the cells in the hero context
parts = [Part(n, shape, colour, bom, ex) for n, shape, colour, bom, ex in build_parts()]

# Context for scale: a 4S LiFePO4 pack of 280 Ah prismatic cells under the board
CELL_X, CELL_Y, CELL_Z = 71.7, 173.9, 207.2
PX = 25.0                                        # pack centre in X
cx = [PX + (i - 1.5) * CELL_X for i in range(4)]
cells = None
for x in cx:
    c = box(x - CELL_X / 2 + 0.6, x + CELL_X / 2 - 0.6, -CELL_Y / 2, CELL_Y / 2, PACK_TOP - CELL_Z, PACK_TOP)
    for y in (-60, 60):
        c = c + box(x - 10, x + 10, y - 10, y + 10, PACK_TOP, PACK_TOP + 6)
    cells = c if cells is None else cells + c
for (i, y) in ((0, 60), (1, -60), (2, 60)):      # series busbars
    cells = cells + box(cx[i] - 10, cx[i + 1] + 10, y - 10, y + 10, PACK_TOP + 6, PACK_TOP + 9)
posts = None
for x, y in PARAMS["mount_holes"]:                # pack posts under the plate's four tapped mounting holes
    p = rod(x, y, PACK_TOP, 0, 5.0)
    posts = p if posts is None else posts + p
# cell tap leads lying on the cell tops, from the harness to each series node
taps = [(cx[0], -60), ((cx[0] + cx[1]) / 2, 60), ((cx[1] + cx[2]) / 2, -60),
        ((cx[2] + cx[3]) / 2, 60), (cx[3], -60)]
leads = None
for k, (tx, ty) in enumerate(taps):
    y0 = -16 + 8 * k
    seg = box(-95, tx + 1, y0 - 1, y0 + 1, PACK_TOP, PACK_TOP + 2)
    ya, yb = sorted((y0, ty - 10 if ty > 0 else ty + 10))
    seg = seg + box(tx - 1, tx + 1, ya - 1, yb + 1, PACK_TOP, PACK_TOP + 2 + 0.3 * k)
    leads = seg if leads is None else leads + seg
context = [Part("4S LiFePO4 pack (4 x 280 Ah cells)", cells, "#C8CDD3"),
           Part("mounting posts and cell tap leads", posts + leads, "#8A9099")]

render_all(
    parts, project="CellGuard", title="Battery management board concept", dwg_no="CGD-DWG-010", date="2026-09-30",
    key_figures=["4 to 16 LiFePO4 cells in series (12.8 to 58.4 V)",
                 "40 A continuous, 80 A for 10 s; FET junction 54 °C (calc.)",
                 "Board loss 4.4 W at 40 A, R6 target 4 W (calc., not met)",
                 "Independent secondary protector and SCP fuse (R4)",
                 "CAN 2.0B 250 kbit/s, SwapCell v0.3 message set; UART",
                 "220 x 110 x 33 mm, 0.67 kg; $138 in parts (est.)"],
    scale_figure=False, context=context,
    flow={"title": "power path, 16S pack discharging at 40 A (estimates, CGD-CAL-001)", "unit": "W (est.)",
          "stages": [("Cells, 16S at 51.2 V", 2048.0), ("Fuse and links", 2046.4),
                     ("SCP fuse", 2045.8), ("MOSFET switches", 2043.4),
                     ("Shunt and PCB copper", 2042.0), ("Load at P+ and P-", 2042.0)],
          "losses": [(1, "Fuse and links", 1.6), (2, "SCP fuse", 0.6),
                     (3, "MOSFETs", 2.4), (4, "Shunt and copper", 1.4)]},
)
