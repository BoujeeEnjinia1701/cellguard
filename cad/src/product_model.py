"""CellGuard product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders, matching the constructable design of model.py
(CGD-DDR-003) and the decisions of 2026-10-02 (CGD-DEC-001): the battery management board under an
opaque printed flame-retardant polycarbonate cover carried on four pillars and held by four
screws, with a light pipe in its top showing the lit three-colour status light, a name plate and a
warning label. The aluminium base plate is flat with filleted corners and four tapped mounting
holes; the board sits on six spacers. Brass M6 stud terminals with nuts, the bolted pack fuse in
its holder in line with the B+ stud, the straight copper fuse link, and latching plugs on the
balance and CAN connectors complete the device. Context is a compact 4S LiFePO4 pack beside the
board (product renders only, decided 2026-10-02), with its balance leads in a braided sleeve, the
two temperature probes, the B- cable to its stud and the B+ cable to the fuse holder's outer
terminal, all on a small bench mat.
APPEARANCE MODEL ONLY: no tolerances, no PCB layout, no fabrication detail.
CONCEPT, NOT FOR FABRICATION. A research prototype design, not a certified BMS.

Every main dimension and interface comes from PARAMS, derived(), holder_screws() and
build_components() in model.py. Axes as model.py: X along the board (power end at +X, signal end
at -X), Y across, Z up, base plate bottom face at Z = 0. The pack beside the board is illustrative
(compact prismatic cells, sizes not from a data sheet); in concept_media.py the board sits on posts
above a 4S pack of 280 Ah cells. See docs/REVIEW.md, sessions 2026-09-26 and 2026-10-02.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere, Vector,
                       extrude, fillet)
from model import PARAMS, build_components, build_parts, derived, holder_screws

TITLE = "CellGuard: open battery management board for small LiFePO4 packs"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); board under its opaque "
             "cover with the status light showing through the light pipe, power studs, copper fuse link and pack "
             "fuse at the right end, compact 4S LiFePO4 pack at left with balance leads, temperature probes and "
             "power cables connected"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): opaque cover with light "
             "pipe and screws, pillars, power studs and nuts, populated main board with the status light, balance "
             "and CAN plugs, MOSFETs and gap pad, spacers, pack fuse, holder and copper link, aluminium base plate"},
    {"name": "detail", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 34, "az": -35,
     "note": "Detail from the front right and above (about 34 deg elevation) without the pack: opaque cover "
             "with the green status light lit in its light pipe, studs, copper fuse link and fuse at right, "
             "the cable slot in the cover at left"},
]

# Colours (restrained product palette; kit accent)
C_ACCENT = "#0F766E"
C_PLATE = "#A9AFB6"
C_CLEAR = "#DCEBF5"
C_COVER = "#2F3A45"                          # opaque flame-retardant polycarbonate (decided 2026-10-02)
C_PCB = "#166534"
C_CHIP = "#111827"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_METAL = "#B8BEC6"
C_BRASS = "#C9A227"
C_COPPER = "#B87333"
C_GOLD = "#C8A23A"
C_PAD = "#7C8C99"
C_LABEL = "#F4F4F2"
C_SILK = "#EDEDEA"
C_LED_G = "#22C55E"
C_LED_A = "#6E5315"
C_LED_R = "#5E1C1C"
C_FUSE = "#E7E2D6"
C_RED = "#B91C1C"
C_LEAD = "#374151"
C_PROBE = "#D1D5DB"
C_CELL = "#3E5C7A"
C_CELLTOP = "#23272E"
C_ENDPL = "#4B5563"
C_STRAP = "#1F2937"
C_MAT = "#D5D8DC"

# Context layout (render only; not part of the board)
CELL_T, CELL_W, CELL_H = 27.0, 148.0, 97.0   # illustrative compact prismatic cell: thickness (Y), width (X), height
END_T = 5.0                                  # pack end plate thickness
PCX = -204.0                                 # pack centre X (pack spans x -278 .. -130, beside the -X end)
TERM_DX = 45.0                               # terminal offset from the cell centre along X
TOP_CAP = 1.5
MAT = (-292.0, 162.0, -80.0, 78.0, 3.0)      # bench mat x0, x1, y0, y1, thickness


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _b(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners (as model.py)."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _zcyl(x, y, z0, z1, r):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _hex_z(x, y, z0, af, h):
    return Pos(x, y, z0) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _pipe(points, r):
    """Round cable through `points` with spherical joints (clean bends)."""
    out = None
    for a, c in zip(points, points[1:]):
        a, c = Vector(*a), Vector(*c)
        d = c - a
        seg = Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))
        out = seg if out is None else out + seg
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _zedges(s):
    return s.edges().filter_by(Axis.Z)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _nut(x, y, z0, af=10.0, h=5.0):
    n = _hex_z(x, y, z0, af, h)
    n = _fillet_try(n, _top(n), [0.6, 0.3])
    return n - _zcyl(x, y, z0 - 1, z0 + h + 1, af * 0.26)


def _screw(x, y, z0, r=2.8, h=1.4):
    s = _zcyl(x, y, z0, z0 + h, r)
    s = _fillet_try(s, _top(s), [0.9, 0.5])
    return s - _b(x - r, x + r, y - 0.35, y + 0.35, z0 + 0.6, z0 + h + 1) \
        - _b(x - 0.35, x + 0.35, y - r, y + r, z0 + 0.6, z0 + h + 1)


def _lug(x, y, z0, t, r_out, r_in, dx, dy, w):
    """Flat ring lug centred on a stud, with its barrel tongue toward (dx, dy)."""
    ring = _zcyl(x, y, z0, z0 + t, r_out) - _zcyl(x, y, z0 - 1, z0 + t + 1, r_in)
    L = (dx * dx + dy * dy) ** 0.5
    ang = 0.0 if abs(dy) < 1e-9 and dx > 0 else (180.0 if abs(dy) < 1e-9 else (90.0 if dy > 0 else -90.0))
    tongue = Pos(x, y, z0 + t / 2) * Rot(0, 0, ang) * Pos(L / 2 + r_out * 0.4, 0, 0) * Box(L, w, t)
    return ring + tongue


def product_parts(P=PARAMS):
    m = {bom: s for _, s, _, bom, _ in build_parts(P)}
    C = {k: v[0] for k, v in build_components(P).items()}
    d = derived(P)
    T = P["plate_t"]
    top = P["pcb_z0"] + P["pcb_t"]                     # PCB top face, 8.4 mm
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    E_PLATE = (0, 0, -90)
    E_PAD = (0, 0, -55)
    E_FET = (0, 0, -32)
    E_PCB = (0, 0, 25)
    E_STUD = (0, 0, 80)
    E_NUT = (0, 0, 115)
    E_COVER = (0, 0, 165)
    E_CSCREW = (0, 0, 195)
    E_FUSE = (70, 0, -45)
    E_FNUT = (70, 0, -15)
    E_PLUG = (-75, 0, 25)

    # ------------------------------------------------------------ base plate (BOM 1)
    x0 = P["plate_x0"]; x1 = x0 + P["plate_l"]; hw = P["plate_w"] / 2
    plate = _b(x0, x1, -hw, hw, 0, T)
    plate = _fillet_try(plate, _zedges(plate), [8.0, 6.0, 4.0])
    plate = _fillet_try(plate, _top(plate), [1.2, 0.8, 0.5])
    for hx, hy in P["mount_holes"]:                        # four M4 tapped mounting holes (CGD-DDR-003)
        plate -= _zcyl(hx, hy, -1, T + 1, 1.65)
    for hx, hy in holder_screws(P):                        # fuse holder screws go into these
        plate -= _zcyl(hx, hy, -1, T + 1, 1.65)
    for sx, sy, _ in P["pcb_fix"]:                         # board fixings, countersunk from below
        plate -= _zcyl(sx, sy, -1, T + 1, P["hole_m3"] / 2)
    add("Aluminium base plate and heat spreader", plate, C_PLATE, "metal", 1, "shell", E_PLATE)
    # bought spacers under the board, pillars that carry the cover, nuts at the power-end corners (BOM 17)
    add("Board spacers, aluminium (6)", C["spacers"], C_METAL, "metal", 17, "internal", E_PAD)
    add("Cover pillars, aluminium (4)", C["pillars"], C_METAL, "metal", 17, "internal", E_STUD)
    add("Board fixing nuts (2)", C["nuts"], C_METAL, "metal", 17, "internal", E_STUD)

    # thermal pad and MOSFET bank under the PCB (BOM 4, 17), same envelopes as model.py
    pad = _b(15, 70, -22, 22, T, T + P["pad_t"])
    add("Thermal pad", pad, C_PAD, "rubber", 17, "internal", E_PAD)
    fets = []
    for x in P["fet_x"]:
        for y in (-P["fet_y"], P["fet_y"]):
            f = _b(x - P["fet_l"] / 2, x + P["fet_l"] / 2, y - P["fet_w"] / 2, y + P["fet_w"] / 2,
                   T + P["pad_t"], P["pcb_z0"])
            fets.append(_fillet_try(f, _zedges(f), [0.6, 0.3]))
    add("Charge and discharge MOSFETs (8, TOLT)", _union(fets), C_CHIP, "plastic", 4, "internal", E_FET)

    # ------------------------------------------------------------ main PCB (BOM 2) and components
    pl, pw = P["pcb_l"], P["pcb_w"]
    pcb = _b(-pl / 2, pl / 2, -pw / 2, pw / 2, P["pcb_z0"], top)
    pcb = _fillet_try(pcb, _zedges(pcb), [2.5, 1.5])
    add("Main PCB, 4-layer, 2 oz copper", pcb, C_PCB, "plastic", 2, "internal", E_PCB)

    add("Cell monitor and protection IC", m[3], C_CHIP, "plastic", 3, "internal", E_PCB)
    add("Microcontroller and CAN transceiver", m[6], C_CHIP, "plastic", 6, "internal", E_PCB)
    add("Secondary protector and SCP fuse", m[14], C_CHIP, "plastic", 14, "internal", E_PCB)
    add("Current shunt, 0.25 mOhm", m[5], C_COPPER, "metal", 5, "internal", E_PCB)

    # precharge: aluminium-housed resistor with fins, and the DPAK-class switch (BOM 7)
    res = _b(20, 46, 26, 40, top, top + 7.5)
    for k in range(4):
        yk = 28.5 + 3.0 * k
        res -= _b(19, 47, yk, yk + 1.2, top + 5.5, top + 8.5)
    res = _fillet_try(res, _zedges(res), [0.8, 0.4])
    add("Precharge resistor, aluminium housed", res, C_GOLD, "metal", 7, "internal", E_PCB)
    add("Precharge switch (DPAK)", _b(8, 15, 30, 36.5, top, top + 2.3), C_CHIP, "plastic", 7, "internal", E_PCB)

    # temperature sensing on the board: SMD thermistor and the probe lead header (BOM 11)
    ntc = _b(38, 41, -6, -4, top, top + 1.5) + _b(-40, -30, -46, -40, top, top + 5.6)
    add("Board thermistor and probe header", ntc, C_DARK, "plastic", 11, "internal", E_PCB)

    # supporting electronics (BOM 15): balance resistors, buck, flash, TVS, capacitors
    small = []
    for row, y in enumerate((-31.0, -26.5)):
        for k in range(8):
            x = -58.0 + 3.8 * k
            small.append(_b(x - 1.2, x + 1.2, y - 1.6, y + 1.6, top, top + 0.6))
    small += [_b(-28, -23, 29, 34, top, top + 1.0),               # buck regulator
              _b(-38, -32, 2, 7, top, top + 1.2),                 # SPI flash
              _b(46, 51, 5, 9, top, top + 2.2)]                   # TVS diode
    ind = _b(-32, -24, 37, 45, top, top + 4.5)
    small.append(_fillet_try(ind, _zedges(ind), [1.0, 0.5]))
    add("Supporting electronics", _union(small), C_CHIP, "plastic", 15, "internal", E_PCB)
    caps = []
    for (x, y, r, h) in [(-5.0, 30.0, 4.0, 9.0), (-5.0, 40.5, 4.0, 9.0), (4.0, -30.0, 3.2, 7.0)]:
        c = _zcyl(x, y, top, top + h, r)
        c = _fillet_try(c, _top(c), [0.6, 0.3])
        c -= _b(x - r, x + r, y - 0.2, y + 0.2, top + h - 0.3, top + h + 1)     # vent score
        caps.append(c)
    add("Capacitors", _union(caps), C_METAL, "metal", 15, "internal", E_PCB)
    sleeves = [_zcyl(x, y, top, top + h - 1.2, r + 0.1) - _zcyl(x, y, top - 1, top + h, r - 0.2)
               for (x, y, r, h) in [(-5.0, 30.0, 4.0, 9.0), (-5.0, 40.5, 4.0, 9.0), (4.0, -30.0, 3.2, 7.0)]]
    add("Capacitor sleeves", _union(sleeves), "#1E3A5F", "plastic", 15, "internal", E_PCB)

    # silkscreen (thin raised marks): name block and connector legends
    silk = [_b(0, 30, -24, -21.5, top, top + 0.05), _b(0, 18, -19.5, -18.3, top, top + 0.05),
            _b(21, 30, -19.5, -18.3, top, top + 0.05),
            _b(-62, -56, -40, -38.8, top, top + 0.05), _b(-62, -56, 24, 25.2, top, top + 0.05)]
    for x in (-60.0, -45.0, -30.0):
        silk.append(_b(x, x + 10, -36, -35.4, top, top + 0.05))
    add("Silkscreen markings", _union(silk), C_SILK, "paper", 2, "internal", E_PCB)

    # one three-colour status light on the board, lit green (BOM 15, decided 2026-10-02), from model.py
    lx, ly = P["led_xy"]; ll, lw_, lh = P["led"]
    add("Status light housing, white", _b(lx - ll / 2, lx + ll / 2, ly - lw_ / 2, ly + lw_ / 2, top, top + lh - 0.3),
        "#F1F1EE", "plastic", 15, "internal", E_PCB)
    add("Status light, three-colour (lit green)", _b(lx - 1.2, lx + 1.2, ly - 1.0, ly + 1.0, top + lh - 0.3, top + lh),
        C_LED_G, "emissive", 15, "internal", E_PCB)

    # balance connector header (BOM 10): body of model.py, with the mating socket on the -X face
    bal = _b(-74, -65, -24, 20, top, top + 9.0)
    bal = _fillet_try(bal, _top(bal), [0.8, 0.4])
    bal -= _b(-75, -72, -22.5, 18.5, top + 1.5, top + 7.5)
    add("Balance connector, 17-way", bal, C_DARK, "plastic", 10, "internal", E_PCB)
    # CAN and UART connector (BOM 12): body of model.py
    comm = m[12]
    comm = _fillet_try(comm, _top(comm), [0.8, 0.4])
    comm -= _b(-85, -82, 27.5, 38.5, top + 1.2, top + 5.8)
    add("CAN and UART connector, 6-way", comm, C_DARK, "plastic", 12, "internal", E_PCB)

    # ------------------------------------------------------------ power studs, nuts (BOM 9)
    studs, nuts, washers = [], [], []
    sx = P["stud_x"]
    for y in P["stud_y"]:
        base = _hex_z(sx, y, top, 2 * P["stud_base_r"] * 0.866 * 1.0, 6.0)
        base = _fillet_try(base, _top(base), [0.6, 0.3])
        s = base + _zcyl(sx, y, top + 6.0, top + P["stud_h"], P["stud_d"] / 2)
        s = _fillet_try(s, _top(s), [0.5, 0.3])
        for k in range(8):
            zk = top + 12.6 + 0.9 * k
            s -= _zcyl(sx, y, zk, zk + 0.35, 3.4) - _zcyl(sx, y, zk - 1, zk + 1, 2.65)
        studs.append(s)
        zw = d["stud_face"] + {P["stud_y"][3]: P["link_t"], P["stud_y"][0]: 1.5}.get(y, 0.0)  # link (B+), lug (B-)
        washers.append(_zcyl(sx, y, zw, zw + 1.0, 6.0) - _zcyl(sx, y, zw - 1, zw + 2, 3.2))
        nuts.append(_nut(sx, y, zw + 1.0, 10.0, 5.0))
    add("Power terminal studs, M6 brass (B-, P-, P+, B+)", _union(studs), C_BRASS, "metal", 9, "shell", E_STUD)
    add("Stud washers", _union(washers), C_METAL, "metal", 9, "shell", E_NUT)
    add("Stud nuts", _union(nuts), C_METAL, "metal", 9, "shell", E_NUT)

    # ------------------------------------------------------------ pack fuse and holder (BOM 8), copper link (BOM 18)
    fx0, fl, fw, fy = P["fuse_x0"], P["fuse_l"], P["fuse_w"], P["fuse_y"]
    fx1 = fx0 + fl
    ht = d["holder_top"]                                           # holder top, where the fuse blades sit
    t0, t1 = d["fuse_term"]                                        # inner (link) and outer (B+ cable) terminals
    holder = _b(fx0, fx1, fy - fw / 2, fy + fw / 2, T, ht)
    holder = _fillet_try(holder, _zedges(holder), [4.0, 3.0, 2.0])
    holder = _fillet_try(holder, _top(holder), [1.0, 0.6])
    HS = holder_screws(P)
    for xs, ys in HS:
        holder -= _zcyl(xs, ys, ht - 1.5, ht + 1, 3.6)              # screw counterbores
        holder -= _zcyl(xs, ys, T - 1, ht + 1, 2.2)
    add("Fuse holder", holder, C_DARK, "plastic", 8, "shell", E_FUSE)
    hs = _union([_screw(xs, ys, ht - 1.5, 3.2, 2.0) for xs, ys in HS])
    add("Fuse holder screws", hs, C_METAL, "metal", 17, "shell", E_FUSE)
    body = _xcyl((t0 + t1) / 2, fy, ht + 9.0, 7.0, (t1 - 7) - (t0 + 7))
    body = _fillet_try(body, body.edges(), [1.0, 0.6])
    add("Pack fuse, 60 A", body, C_FUSE, "plastic", 8, "shell", E_FUSE)
    flab = _b(t0 + 11, t1 - 11, fy - 4, fy + 4, ht + 15.9, ht + 16.1)
    add("Fuse rating label", flab, "#B45309", "paper", 8, "shell", E_FUSE)
    tabs = (_b(t0 - 6, t0 + 8, fy - 6, fy + 6, ht, ht + 2.0) - _zcyl(t0, fy, ht - 1, ht + 3, 4.25)) + \
           (_b(t1 - 8, t1 + 6, fy - 6, fy + 6, ht, ht + 2.0) - _zcyl(t1, fy, ht - 1, ht + 3, 4.25))
    add("Fuse blades", tabs, C_METAL, "metal", 8, "shell", E_FUSE)
    fb = []
    for xt in (t0, t1):
        sb = _zcyl(xt, fy, ht, ht + 15.0, 4.0)
        fb.append(_fillet_try(sb, _top(sb), [0.6, 0.3]))
    add("Fuse terminal studs, M8", _union(fb), C_BRASS, "metal", 8, "shell", E_FNUT)
    lt = P["link_t"]
    fn = _union([_nut(t0, fy, ht + 2.0 + lt, 13.0, 6.5), _nut(t1, fy, ht + 2.0 + 1.5, 13.0, 6.5)])
    add("Fuse terminal nuts", fn, C_METAL, "metal", 8, "shell", E_FNUT)
    link = C["link"]
    add("Fuse link, copper bar", link, C_COPPER, "metal", 18, "shell", E_FNUT)
    sb_ = P["stud_y"][3]
    sleeve = _b(P["stud_x"] + 8, t0 - 9, sb_ - P["link_w"] / 2 - 0.4, sb_ + P["link_w"] / 2 + 0.4,
                d["stud_face"] - 0.4, d["stud_face"] + lt + 0.4)
    add("Fuse link heat-shrink sleeve", sleeve, C_RED, "rubber", 18, "shell", E_FNUT)

    # ------------------------------------------------------------ opaque cover on four pillars (BOM 13), light pipe (BOM 19)
    cx0, cx1, cw, ct, wl = P["cover_x0"], P["cover_x1"], P["cover_w"] / 2, P["cover_top"], P["cover_wall"]
    zb = T + P["cover_lift"]
    outer = _b(cx0, cx1, -cw, cw, zb, ct)
    outer = _fillet_try(outer, _zedges(outer), [6.0, 4.0, 3.0])
    outer = _fillet_try(outer, _top(outer), [2.0, 1.5, 1.0])
    inner = _b(cx0 + wl, cx1 - wl, -cw + wl, cw - wl, zb - 1, ct - wl)
    inner = _fillet_try(inner, _zedges(inner), [4.0, 2.5, 1.5])
    cover = outer - inner
    cover -= _b(cx0 - 1, cx0 + 3, -26, 42, zb - 1, top + 11.0)        # connector notch, open at the bottom (model.py)
    cover -= _b(cx1 - 3, cx1 + 1, -cw + 3, cw - 3, zb - 1, top + 1.0)  # board pass-through, open at the bottom
    cover -= _b(-38, -30, -cw - 1, -cw + 3, zb - 1, top + 5.0)        # probe lead notch, open at the bottom
    CS = [(x, y) for x, y, kind in P["pcb_fix"] if kind == "pillar"]
    for (x, y) in CS:
        cover -= _zcyl(x, y, ct - wl - 1, ct + 1, 1.7)
    cover -= _zcyl(lx, ly, ct - wl - 1, ct + 1, P["lp_hole"] / 2)    # light pipe hole
    add("Flame-retardant cover, opaque printed", cover, C_COVER, "plastic", 13, "shell", E_COVER)
    add("Cover screws", _union([_screw(x, y, ct) for (x, y) in CS]), C_METAL, "metal", 17, "shell", E_CSCREW)
    lp = C["light_pipe"]
    add("Light pipe, clear", lp, C_CLEAR, "clear", 19, "shell", E_COVER)
    glow = _zcyl(lx, ly, ct + P["lp_flange_t"], ct + P["lp_flange_t"] + 0.15, P["lp_d"] / 2)
    add("Light pipe tip, lit green", glow, C_LED_G, "emissive", 19, "shell", E_COVER)

    plate_lab = _b(-62, -22, 32, 42, ct, ct + 0.3)
    plate_lab = _fillet_try(plate_lab, _zedges(plate_lab), [1.5, 0.8])
    add("Cover name plate", plate_lab, C_ACCENT, "painted", 13, "shell", E_COVER)
    ink = _union([_b(-58, -38, 36.2, 39.2, ct + 0.3, ct + 0.45), _b(-58, -30, 34.0, 35.0, ct + 0.3, ct + 0.45)])
    add("Name plate print", ink, C_LABEL, "paper", 13, "shell", E_COVER)
    wlab = _b(8, 44, -44, -28, ct, ct + 0.3)
    wlab = _fillet_try(wlab, _zedges(wlab), [1.0, 0.5])
    add("Warning label", wlab, C_LABEL, "paper", 13, "shell", E_COVER)
    wink = _union([_b(10.5, 17.5, -41.5, -30.5, ct + 0.3, ct + 0.45), _b(20, 42, -33, -31.5, ct + 0.3, ct + 0.45),
                   _b(20, 38, -36.5, -35.3, ct + 0.3, ct + 0.45), _b(20, 40, -40, -38.8, ct + 0.3, ct + 0.45)])
    add("Warning label print", wink, "#B45309", "paper", 13, "shell", E_COVER)

    # ------------------------------------------------------------ mating plugs (accessory)
    bplug = _b(-90, -74, -23, 19, top + 1.0, top + 8.0)
    bplug = _fillet_try(bplug, _zedges(bplug), [1.2, 0.6])
    bplug += _b(-73.9, -72.1, -22.3, 18.3, top + 1.6, top + 7.4)      # nose in the header socket
    for k in range(6):
        bplug -= _b(-88 + 2.2 * k, -87.2 + 2.2 * k, -21, 17, top + 7.6, top + 8.5)   # grip ribs
    bplug += _b(-80, -76, -4, 0, top + 8.0, top + 9.2)                # latch
    add("Balance plug, 17-way", bplug, C_BLACK, "plastic", 10, "accessory", E_PLUG)
    cplug = _b(-96, -84, 27, 39, top + 0.8, top + 6.6)
    cplug = _fillet_try(cplug, _zedges(cplug), [1.0, 0.5])
    cplug += _b(-84.2, -82.2, 27.7, 38.3, top + 1.4, top + 5.6)
    cplug += _b(-92, -88, 31, 35, top + 6.6, top + 7.6)
    add("CAN and UART plug, 6-way", cplug, C_BLACK, "plastic", 12, "accessory", E_PLUG)

    # ------------------------------------------------------------ context: compact 4S pack
    cells, caps_, vents, terms, bus, tnuts = [], [], [], [], [], []
    ys = [-1.5 * CELL_T + CELL_T * k for k in range(4)]          # cell centres in Y (front to back)
    N, F = PCX + TERM_DX, PCX - TERM_DX                           # near (board side) and far terminal X
    ct_top = CELL_H + TOP_CAP
    for y in ys:
        c = _b(PCX - CELL_W / 2, PCX + CELL_W / 2, y - CELL_T / 2 + 0.3, y + CELL_T / 2 - 0.3, 0, CELL_H)
        cells.append(_fillet_try(c, _zedges(c), [1.5, 1.0]))
        caps_.append(_b(PCX - CELL_W / 2 + 1, PCX + CELL_W / 2 - 1, y - CELL_T / 2 + 1, y + CELL_T / 2 - 1,
                        CELL_H, ct_top))
        vents.append(_zcyl(PCX, y, ct_top, ct_top + 0.4, 5.0))
        for x in (N, F):
            terms.append(_zcyl(x, y, ct_top, 104.0, 6.0))
    add("LiFePO4 cells (4), illustrative", _union(cells), C_CELL, "plastic", None, "context", (0, 0, 0))
    add("Cell top caps", _union(caps_), C_CELLTOP, "plastic", None, "context", (0, 0, 0))
    add("Cell vents", _union(vents), "#9CA3AF", "metal", None, "context", (0, 0, 0))
    add("Cell terminals", _union(terms), C_METAL, "metal", None, "context", (0, 0, 0))
    # series busbars: far side joins cells 0-1 and 2-3, near side joins 1-2; end pads at B- and B+
    for (x, ya, yb) in [(F, ys[0], ys[1]), (N, ys[1], ys[2]), (F, ys[2], ys[3])]:
        bb = _b(x - 10, x + 10, ya - 8, yb + 8, 104.0, 106.0)
        bus.append(_fillet_try(bb, _zedges(bb), [3.0, 1.5]))
    for y in (ys[0], ys[3]):
        pd = _b(N - 10, N + 10, y - 8, y + 8, 104.0, 106.0)
        bus.append(_fillet_try(pd, _zedges(pd), [3.0, 1.5]))
    add("Busbars", _union(bus), "#C9CDD2", "metal", None, "context", (0, 0, 0))
    lug_sites = {(N, ys[0]), (N, ys[3]), (F, ys[1]), (N, ys[2]), (F, ys[3]), (N, ys[1]), (F, ys[0])}
    for x in (N, F):
        for y in ys:
            z0 = 108.0 if (x, y) in lug_sites else 106.0
            tnuts.append(_nut(x, y, z0, 10.0, 5.0) + _zcyl(x, y, 104.0, z0 + 6.0, 2.6))
    add("Terminal nuts", _union(tnuts), C_METAL, "metal", None, "context", (0, 0, 0))
    yend = 2 * CELL_T
    ends = []
    for s in (-1, 1):
        y0, y1 = (-yend - END_T, -yend) if s < 0 else (yend, yend + END_T)
        e = _b(PCX - CELL_W / 2 + 2, PCX + CELL_W / 2 - 2, y0, y1, 2, CELL_H - 4)
        ends.append(_fillet_try(e, e.edges(), [1.5, 1.0]))
    add("Pack end plates", _union(ends), C_ENDPL, "plastic", None, "context", (0, 0, 0))
    plab = _b(PCX - 40, PCX + 40, -yend - END_T - 0.3, -yend - END_T, 30, 62)
    add("Pack label", plab, C_LABEL, "paper", None, "context", (0, 0, 0))
    pink = _union([_b(PCX - 34, PCX - 4, -yend - END_T - 0.5, -yend - END_T - 0.3, 50, 56),
                   _b(PCX - 34, PCX + 30, -yend - END_T - 0.5, -yend - END_T - 0.3, 43, 45),
                   _b(PCX - 34, PCX + 18, -yend - END_T - 0.5, -yend - END_T - 0.3, 37, 39)])
    add("Pack label print", pink, C_DARK, "paper", None, "context", (0, 0, 0))
    straps = []
    for zc in (24.0, 70.0):
        so = _b(PCX - CELL_W / 2 - 1.2, PCX + CELL_W / 2 + 1.2, -yend - END_T - 1.2, yend + END_T + 1.2,
                zc - 8, zc + 8)
        so = _fillet_try(so, _zedges(so), [3.0, 2.0])
        si = _b(PCX - CELL_W / 2 + 0.2, PCX + CELL_W / 2 - 0.2, -yend - END_T + 0.2, yend + END_T - 0.2,
                zc - 9, zc + 9)
        si = _fillet_try(si, _zedges(si), [1.5, 1.0])
        straps.append(so - si)
    add("Pack straps (woven polyester)", _union(straps), C_STRAP, "fabric", None, "context", (0, 0, 0))

    # ------------------------------------------------------------ context: harness and cables
    zl = 108.0                                                     # balance lug level
    blugs = []
    # (terminal, lug tongue direction) for V0 .. V4
    vt = [((N, ys[0]), (0, 1)), ((F, ys[1]), (1, 0)), ((N, ys[2]), (1, 0)),
          ((F, ys[3]), (1, 0)), ((N, ys[3]), (0, -1))]
    for (x, y), (dx, dy) in vt:
        blugs.append(_lug(x, y, zl - 1.0, 0.8, 4.8, 3.2, dx * 7, dy * 7, 3.0))
    add("Balance lead ring lugs", _union(blugs), C_METAL, "metal", 10, "context", (0, 0, 0))
    rl = 1.2
    tip = lambda x, y, dx, dy: (x + dx * 9.5, y + dy * 9.5, zl - 0.6)
    sl_end = (-138.0, 0.0, 114.0)
    routes = [
        [(-138, -5, 114), (-150, -22, 113), (N, -28 + 0.0, 111), tip(N, ys[0], 0, 1)],
        [(-138, -2.5, 114), (-150, -27, 113), (F + 16, -27, 112), (F + 12, ys[1], 110), tip(F, ys[1], 1, 0)],
        [(-138, 0, 114), (-146, 8, 112), (N + 12, ys[2], 110), tip(N, ys[2], 1, 0)],
        [(-138, 2.5, 114), (-150, 27, 113), (F + 16, 27, 112), (F + 12, ys[3], 110), tip(F, ys[3], 1, 0)],
        [(-138, 5, 114), (-150, 22, 113), (N, 28, 111), tip(N, ys[3], 0, -1)],
    ]
    leads = _union([_pipe(r, rl) for r in routes])
    add("Balance leads (4S uses 5 of 17)", leads, C_LEAD, "plastic", 10, "context", (0, 0, 0))
    sleeve = _pipe([(-90.5, -2, top + 4.5), (-104, -2, top + 6), (-118, -1, 60), (-126, 0, 104), sl_end], 4.6)
    add("Balance harness braided sleeve", sleeve, C_BLACK, "fabric", 10, "context", (0, 0, 0))

    # temperature probes: ring-lug NTC probes on two cell terminals (BOM 11)
    plugs = [_lug(N, ys[1], zl - 1.0, 0.8, 4.8, 3.2, 7, 0, 3.0), _lug(F, ys[0], zl - 1.0, 0.8, 4.8, 3.2, 7, 0, 3.0)]
    beads = [Pos(N + 11, ys[1], zl) * Sphere(2.4), Pos(F + 11, ys[0], zl) * Sphere(2.4)]
    add("Temperature probe lugs", _union(plugs), C_METAL, "metal", 11, "context", (0, 0, 0))
    add("Temperature probe beads", _union(beads), C_BLACK, "plastic", 11, "context", (0, 0, 0))
    p1 = [(-36, -45, top + 2.8), (-36, -60, top + 2.8), (-86, -63, 18), (-120, -57, 90),
          (-134, -30, 113), (N + 22, ys[1], 111), (N + 12.5, ys[1], zl)]
    p2 = [(-32, -45, top + 2.8), (-32, -64, top + 2.8), (-88, -67, 18), (-122, -61, 90),
          (-136, -52, 112), (F + 26, -52, 112), (F + 14, ys[0] - 6, 110), (F + 12.5, ys[0], zl)]
    add("Temperature probe leads", _pipe(p1, 0.9) + _pipe(p2, 0.9), C_PROBE, "plastic", 11, "context", (0, 0, 0))

    # power cables, 10 mm2 silicone, with ring lugs (BOM 16, 9)
    rc = 3.6
    zp = 106.0                                                     # power lug level on the pack
    zs = top + 6.0                                                 # stud lug level (on the stud base)
    zf = ht + 2.0                                                  # outer fuse blade face, B+ cable lug
    plugs_p = [_lug(N, ys[0], zp, 1.5, 6.5, 3.3, 12, 0, 7.0), _lug(N, ys[3], zp, 1.5, 6.5, 3.3, 12, 0, 7.0),
               _lug(sx, -33.0, zs, 1.5, 6.5, 3.3, 0, -11, 7.0),
               _lug(t1, fy, zf, 1.5, 6.8, 4.3, 12, 0, 8.0)]
    add("Power cable ring lugs", _union(plugs_p), "#C9CDD2", "metal", 9, "context", (0, 0, 0))
    neg = _pipe([(N + 20, ys[0], zp + 0.8), (-134, ys[0] - 2, zp), (-126, -46, 96), (-117, -52, 58),
                 (-110, -64, rc), (40, -64, rc), (56, -64, 6), (sx, -58, zs + 0.8), (sx, -46.5, zs + 0.8)], rc)
    add("B- power cable (black)", neg, C_BLACK, "rubber", 16, "context", (0, 0, 0))
    pos = _pipe([(N + 20, ys[3], zp + 0.8), (-134, ys[3] + 2, zp), (-126, 46, 96), (-117, 52, 58),
                 (-110, 64, rc), (140, 64, rc), (152, 54, rc + 2), (154, fy + 4, zf + 0.8), (t1 + 16, fy, zf + 0.8)], rc)
    add("B+ power cable to the fuse holder (red)", pos, C_RED, "rubber", 16, "context", (0, 0, 0))
    shr = [_pipe([(sx, -54, zs + 0.8), (sx, -49.5, zs + 0.8)], rc + 0.5),
           _pipe([(N + 16, ys[0], zp + 0.8), (N + 21, ys[0], zp + 0.8)], rc + 0.5)]
    add("Heat-shrink boots, B-", _union(shr), C_BLACK, "rubber", 16, "context", (0, 0, 0))
    shr = [_pipe([(N + 16, ys[3], zp + 0.8), (N + 21, ys[3], zp + 0.8)], rc + 0.5),
           _pipe([(t1 + 14, fy, zf + 0.8), (t1 + 19, fy, zf + 0.8)], rc + 0.5)]
    add("Heat-shrink boots, B+", _union(shr), C_RED, "rubber", 16, "context", (0, 0, 0))

    # CAN and UART cable to the host, leaving over the back of the mat
    can = _pipe([(-96, 33, top + 3.7), (-106, 33, top + 3.7), (-114, 52, 2.5), (-122, 70, 2.5),
                 (-175, 74, 2.5), (-185, 90, -18)], 2.5)
    add("CAN and UART cable", can, C_DARK, "rubber", 12, "context", (0, 0, 0))

    # bench mat
    mx0, mx1, my0, my1, mt = MAT
    mat = _b(mx0, mx1, my0, my1, -mt, 0)
    mat = _fillet_try(mat, _zedges(mat), [10.0, 6.0])
    mat = _fillet_try(mat, _top(mat), [1.0, 0.5])
    add("Bench mat", mat, C_MAT, "rubber", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:48s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
