"""CellGuard parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the envelope, a clash
check and the part volumes that CGD-CAL-001 uses for the mass estimate.

Massing-plus detail: correct interfaces (four M6 power studs, the 17-way balance
connector, the 6-way CAN and UART connector, the fuse on the base plate, the MOSFET
bank on the thermal pad) and main dimensions; not fabrication detail.

Axes: X along the board (power end at +X, signal end at -X), Y across, Z up. Units mm.
The base plate bottom face is z = 0.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 Base plate and heat spreader (6061 aluminium)
    "plate_x0": -85.0, "plate_l": 220.0, "plate_w": 110.0, "plate_t": 4.0,
    "standoff_x": 68.0, "standoff_y": 40.0, "standoff_r": 3.0,
    # 2 Main PCB
    "pcb_l": 150.0, "pcb_w": 95.0, "pcb_t": 1.6, "pcb_z0": 6.8,
    # 4 MOSFET bank: 2 rows of 4 packages under the PCB on a 0.5 mm thermal pad
    "fet_x": (22.0, 36.0, 50.0, 63.0), "fet_y": 14.0, "fet_l": 10.0, "fet_w": 12.0,
    "pad_t": 0.5,
    # 8 Pack fuse and holder on the plate at +X
    "fuse_x0": 88.0, "fuse_l": 44.0, "fuse_w": 32.0, "fuse_h": 24.0,
    # 9 Power studs (M6) on the PCB, B-, P-, P+, B+ from -Y to +Y
    "stud_x": 66.0, "stud_y": (-33.0, -11.0, 11.0, 33.0), "stud_h": 20.0, "stud_d": 6.0,
    "stud_base_r": 6.5,
    # 13 Cover (flame-retardant polycarbonate)
    "cover_x0": -80.0, "cover_x1": 54.0, "cover_w": 104.0, "cover_top": 30.0, "cover_wall": 2.0,
    # 14 Secondary protector (BQ77216 class, TSSOP-24) and self-control protector fuse
    "sec_ic": (7.8, 6.4), "scp": (10.0, 6.5, 3.2),
}


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _rod(x, y, z0, z1, r):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def envelope(p=PARAMS):
    """Overall board envelope (x0, x1, y0, y1, z0, z1) without cables or harness tails."""
    fuse_top = p["plate_t"] + p["fuse_h"] + 4.0      # fuse body plus the link bolts
    top = max(p["cover_top"], fuse_top, p["pcb_z0"] + p["pcb_t"] + p["stud_h"])
    return (p["plate_x0"], p["plate_x0"] + p["plate_l"], -p["plate_w"] / 2, p["plate_w"] / 2, 0.0, top)


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    from build123d import Box, Pos, Sphere
    b, rod = _box, _rod
    T = p["plate_t"]
    top = p["pcb_z0"] + p["pcb_t"]                  # top face of the PCB
    wire_z = 11.0                                   # height of probe leads leaving the board
    probe_z = -22.5                                 # probe beads rest on the cell tops (hero context)

    # 1 Base plate with four PCB standoffs
    x0 = p["plate_x0"]; x1 = x0 + p["plate_l"]; hw = p["plate_w"] / 2
    plate = b(x0, x1, -hw, hw, 0, T)
    for sx in (-p["standoff_x"], p["standoff_x"]):
        for sy in (-p["standoff_y"], p["standoff_y"]):
            plate = plate + rod(sx, sy, T, p["pcb_z0"], p["standoff_r"])

    # 2 Main PCB
    pl, pw = p["pcb_l"], p["pcb_w"]
    pcb = b(-pl / 2, pl / 2, -pw / 2, pw / 2, p["pcb_z0"], top)

    # 3 Front end (BQ76952 class, TQFP-48, 9 x 9 mm)
    afe = b(-19.5, -10.5, -4.5, 4.5, top, top + 1.2)

    # 4 MOSFET bank on the thermal pad
    fets = b(15, 70, -22, 22, T, T + p["pad_t"])
    for x in p["fet_x"]:
        for y in (-p["fet_y"], p["fet_y"]):
            fets = fets + b(x - p["fet_l"] / 2, x + p["fet_l"] / 2, y - p["fet_w"] / 2, y + p["fet_w"] / 2,
                            T + p["pad_t"], p["pcb_z0"])

    # 5 Current shunt
    shunt = b(25, 45, -42, -34, top, top + 3.0)

    # 6 Microcontroller and CAN transceiver
    mcu = b(-48.5, -41.5, 14.5, 21.5, top, top + 1.4) + b(-60, -55, 28, 32, top, top + 1.5)

    # 7 Precharge resistor (aluminium housed) and P-channel MOSFET (DPAK class)
    pre = b(20, 46, 26, 40, top, top + 7.5) + b(8, 15, 30, 36.5, top, top + 2.3)

    # 8 Pack fuse and bolted holder on the plate
    fx0, fl, fw, fh = p["fuse_x0"], p["fuse_l"], p["fuse_w"], p["fuse_h"]
    fuse = b(fx0, fx0 + fl, -fw / 2, fw / 2, T, T + fh) + b(fx0 + 4, fx0 + fl - 4, -6, 6, T + fh, T + fh + 4)

    # 9 Power studs
    studs = None
    for y in p["stud_y"]:
        s = rod(p["stud_x"], y, top, top + 6.0, p["stud_base_r"]) + \
            rod(p["stud_x"], y, top + 6.0, top + p["stud_h"], p["stud_d"] / 2)
        studs = s if studs is None else studs + s

    # 10 Balance connector (17-way) and flat harness leaving the -X end
    bal = (b(-74, -65, -24, 20, top, top + 9.0)
           + b(-97, -74, -20, 16, wire_z, wire_z + 2.0)
           + b(-97, -95, -20, 16, probe_z - 2.5, wire_z + 2.0))

    # 11 Temperature sensors: one SMD beside the MOSFETs, two ring-lug probes
    ntc = b(38, 41, -6, -4, top, top + 1.5) + b(-40, -30, -46, -40, top, top + 5.6)
    lead1 = (Pos(-36, -63, wire_z) * Box(1.5, 34, 1.5)
             + rod(-36, -80, probe_z, wire_z + 0.75, 0.75) + Pos(-36, -80, probe_z) * Sphere(2.5))
    lead2 = (Pos(-32, -54, wire_z) * Box(1.5, 16, 1.5)
             + Pos(4, -62, wire_z) * Box(73.5, 1.5, 1.5)
             + Pos(40, -71, wire_z) * Box(1.5, 19.5, 1.5)
             + rod(40, -80, probe_z, wire_z + 0.75, 0.75) + Pos(40, -80, probe_z) * Sphere(2.5))
    ntc = ntc + lead1 + lead2

    # 12 CAN and UART connector through the cover's -X wall
    comm = b(-84, -66, 26, 40, top, top + 7.0)

    # 13 Cover over the signal and MOSFET area; studs and fuse stay reachable
    cx0, cx1, cw, ct, wl = p["cover_x0"], p["cover_x1"], p["cover_w"] / 2, p["cover_top"], p["cover_wall"]
    cover = b(cx0, cx1, -cw, cw, T, ct) - b(cx0 + wl, cx1 - wl, -cw + wl, cw - wl, T - 1, ct - wl)
    cover = cover - b(cx0 - 1, cx0 + 3, -26, 42, top - 0.4, top + 11.0)     # connector window
    cover = cover - b(cx1 - 3, cx1 + 1, -cw + 3, cw - 3, T - 1, top + 1.0)  # PCB and MOSFET pass-through
    cover = cover - b(-38, -30, -cw - 1, -cw + 3, top + 0.6, top + 5.0)     # probe lead exit

    # 14 Secondary protector IC and self-control protector (SCP) fuse in the B+ path
    sl, sw = p["sec_ic"]; ql, qw, qh = p["scp"]
    sec = b(-19.5, -19.5 + sl, -20.5, -20.5 + sw, top, top + 1.2) + b(57, 57 + ql, 40, 40 + qw, top, top + qh)

    return [
        ("Base plate and heat spreader", plate, "#9CA3AF", 1, (0, 0, -110)),
        ("Main PCB, 4-layer, 2 oz copper", pcb, "#15803D", 2, (0, 0, 45)),
        ("Cell monitor and protection IC", afe, "#111827", 3, (0, 0, 95)),
        ("Charge and discharge MOSFETs (8)", fets, "#374151", 4, (0, 0, -50)),
        ("Current shunt, 0.25 mOhm", shunt, "#B45309", 5, (0, -40, 95)),
        ("Microcontroller and CAN transceiver", mcu, "#0F766E", 6, (0, 30, 95)),
        ("Precharge resistor and switch", pre, "#D4A017", 7, (0, 40, 95)),
        ("Pack fuse and holder", fuse, "#C2410C", 8, (110, 0, 20)),
        ("Power terminals (B-, P-, P+, B+)", studs, "#E5E7EB", 9, (40, 0, 95)),
        ("Balance connector and lead harness", bal, "#1F2937", 10, (-20, 0, -75)),
        ("Temperature sensors (3)", ntc, "#38BDF8", 11, (0, -80, 85)),
        ("CAN and UART connector", comm, "#6B7280", 12, (-40, 60, 15)),
        ("Flame-retardant cover", cover, "#334155", 13, (40, 0, 200)),
        ("Secondary protector", sec, "#DC2626", 14, (0, 70, 95)),
    ]


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts}
    return {
        "cellguard-assembly": Compound([s for _, s, _, _, _ in parts]),
        "cellguard-base-plate": by[1],
        "cellguard-cover": by[13],
    }


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:24s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    e = envelope()
    print(f"board envelope without harness tails: {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.0f} mm")
    # Clash check between parts (pairwise intersection volume); the harness tail and probes are excluded
    worst = 0.0
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            v = (parts[i][1] & parts[j][1]).volume
            if v > 1.0:
                print(f"clash {parts[i][0]} / {parts[j][0]}: {v:.0f} mm3")
                worst = max(worst, v)
    print("clash check: none" if worst == 0 else "clash check: see above")
    for n, s, _, bom, _ in parts:
        print(f"volume {bom:2d} {n:40s} {s.volume / 1e3:8.2f} cm3")
