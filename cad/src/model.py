"""CellGuard parametric model (build123d), TRL 3, constructable design (CGD-DDR-003).

Run from the repo root:
    python cad/src/model.py            export STEP and STL, print envelope, clash check and volumes
    python cad/src/model.py --check    run the constructability checks only

Every part can be made or bought and every part is fixed to the next one (STANDARDS
section 18). The changes from the concept model are listed in CGD-DDR-003:
bought spacers and screws in place of standoffs drawn as part of the plate, a 3 mm
board-to-plate gap with a gap pad compressed from 1.0 to 0.7 mm, six board fixings,
four pillars that carry the cover, a cover with notches open at the bottom, a fuse
holder in line with the B+ stud joined by a straight copper link, and tapped holes
for mounting the plate.
Added on 2026-10-02 for the decisions in CGD-DEC-001: a three-colour status light on the
board (BOM line 15) and a flanged light pipe pressed into the opaque cover above it (line 19).

Axes: X along the board (power end at +X, signal end at -X), Y across, Z up. Units mm.
The base plate bottom face is z = 0.
"""
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 Base plate and heat spreader (6061 aluminium)
    "plate_x0": -85.0, "plate_l": 220.0, "plate_w": 110.0, "plate_t": 4.0,
    # board fixings: (x, y, what sits on top of the board there)
    "pcb_fix": ((-68.0, -40.0, "pillar"), (-68.0, 40.0, "pillar"), (48.0, -44.0, "pillar"),
                (48.0, 44.0, "pillar"), (71.5, -43.5, "nut"), (71.5, 43.5, "nut")),
    "spacer_h": 3.0, "spacer_od": 6.0, "spacer_id": 3.2,      # bought round aluminium spacers
    "pillar_h": 20.0, "pillar_od": 5.0,                       # bought M3 female-female round pillars
    "hole_m3": 3.4, "csk_d": 6.6,                             # M3 clearance, 90 degree countersink from below
    "mount_holes": ((-55.0, -30.0), (-55.0, 30.0), (82.0, -30.0), (82.0, 30.0)),   # M4 tapped, screws from below
    # 2 Main PCB
    "pcb_l": 150.0, "pcb_w": 95.0, "pcb_t": 1.6,
    # 4 MOSFET bank: 2 rows of 4 packages under the PCB on a gap pad
    "fet_x": (22.0, 36.0, 50.0, 63.0), "fet_y": 14.0, "fet_l": 10.0, "fet_w": 12.0, "fet_h": 2.3,
    "pad": (15.0, 70.0, -22.0, 22.0), "pad_nominal": 1.0,
    # 8 Pack fuse and holder on the plate, in line with the B+ stud
    "fuse_x0": 88.0, "fuse_l": 44.0, "fuse_w": 32.0, "fuse_y": 33.0, "fuse_term_dx": 5.0,
    # 9 Power studs (M6) soldered in the PCB, B-, P-, P+, B+ from -Y to +Y
    "stud_x": 66.0, "stud_y": (-33.0, -11.0, 11.0, 33.0), "stud_h": 20.0, "stud_d": 6.0,
    "stud_base_r": 6.5, "stud_base_h": 6.0,
    # 18 Fuse link: copper flat bar from the B+ stud to the fuse holder's inner terminal
    "link_w": 14.0, "link_t": 3.0,
    # 12 CAN and UART connector, mating face flush with the cover's outside face
    "comm": (-80.0, -62.0, 22.0, 36.0, 7.0),
    # 13 Cover (flame-retardant polycarbonate, printed)
    "cover_x0": -80.0, "cover_x1": 54.0, "cover_w": 104.0, "cover_wall": 2.0, "cover_lift": 0.5,
    # 14 Secondary protector (BQ77216 class, TSSOP-24) and self-control protector fuse
    "sec_ic": (7.8, 6.4), "scp": (10.0, 6.5, 3.2),
    # 15 Status light: one three-colour LED (PLCC-4, 3.5 x 2.8 x 1.9 mm) on the board top (CGD-DEC-001, 2026-10-02)
    "led_xy": (-30.0, 20.0), "led": (3.5, 2.8, 1.9),
    # 19 Light pipe: flanged round light pipe pressed into a hole in the cover top, over the status light
    "lp_d": 3.0, "lp_hole": 3.2, "lp_flange_d": 6.0, "lp_flange_t": 1.0, "lp_gap": 0.5,
}


def derived(p=PARAMS):
    """Heights that follow from the parameters."""
    T = p["plate_t"]
    pcb_z0 = T + p["spacer_h"]
    top = pcb_z0 + p["pcb_t"]
    pad_t = p["spacer_h"] - p["fet_h"]                       # compressed gap pad thickness
    stud_face = top + p["stud_base_h"]                       # where ring lugs and the link sit
    pillar_top = top + p["pillar_h"]
    return dict(T=T, pcb_z0=pcb_z0, top=top, pad_t=pad_t, stud_face=stud_face, pillar_top=pillar_top,
                cover_top=pillar_top + p["cover_wall"], holder_top=stud_face - 2.0,
                fuse_term=(p["fuse_x0"] + p["fuse_term_dx"], p["fuse_x0"] + p["fuse_l"] - p["fuse_term_dx"]))


# Heights that follow from the parameters, also kept in PARAMS for cad/src/product_model.py
PARAMS.update({k: v for k, v in derived(PARAMS).items() if k in ("pcb_z0", "pad_t", "cover_top")})


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _rod(x, y, z0, z1, r):
    from build123d import Cylinder, Pos
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _xrod(x0, x1, y, z, r):
    from build123d import Cylinder, Pos, Rot
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _csk_hole(x, y, T, d, dk):
    """Through hole with a 90 degree countersink opening on the bottom face (z = 0)."""
    from build123d import Cone, Pos
    h = (dk - d) / 2
    return _rod(x, y, -1, T + 1, d / 2) + Pos(x, y, h / 2 - 0.01) * Cone(dk / 2 + 0.01, d / 2, h + 0.02)


def build_components(p=PARAMS):
    """Every part of the prototype as a dict name -> shape (plus BOM line), for the checks and pictures."""
    from build123d import Box, Pos, Sphere
    b, rod = _box, _rod
    d = derived(p)
    T, z0, top = d["T"], d["pcb_z0"], d["top"]
    wire_z = 11.0                                   # height of the probe leads and harness as they leave
    probe_z = -22.5                                 # probe beads rest on the cell tops (hero context)
    C = {}

    def add(key, shape, bom):
        C[key] = (shape, bom)

    # 1 Base plate: flat 4 mm sheet with holes only
    x0 = p["plate_x0"]; x1 = x0 + p["plate_l"]; hw = p["plate_w"] / 2
    plate = b(x0, x1, -hw, hw, 0, T)
    for x, y, _ in p["pcb_fix"]:
        plate = plate - _csk_hole(x, y, T, p["hole_m3"], p["csk_d"])
    for x, y in p["mount_holes"]:
        plate = plate - rod(x, y, -1, T + 1, 3.3 / 2)                     # M4 tapped through
    fy = p["fuse_y"]
    hs = holder_screws(p)
    for x, y in hs:
        plate = plate - rod(x, y, -1, T + 1, 2.0)                         # M4 tapped through (drawn at thread size)
    add("plate", plate, 1)

    # 17 Gap pad, compressed between the MOSFET tops and the plate
    px0, px1, py0, py1 = p["pad"]
    add("pad", b(px0, px1, py0, py1, T, T + d["pad_t"]), 17)

    # 17 Spacers under the board and M3 countersunk screws up from below the plate
    sp = None; scr = None
    for x, y, kind in p["pcb_fix"]:
        s = rod(x, y, T, z0, p["spacer_od"] / 2) - rod(x, y, T - 1, z0 + 1, p["spacer_id"] / 2)
        sp = s if sp is None else sp + s
        tip = top + (6.0 if kind == "pillar" else 3.6)
        from build123d import Cone
        h = (p["csk_d"] - 3.0) / 2
        sc = rod(x, y, h, tip, 1.4) + Pos(x, y, h / 2) * Cone(p["csk_d"] / 2 - 0.1, 1.5, h)
        scr = sc if scr is None else scr + sc
    add("spacers", sp, 17)
    add("pcb_screws", scr, 17)

    # 2 Main PCB with six fixing holes
    pl, pw = p["pcb_l"], p["pcb_w"]
    pcb = b(-pl / 2, pl / 2, -pw / 2, pw / 2, z0, top)
    for x, y, _ in p["pcb_fix"]:
        pcb = pcb - rod(x, y, z0 - 1, top + 1, p["hole_m3"] / 2)
    add("pcb", pcb, 2)

    # 3 Front end (BQ76952 class, TQFP-48, 9 x 9 mm)
    add("afe", b(-19.5, -10.5, -4.5, 4.5, top, top + 1.2), 3)

    # 4 MOSFETs, soldered to the underside of the PCB, tops on the pad
    fets = None
    for x in p["fet_x"]:
        for y in (-p["fet_y"], p["fet_y"]):
            f = b(x - p["fet_l"] / 2, x + p["fet_l"] / 2, y - p["fet_w"] / 2, y + p["fet_w"] / 2, T + d["pad_t"], z0)
            fets = f if fets is None else fets + f
    add("fets", fets, 4)

    # 5 Current shunt, 6 microcontroller and CAN transceiver, 7 precharge
    add("shunt", b(25, 45, -42, -34, top, top + 3.0), 5)
    add("mcu", b(-48.5, -41.5, 14.5, 21.5, top, top + 1.4) + b(-60, -55, 28, 32, top, top + 1.5), 6)
    add("pre", b(20, 46, 26, 40, top, top + 7.5) + b(8, 15, 30, 36.5, top, top + 2.3), 7)

    # 9 Power studs: brass terminal blocks soldered through the PCB, M6 male thread
    studs = None
    for y in p["stud_y"]:
        s = rod(p["stud_x"], y, top, d["stud_face"], p["stud_base_r"]) + \
            rod(p["stud_x"], y, d["stud_face"], top + p["stud_h"], p["stud_d"] / 2)
        studs = s if studs is None else studs + s
    add("studs", studs, 9)

    # 10 Balance connector on the board, and the harness plug and tail
    add("bal_header", b(-74, -65, -24, 20, top, top + 9.0), 10)
    add("harness", b(-97, -74, -20, 16, wire_z, wire_z + 2.0) + b(-97, -95, -20, 16, probe_z - 2.5, wire_z), 10)

    # 11 Temperature sensors: SMD beside the MOSFETs and the probe header on the board; two probe leads
    add("ntc_board", b(38, 41, -6, -4, top, top + 1.5) + b(-40, -30, -46, -40, top, top + 5.6), 11)
    lead1 = (Pos(-36, -63, wire_z) * Box(1.5, 34, 1.5)
             + rod(-36, -80, probe_z, wire_z + 0.75, 0.75) + Pos(-36, -80, probe_z) * Sphere(2.5))
    lead2 = (Pos(-32, -54, wire_z) * Box(1.5, 16, 1.5)
             + Pos(4, -62, wire_z) * Box(73.5, 1.5, 1.5)
             + Pos(40, -71, wire_z) * Box(1.5, 19.5, 1.5)
             + rod(40, -80, probe_z, wire_z + 0.75, 0.75) + Pos(40, -80, probe_z) * Sphere(2.5))
    add("probes", lead1 + lead2, 11)

    # 12 CAN and UART connector, mating face flush with the cover outside face
    cx0_, cx1_, cy0_, cy1_, ch = p["comm"]
    add("comm", b(cx0_, cx1_, cy0_, cy1_, top, top + ch), 12)
    add("can_plug", b(cx0_ - 16, cx0_, cy0_ + 1, cy1_ - 1, top + 0.5, top + ch - 0.5)
        + b(cx0_ - 40, cx0_ - 16, (cy0_ + cy1_) / 2 - 2.5, (cy0_ + cy1_) / 2 + 2.5, top + 1.0, top + 6.0), 0)

    # 14 Secondary protector IC and self-control protector (SCP) fuse in the B+ path
    sl, sw = p["sec_ic"]; ql, qw, qh = p["scp"]
    add("sec", b(-19.5, -19.5 + sl, -20.5, -20.5 + sw, top, top + 1.2) + b(57, 57 + ql, 40, 40 + qw, top, top + qh), 14)

    # 15 Status light: one three-colour LED on the board top, under the light pipe (CGD-DEC-001, 2026-10-02)
    lx, ly = p["led_xy"]; ll, lw_, lh = p["led"]
    add("led", b(lx - ll / 2, lx + ll / 2, ly - lw_ / 2, ly + lw_ / 2, top, top + lh), 15)

    # 17 Pillars on the board (carry the cover) and nuts at the two outer fixings
    pil = None; nuts = None
    for x, y, kind in p["pcb_fix"]:
        if kind == "pillar":
            s = rod(x, y, top, d["pillar_top"], p["pillar_od"] / 2) - rod(x, y, top - 1, d["pillar_top"] + 1, 1.5)
            pil = s if pil is None else pil + s
        else:
            from build123d import RegularPolygon, extrude, Plane
            n = Pos(x, y, top) * extrude(RegularPolygon(5.5 / 2 / 0.866, 6), 2.4) - rod(x, y, top - 1, top + 3.4, 1.6)
            nuts = n if nuts is None else nuts + n
    add("pillars", pil, 17)
    add("nuts", nuts, 17)

    # 8 Fuse holder (insulating base, two terminal studs) with the fuse bolted across it
    fx0, fl, fw = p["fuse_x0"], p["fuse_l"], p["fuse_w"]
    ht = d["holder_top"]
    t0, t1 = d["fuse_term"]
    holder = b(fx0, fx0 + fl, fy - fw / 2, fy + fw / 2, T, ht)
    for x, y in hs:
        holder = holder - rod(x, y, T - 1, ht + 1, 2.2)
    fuse_body = _xrod(t0 + 7, t1 - 7, fy, ht + 9.0, 7.0)
    blades = (b(t0 - 6, t0 + 8, fy - 6, fy + 6, ht, ht + 2.0) - rod(t0, fy, ht - 1, ht + 3, 4.25)) + \
             (b(t1 - 8, t1 + 6, fy - 6, fy + 6, ht, ht + 2.0) - rod(t1, fy, ht - 1, ht + 3, 4.25))
    tstuds = rod(t0, fy, ht, ht + 15.0, 4.0) + rod(t1, fy, ht, ht + 15.0, 4.0)
    add("fuse", holder + fuse_body + blades + tstuds, 8)
    hscr = None
    for x, y in hs:
        s = rod(x, y, T - 3.5, ht, 1.9) + rod(x, y, ht, ht + 2.8, 3.5)
        hscr = s if hscr is None else hscr + s
    add("holder_screws", hscr, 17)

    # 18 Fuse link: straight copper flat bar, B+ stud to the fuse holder's inner terminal
    lw, lt = p["link_w"], p["link_t"]
    sx, by = p["stud_x"], p["stud_y"][3]
    z = d["stud_face"]
    link = b(sx, t0, by - lw / 2, by + lw / 2, z, z + lt) + rod(sx, by, z, z + lt, lw / 2) + rod(t0, fy, z, z + lt, lw / 2)
    link = link - rod(sx, by, z - 1, z + lt + 1, 6.5 / 2) - rod(t0, fy, z - 1, z + lt + 1, 8.5 / 2)
    add("link", link, 18)

    # 13 Cover: printed, carried on the four pillars, walls 0.5 mm clear of the plate
    cx0, cx1, cw, wl = p["cover_x0"], p["cover_x1"], p["cover_w"] / 2, p["cover_wall"]
    ct = d["cover_top"]
    zb = T + p["cover_lift"]
    cover = b(cx0, cx1, -cw, cw, zb, ct) - b(cx0 + wl, cx1 - wl, -cw + wl, cw - wl, zb - 1, ct - wl)
    cover = cover - b(cx0 - 1, cx0 + 3, -26, 42, zb - 1, top + 11.0)       # connector notch, open at the bottom
    cover = cover - b(cx1 - 3, cx1 + 1, -cw + 3, cw - 3, zb - 1, top + 1.0)  # board pass-through, open at the bottom
    cover = cover - b(-38, -30, -cw - 1, -cw + 3, zb - 1, top + 5.0)       # probe lead notch, open at the bottom
    cscr = None
    for x, y, kind in p["pcb_fix"]:
        if kind == "pillar":
            cover = cover - rod(x, y, ct - wl - 1, ct + 1, 1.7)
            s = rod(x, y, ct - wl - 4.0, ct, 1.4) + rod(x, y, ct, ct + 2.1, 2.75)
            cscr = s if cscr is None else cscr + s
    cover = cover - rod(lx, ly, ct - wl - 1, ct + 1, p["lp_hole"] / 2)        # light pipe hole over the status light
    add("cover", cover, 13)
    add("cover_screws", cscr, 17)

    # 19 Light pipe: round, flanged, pressed into the cover top from above; its foot stops just above the LED
    lp = rod(lx, ly, top + lh + p["lp_gap"], ct, p["lp_d"] / 2) + rod(lx, ly, ct, ct + p["lp_flange_t"], p["lp_flange_d"] / 2)
    add("light_pipe", lp, 19)
    return C


def holder_screws(p=PARAMS):
    fx0, fl, fy = p["fuse_x0"], p["fuse_l"], p["fuse_y"]
    return [(fx0 + 5, fy - 12), (fx0 + 5, fy + 12), (fx0 + fl - 5, fy - 12), (fx0 + fl - 5, fy + 12)]


NAMES = {
    1: "Base plate and heat spreader", 2: "Main PCB, 4-layer, 2 oz copper", 3: "Cell monitor and protection IC",
    4: "Charge and discharge MOSFETs (8)", 5: "Current shunt, 0.25 mOhm", 6: "Microcontroller and CAN transceiver",
    7: "Precharge resistor and switch", 8: "Pack fuse and holder", 9: "Power terminals (B-, P-, P+, B+)",
    10: "Balance connector and lead harness", 11: "Temperature sensors (3)", 12: "CAN and UART connector",
    13: "Flame-retardant cover", 14: "Secondary protector", 17: "Gap pad, spacers, pillars and screws",
    15: "Status light, three-colour", 18: "Fuse link (copper bar)", 19: "Light pipe"}
COLOURS = {1: "#9CA3AF", 2: "#15803D", 3: "#111827", 4: "#374151", 5: "#B45309", 6: "#0F766E", 7: "#D4A017",
           8: "#C2410C", 9: "#E5E7EB", 10: "#1F2937", 11: "#38BDF8", 12: "#6B7280", 13: "#334155", 14: "#DC2626",
           15: "#22C55E", 17: "#78716C", 18: "#B87333", 19: "#E5E7EB"}
EXPLODE = {1: (0, 0, -110), 2: (0, 0, 45), 3: (0, 0, 95), 4: (0, 0, -50), 5: (0, -40, 95), 6: (0, 30, 95),
           7: (0, 40, 95), 8: (110, 0, 20), 9: (40, 0, 95), 10: (-20, 0, -75), 11: (0, -80, 85), 12: (-40, 60, 15),
           13: (40, 0, 200), 14: (0, 70, 95), 15: (-20, 60, 95), 17: (0, 0, -80), 18: (60, 40, 60),
           19: (40, 0, 250)}


def build_parts(p=PARAMS):
    """BOM-numbered parts: a list of (name, shape, colour, bom_item, explode_offset). Line 0 (host plug) is left out."""
    C = build_components(p)
    by = {}
    for k, (s, bom) in C.items():
        if bom:
            by.setdefault(bom, []).append(s)
    return [(NAMES[n], _fuse(by[n]), COLOURS[n], n, EXPLODE[n]) for n in sorted(by)]


def envelope(p=PARAMS):
    """Overall board envelope (x0, x1, y0, y1, z0, z1) without cables, harness tail, probes or the host plug."""
    C = build_components(p)
    z1 = max(C[k][0].bounding_box().max.Z for k in ("cover", "cover_screws", "studs", "fuse", "light_pipe"))
    return (p["plate_x0"], p["plate_x0"] + p["plate_l"], -p["plate_w"] / 2, p["plate_w"] / 2, 0.0, z1)


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts}
    return {
        "cellguard-assembly": Compound([s for _, s, _, _, _ in parts]),
        "cellguard-base-plate": by[1],
        "cellguard-cover": by[13],
        "cellguard-fuse-link": by[18],
    }


# ---------------------------------------------------------------- constructability checks
def checks(p=PARAMS, verbose=True):
    """Return a list of (ok, text). Contacts must touch; clearances must hold; nothing may overlap;
    each part fitted in an assembly step must reach its place along its fitting direction."""
    from build123d import Pos
    C = {k: v[0] for k, v in build_components(p).items()}
    d = derived(p)
    res = []

    def vol(a, b):
        try:
            return (C[a] & C[b]).volume
        except Exception:
            return 0.0

    def gap(a, b):
        return C[a].distance_to(C[b])

    # 1 no overlaps between any two parts (screws pass through clearance holes)
    keys = [k for k in C if k not in ("harness", "probes", "can_plug")]
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            v = vol(keys[i], keys[j])
            if v > 0.05:
                res.append((False, f"overlap {keys[i]} / {keys[j]}: {v:.2f} mm3"))
    if not any(not ok for ok, _ in res):
        res.append((True, f"no overlaps among {len(keys)} parts"))

    # 2 contacts (faces that must touch: gap 0)
    for a, b, why in [("pad", "plate", "gap pad sits on the plate"), ("fets", "pad", "MOSFET tops press on the pad"),
                      ("fets", "pcb", "MOSFETs soldered to the board underside"), ("spacers", "plate", "spacers on the plate"),
                      ("spacers", "pcb", "board on the spacers"), ("pillars", "pcb", "pillars on the board"),
                      ("nuts", "pcb", "nuts on the board"), ("cover", "pillars", "cover on the pillar tops"),
                      ("fuse", "plate", "fuse holder on the plate"), ("holder_screws", "fuse", "holder screw heads on the holder"),
                      ("link", "studs", "link on the B+ stud shoulder"), ("link", "fuse", "link on the fuse terminal blade"),
                      ("studs", "pcb", "studs soldered to the board"), ("comm", "pcb", "CAN connector on the board"),
                      ("bal_header", "pcb", "balance connector on the board"), ("cover_screws", "cover", "cover screws on the cover"),
                      ("pcb_screws", "plate", "board screws seated in the countersinks"),
                      ("led", "pcb", "status light soldered to the board"),
                      ("light_pipe", "cover", "light pipe flange on the cover top")]:
        g = gap(a, b)
        res.append((g < 0.02, f"contact: {why} (gap {g:.2f} mm)"))

    # 3 clearances
    for a, b, need, why in [("cover", "plate", p["cover_lift"] - 0.01, "cover walls clear the plate"),
                            ("cover", "pcb", 0.9, "cover clear of the board"),
                            ("cover", "comm", 0.0, "cover clear of the CAN connector"),
                            ("cover", "studs", 4.0, "cover clear of the studs"),
                            ("link", "sec", 2.0, "link clear of the SCP fuse"),
                            ("link", "holder_screws", 0.5, "link clear of the holder screws"),
                            ("nuts", "studs", 1.0, "board nuts clear of the studs"),
                            ("nuts", "sec", 1.0, "board nuts clear of the SCP fuse"),
                            ("pillars", "comm", 1.0, "pillars clear of the CAN connector"),
                            ("pillars", "pre", 1.0, "pillars clear of the precharge resistor"),
                            ("pillars", "shunt", 0.4, "pillars clear of the shunt"),
                            ("fuse", "pcb", 10.0, "fuse holder clear of the board edge"),
                            ("spacers", "fets", 10.0, "spacers clear of the MOSFETs"),
                            ("light_pipe", "led", p["lp_gap"] - 0.01, "light pipe foot clear of the status light"),
                            ("light_pipe", "mcu", 1.0, "light pipe clear of the controller"),
                            ("led", "mcu", 1.0, "status light clear of the controller"),
                            ("led", "pillars", 3.0, "status light clear of the pillars")]:
        g = gap(a, b)
        res.append((g >= need, f"clearance: {why} {g:.2f} mm (need {need:.1f})"))
    # link to the P+ stud: live parts at different potential, keep 6 mm for the P+ ring lug and nut
    from build123d import Cylinder
    pplus = _rod(p["stud_x"], p["stud_y"][2], d["top"], d["top"] + p["stud_h"], 7.5)  # P+ lug envelope
    g = C["link"].distance_to(pplus)
    res.append((g >= 1.5, f"clearance: link to the P+ ring lug envelope {g:.2f} mm (need 1.5)"))

    # 4 heights that must match
    res.append((abs(d["pad_t"] - 0.7) < 1e-6, f"gap pad compressed from {p['pad_nominal']:.1f} to {d['pad_t']:.1f} mm "
                f"({100 * (1 - d['pad_t'] / p['pad_nominal']):.0f} %, within the 10 to 40 % a gap pad takes)"))
    res.append((abs(C["link"].bounding_box().min.Z - d["stud_face"]) < 1e-6, "link is flat: stud shoulder and fuse blade at the same height"))
    lpc = C["light_pipe"].bounding_box().center(); ldc = C["led"].bounding_box().center()
    off = ((lpc.X - ldc.X) ** 2 + (lpc.Y - ldc.Y) ** 2) ** 0.5
    res.append((off < 0.3, f"light pipe on the status light axis (offset {off:.2f} mm, need under 0.3)"))
    lp_top = C["light_pipe"].bounding_box().max.Z
    res.append((lp_top <= C["cover_screws"].bounding_box().max.Z + 1e-6,
                f"light pipe flange top {lp_top:.1f} mm, inside the envelope set by the cover screw heads"))

    # 5 assembly order: each part reaches its place along its fitting direction without passing through fitted parts
    order = [("pad", (0, 0, 1), ["plate"]),
             ("spacers", (0, 0, 1), ["plate", "pad", "pcb_screws"]),
             ("pcb+", (0, 0, 1), ["plate", "pad", "spacers", "pcb_screws"]),
             ("pillars", (0, 0, 1), ["plate", "pad", "spacers", "pcb_screws", "pcb+"]),
             ("nuts", (0, 0, 1), ["plate", "pad", "spacers", "pcb_screws", "pcb+"]),
             ("fuse", (0, 0, 1), ["plate", "pcb+", "pillars", "nuts"]),
             ("holder_screws", (0, 0, 1), ["plate", "fuse"]),
             ("link", (0, 0, 1), ["plate", "pcb+", "fuse", "holder_screws", "nuts"]),
             ("cover", (0, 0, 1), ["plate", "pcb+", "pillars", "nuts", "fuse", "link", "probes"]),
             ("cover_screws", (0, 0, 1), ["cover", "pillars"]),
             ("light_pipe", (0, 0, 1), ["cover", "pcb+"]),
             ("harness", (-1, 0, 0), ["plate", "pcb+", "cover"]),
             ("can_plug", (-1, 0, 0), ["plate", "pcb+", "cover"])]
    board = None
    for k in ("pcb", "afe", "fets", "shunt", "mcu", "pre", "studs", "bal_header", "ntc_board", "comm", "sec", "led"):
        board = C[k] if board is None else board + C[k]
    C["pcb+"] = board
    for key, (dx, dy, dz), fitted in order:
        hit = 0.0
        for s in (2, 5, 10, 20, 40, 80):
            moved = Pos(dx * s, dy * s, dz * s) * C[key]
            for f in fitted:
                if f == key:
                    continue
                try:
                    hit = max(hit, (moved & C[f]).volume)
                except Exception:
                    pass
        res.append((hit < 0.05, f"assembly: {key} goes in along {(dx, dy, dz)} without hitting fitted parts"
                    + ("" if hit < 0.05 else f" (hit {hit:.1f} mm3)")))
    if verbose:
        for ok, t in res:
            print(("PASS " if ok else "FAIL ") + t)
        print(f"{sum(ok for ok, _ in res)} of {len(res)} checks pass")
    return res


if __name__ == "__main__":
    if "--check" in sys.argv:
        r = checks()
        sys.exit(0 if all(ok for ok, _ in r) else 1)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name:24s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    e = envelope()
    print(f"board envelope without harness tails: {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.1f} mm")
    worst = 0.0
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            v = (parts[i][1] & parts[j][1]).volume
            if v > 0.05:
                print(f"clash {parts[i][0]} / {parts[j][0]}: {v:.2f} mm3")
                worst = max(worst, v)
    print("clash check: none" if worst == 0 else "clash check: see above")
    for n, s, _, bom, _ in parts:
        print(f"volume {bom:2d} {n:40s} {s.volume / 1e3:8.2f} cm3")
