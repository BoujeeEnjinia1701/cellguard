"""CellGuard concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X along the board (power end at +X, signal end at -X), Y across, Z up. Units mm.
The board assembly sits on an aluminium base plate that also carries the pack fuse.
For scale the hero render shows it on four posts above a 4S LiFePO4 pack of
280 Ah prismatic cells (173.9 x 71.7 x 207.2 mm each, EVE LF280K class).
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Sphere, Pos
from concept import Part, render_all


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def rod(x, y, z0, z1, r):
    """Vertical cylinder from z0 to z1."""
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


PLATE_T = 4.0
PCB_Z0, PCB_T = 6.8, 1.6
TOP = PCB_Z0 + PCB_T            # top face of the PCB, 8.4 mm
PACK_TOP = -25.0                # top face of the cells in the hero context
WIRE_Z = 11.0                   # height of probe leads leaving the board

# 1 Aluminium base plate and heat spreader, with four PCB standoffs; carries the fuse at +X
plate = box(-85, 135, -55, 55, 0, PLATE_T)
for sx in (-68, 68):
    for sy in (-40, 40):
        plate = plate + rod(sx, sy, PLATE_T, PCB_Z0, 3.0)

# 2 Main PCB, 4-layer, 2 oz copper
pcb = box(-75, 75, -47.5, 47.5, PCB_Z0, PCB_Z0 + PCB_T)

# 3 Cell monitor and protection front end (BQ76952 class, TQFP-48)
afe = box(-19.5, -10.5, -4.5, 4.5, TOP, TOP + 1.2)

# 4 Charge and discharge MOSFET bank: 2 x 4 TOLL packages under the PCB, on a thermal pad
fets = box(15, 70, -22, 22, PLATE_T, PLATE_T + 0.5)
for x in (22, 36, 50, 63):
    for y in (-14, 14):
        fets = fets + box(x - 5, x + 5, y - 6, y + 6, PLATE_T + 0.5, PCB_Z0)

# 5 Current shunt, 0.25 mOhm metal element
shunt = box(25, 45, -42, -34, TOP, TOP + 3.0)

# 6 Microcontroller with CAN controller, plus CAN transceiver
mcu = box(-48.5, -41.5, 14.5, 21.5, TOP, TOP + 1.4) + box(-60, -55, 28, 32, TOP, TOP + 1.5)

# 7 Precharge: aluminium-housed 100 ohm 10 W resistor and P-channel MOSFET
pre = box(20, 46, 26, 40, TOP, TOP + 7.5) + box(10, 16, 30, 36, TOP, TOP + 2.0)

# 8 Pack fuse (DC rated, 80 V or more) in a bolted holder on the base plate
fuse = box(88, 132, -16, 16, PLATE_T, 28) + box(92, 128, -6, 6, 28, 32)

# 9 Power terminals B-, P-, P+, B+ (M6 studs on the power end of the PCB)
studs = None
for y in (-33, -11, 11, 33):
    s = rod(66, y, TOP, TOP + 6.0, 6.5) + rod(66, y, TOP + 6.0, TOP + 20.0, 3.0)
    studs = s if studs is None else studs + s

# 10 Balance connector (17-pin) and flat lead harness leaving the -X end, dropping to the pack
bal = (box(-74, -65, -24, 20, TOP, TOP + 9.0)
       + box(-97, -74, -20, 16, WIRE_Z, WIRE_Z + 2.0)
       + box(-97, -95, -20, 16, PACK_TOP, WIRE_Z + 2.0))

# 11 Temperature sensing: one thermistor on the board by the MOSFETs, two probes on cells
ntc = box(38, 41, -6, -4, TOP, TOP + 1.5) + box(-40, -30, -46, -40, TOP, TOP + 5.6)
bead_z = PACK_TOP + 2.5
lead1 = (Pos(-36, -63, WIRE_Z) * Box(1.5, 34, 1.5)          # y -46 to -80
         + rod(-36, -80, bead_z, WIRE_Z + 0.75, 0.75) + Pos(-36, -80, bead_z) * Sphere(2.5))
lead2 = (Pos(-32, -54, WIRE_Z) * Box(1.5, 16, 1.5)          # y -46 to -62
         + Pos(4, -62, WIRE_Z) * Box(73.5, 1.5, 1.5)          # x -32 to 40
         + Pos(40, -71, WIRE_Z) * Box(1.5, 19.5, 1.5)         # y -62 to -80
         + rod(40, -80, bead_z, WIRE_Z + 0.75, 0.75) + Pos(40, -80, bead_z) * Sphere(2.5))
ntc = ntc + lead1 + lead2

# 12 CAN and UART connector, reaching through the cover's -X wall
comm = box(-84, -66, 26, 40, TOP, TOP + 7.0)

# 13 Flame-retardant cover over the signal and MOSFET area (power studs and fuse stay reachable)
cover = box(-80, 54, -52, 52, PLATE_T, 30) - box(-78, 52, -50, 50, PLATE_T - 1, 28)
cover = cover - box(-81, -77, -26, 42, TOP - 0.4, TOP + 11.0)         # connector window, -X wall
cover = cover - box(51, 55, -49, 49, PLATE_T - 1, TOP + 1.0)         # PCB and MOSFET pass-through, +X wall
cover = cover - box(-38, -30, -53, -49, TOP + 0.6, TOP + 5.0)        # probe lead exit, -Y wall

parts = [
    Part("Aluminium base plate and heat spreader", plate, "#9CA3AF", 1, (0, 0, -110)),
    Part("Main PCB, 4-layer, 2 oz copper", pcb, "#15803D", 2, (0, 0, 45)),
    Part("Cell monitor and protection IC", afe, "#111827", 3, (0, 0, 95)),
    Part("Charge and discharge MOSFETs (8)", fets, "#374151", 4, (0, 0, -50)),
    Part("Current shunt, 0.25 mOhm", shunt, "#B45309", 5, (0, -40, 95)),
    Part("Microcontroller and CAN transceiver", mcu, "#0F766E", 6, (0, 30, 95)),
    Part("Precharge resistor and switch", pre, "#D4A017", 7, (0, 40, 95)),
    Part("Pack fuse and holder", fuse, "#C2410C", 8, (110, 0, 20)),
    Part("Power terminals (B-, P-, P+, B+)", studs, "#E5E7EB", 9, (40, 0, 95)),
    Part("Balance connector and lead harness", bal, "#1F2937", 10, (-20, 0, -75)),
    Part("Temperature sensors (3)", ntc, "#38BDF8", 11, (0, -80, 85)),
    Part("CAN and UART connector", comm, "#6B7280", 12, (-40, 60, 15)),
    Part("Flame-retardant cover", cover, "#334155", 13, (40, 0, 200)),
]

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
for x in (-78, 128):
    for y in (-35, 35):
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
    parts, project="CellGuard", title="Battery management board concept", dwg_no="CGD-DWG-010",
    key_figures=["4 to 16 LiFePO4 cells in series (12.8 to 51.2 V nominal)",
                 "40 A continuous, 80 A for 10 s (target)",
                 "Power path loss about 3.2 W at 40 A (estimate)",
                 "Passive balancing, 100 mA per cell (target)",
                 "CAN 2.0B and UART, open message set and log",
                 "About 220 x 110 x 32 mm, 0.5 kg; about $124 in parts (est.)"],
    scale_figure=False, context=context,
    flow={"title": "power path, 16S pack discharging at 40 A (all values are estimates)", "unit": "W",
          "stages": [("Cells, 16S at 51.2 V", 2048), ("Fuse and busbars", 2046.4),
                     ("MOSFET switches", 2044.4), ("Shunt and PCB copper", 2043.2),
                     ("Load at P+ and P-", 2043.2)],
          "losses": [(1, "Fuse and busbars (est.)", 1.6), (2, "MOSFETs (est.)", 2.0),
                     (3, "Shunt and copper (est.)", 1.2)]},
)
