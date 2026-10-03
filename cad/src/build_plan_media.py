"""CellGuard prototype build plan pictures (CGD-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CGD-DWG-101 to 105        making sketches for the made components
    docs/05-build-plan/plate-holes.png     hole positions on the base plate (matplotlib)
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining (joint7: light pipe)
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          how the board connects to the pack, load and host (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-09-30"
DATE2 = "2026-10-02"                 # status light and light pipe (CGD-DEC-001)
REV_P2 = [("P1", "Making sketch for the prototype build plan", DATE, "AC"),
          ("P2", "Status light and light pipe added (CGD-DEC-001)", DATE2, "AC")]
D = derived(P)
C = {k: v[0] for k, v in build_components(P).items()}

COL = {"plate": "#A8A29E", "pad": "#F59E0B", "spacers": "#6B7280", "pcb_screws": "#111827", "pcb": "#15803D",
       "afe": "#111827", "fets": "#374151", "shunt": "#B45309", "mcu": "#0F766E", "pre": "#D4A017",
       "studs": "#CA8A04", "bal_header": "#1F2937", "harness": "#334155", "ntc_board": "#0369A1",
       "probes": "#38BDF8", "comm": "#6B7280", "can_plug": "#4B5563", "sec": "#DC2626", "pillars": "#9CA3AF",
       "nuts": "#111827", "fuse": "#C2410C", "holder_screws": "#111827", "link": "#B87333", "cover": "#475569",
       "cover_screws": "#111827", "led": "#22C55E", "light_pipe": "#E5E7EB"}
BOARD = ("pcb", "afe", "fets", "shunt", "mcu", "pre", "studs", "bal_header", "ntc_board", "comm", "sec", "led")


def S(*ks):
    out = None
    for k in ks:
        out = C[k] if out is None else out + C[k]
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def mv(p, e):
    return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)


def made():
    return {
        "plate": part("Base plate", C["plate"], COL["plate"]),
        "pad": part("Gap pad", C["pad"], COL["pad"]),
        "fix": part("Board screws and spacers (6)", S("pcb_screws", "spacers"), COL["spacers"]),
        "board": part("Main board, populated", S(*BOARD), COL["pcb"]),
        "pillars": part("Pillars (4) and nuts (2)", S("pillars", "nuts"), COL["pillars"]),
        "fuse": part("Fuse holder, fuse and 4 screws", S("fuse", "holder_screws"), COL["fuse"]),
        "link": part("Fuse link", C["link"], COL["link"]),
        "probes": part("Temperature probe leads (2)", C["probes"], COL["probes"]),
        "cover": part("Cover, light pipe and 4 screws", S("cover", "cover_screws", "light_pipe"), COL["cover"]),
        "harness": part("Balance harness plug", C["harness"], "#7C3AED"),
        "can": part("CAN and UART plug (host side)", C["can_plug"], "#0EA5E9"),
    }


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"plate": (0, 0, -60), "pad": (0, 0, -25), "fix": (0, 0, 0), "board": (0, 0, 40), "pillars": (0, 0, 85),
           "fuse": (120, 0, -45), "link": (40, 0, 110), "probes": (0, -60, 40), "cover": (0, 0, 160),
           "harness": (-130, 0, -10), "can": (-130, 0, 45)}
    parts = []
    for k in ("plate", "pad", "fix", "board", "pillars", "fuse", "link", "probes", "cover", "harness", "can"):
        p = M[k]; p.explode = off[k]; parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CellGuard prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the power end, front right and above",
                       elev=24, azim=-50, size=(11, 8), dpi=150)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    """only: drawing numbers to draw (for example ("103", "104")); all five when None."""
    M = made()
    base = dict(project="CellGuard", date=DATE)
    out = []

    def cs(prt, nb, **kw):
        if only and kw["dwg_no"][-3:] not in only:
            return None
        return bv.component_sheet(prt, nb, **kw)
    # 101 base plate
    out.append(cs(
        Part("Base plate", C["plate"], COL["plate"]), [M["pad"], M["fuse"], M["fix"]],
        dwg_no="CGD-DWG-101", title="CellGuard base plate: making sketch", material="Aluminium sheet 4 mm, 6061 class",
        inset_view=(30, -55),
        notes=["Blank 220 x 110 mm, 4 mm aluminium, square; round the corners 3 mm.",
               "Sizes from the signal end (left edge) and the centre line.",
               "Board fixings: six 3.4 mm holes, countersunk 90 degrees from",
               "  the BOTTOM face to 6.6 mm so M3 countersunk heads sit flush:",
               "  17 from the left edge 40 each side; 133 in, 44 each side;",
               "  156.5 in, 43.5 each side.",
               "Fuse holder: four M4 tapped holes (drill 3.3) at 178 and 212 in,",
               "  21 and 45 to the B+ side of the centre line.",
               "Mounting: four M4 tapped holes (drill 3.3) at 30 and 167 in,",
               "  30 each side. Screws come up from below and stop in the plate.",
               "Deburr every hole; the top face must stay flat within 0.1 mm",
               "  under the gap pad (it carries the MOSFET heat).",
               "Check: lay the board on it; all six holes line up with the board's."],
        **base))
    # 102 gap pad
    out.append(cs(
        Part("Gap pad", C["pad"], COL["pad"]), [M["plate"], M["fix"]],
        dwg_no="CGD-DWG-102", title="CellGuard gap pad: cutting sketch", material="Insulating gap pad 1.0 mm, 3 W/m.K",
        inset_view=(35, -55),
        notes=["Cut one piece 55 x 44 mm from 1.0 mm insulating gap pad sheet",
               "  with a sharp knife on a cutting mat; keep the liner on.",
               "Drawn at 0.7 mm: the thickness it is squeezed to in place.",
               "It lies on the plate under the eight MOSFETs: from 100 to 155 mm",
               "  in from the plate's left edge, centred across the plate.",
               "Peel one liner, press it onto the clean plate, then peel the",
               "  other liner just before the board goes on.",
               "Do not stretch it; replace it if it tears or picks up a chip:",
               "  it is the only insulation between the MOSFETs and the plate.",
               "Check: no bubbles; 55 x 44 mm within 1 mm."],
        **base))
    # 103 main board (outline and fixed positions; the layout is TRL 4 work)
    board = S(*BOARD)
    out.append(cs(
        Part("Main board", board, COL["pcb"]), [M["plate"], M["fix"], M["pillars"], M["fuse"]],
        dwg_no="CGD-DWG-103", title="CellGuard main board: outline and fixed positions", material="FR-4 1.6 mm, 4 layers, 2 oz copper",
        view_shape=board, inset_view=(30, -55),
        notes=["Ordered from a board maker; the copper layout is drawn at TRL 4",
               "  and must keep every position on this sheet.",
               "Outline 150 x 95 mm, 1.6 mm. Six 3.4 mm unplated holes with a",
               "  3 mm copper-free ring, at the plate's six board fixings.",
               "Underside: eight MOSFETs in two rows of four, 14 mm each side of",
               "  the centre line, 22, 36, 50 and 63 mm right of the board centre.",
               "Top, power end: four M6 stud terminals 66 mm right of centre,",
               "  B-, P-, P+, B+ at 33 and 11 mm each side (B+ on the far side).",
               "Top, signal end: balance header and CAN and UART connector at the",
               "  left edge; the CAN connector overhangs the edge by 5 mm.",
               "Top: three-colour status light 30 mm left of the board centre,",
               "  20 mm to the B+ side, under the cover's light pipe.",
               "Solder fine-pitch parts on a hot plate, then the MOSFETs from below,",
               "  then the stud terminals and connectors by hand.",
               "Check: MOSFET tops level within 0.1 mm; stud pins trimmed to",
               "  1 mm under the board."],
        rev="P2", revisions=REV_P2, **{**base, "date": DATE2}))
    # 104 cover
    out.append(cs(
        Part("Cover", C["cover"], COL["cover"]), [M["board"], M["pillars"], M["plate"],
                                                  part("Light pipe", C["light_pipe"], COL["light_pipe"])],
        dwg_no="CGD-DWG-104", title="CellGuard cover: making sketch", material="Flame-retardant polycarbonate, opaque, printed, 2 mm wall",
        view_shape=C["cover"], inset_view=(30, -55),
        notes=["Print upside down (top face on the bed), 2 mm walls, 100 % infill,",
               "  in flame-retardant polycarbonate in an enclosed printer.",
               "Outside 134 x 104 x 26.1 mm, open at the bottom.",
               "Four 3.4 mm holes in the top over the pillars: 12 mm from the",
               "  signal end 40 each side, and 128 mm from it 44 each side.",
               "Signal-end notch 68 wide, from 26 below to 42 above the centre",
               "  line, open at the bottom, 15.1 mm tall: the connectors and",
               "  harness sit in it. Power-end notch 98 wide, 5.1 mm tall, open",
               "  at the bottom: the board passes under it with 1 mm clear.",
               "Probe notch 8 wide, 9.1 mm tall, in the near side wall.",
               "Light pipe hole 3.2 mm in the top, 50 mm from the signal end,",
               "  20 to the B+ side: press the flanged 3 mm light pipe in from",
               "  above; its foot stops 0.5 mm over the status light.",
               "Fit: it rests on the four pillars only; its walls stand 0.5 mm",
               "  clear of the plate. Four M3 x 6 pan-head screws.",
               "Check: on the pillars it does not rock and touches no part."],
        rev="P2", revisions=REV_P2, **{**base, "date": DATE2}))
    # 105 fuse link
    out.append(cs(
        Part("Fuse link", C["link"], COL["link"]), [M["board"], M["fuse"], M["plate"]],
        dwg_no="CGD-DWG-105", title="CellGuard fuse link: making sketch", material="Copper flat bar 14 x 3 mm, C101 or C110",
        view_shape=C["link"], inset_view=(40, -40),
        notes=["Cut 41 mm of 14 x 3 mm copper bar; file both ends to a 7 mm",
               "  radius, centred on the hole centres.",
               "Holes on the centre line, 27 mm apart: 6.5 mm at one end (B+",
               "  stud, M6), 8.5 mm at the other (fuse holder terminal, M8).",
               "Deburr; clean both faces bright with an abrasive pad.",
               "Slide 20 mm of heat-shrink over the middle and shrink it; leave",
               "  the ends bare where they clamp.",
               "Fit: lies flat on the B+ stud's shoulder and on the fuse blade",
               "  at the holder's inner terminal, both 10.6 mm above the plate top.",
               "  An M6 and an M8 nut with spring washers hold it.",
               "It carries the full pack current: both faces must be clean and",
               "  flat where they touch.",
               "Check: drops over both studs without bending."],
        **base))
    return out


# ----------------------------------------------------------------- hole layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    x0 = P["plate_x0"]; L, W = P["plate_l"], P["plate_w"]
    fig = plt.figure(figsize=(12, 7.5), dpi=150)
    ax = fig.add_axes([0.05, 0.1, 0.66, 0.78]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, -W / 2), L, W, fc="#F5F5F4", ec=INK, lw=1.2))
    ax.plot([-2, L + 2], [0, 0], color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    ax.add_patch(Rectangle((P["pad"][0] - x0, P["pad"][2]), P["pad"][1] - P["pad"][0], P["pad"][3] - P["pad"][2],
                           fc="#FDE68A", ec="#B45309", lw=0.6, ls="--"))
    ax.text(P["pad"][0] - x0 + 27.5, 11, "gap pad here\n(top face, flat)", ha="center", va="center", fontsize=7.5, color="#92400E")
    fx0 = P["fuse_x0"] - x0
    ax.add_patch(Rectangle((fx0, P["fuse_y"] - 16), P["fuse_l"], 32, fc="none", ec="#C2410C", lw=0.6, ls="--"))
    ax.text(fx0 + 22, P["fuse_y"], "fuse holder", ha="center", va="center", fontsize=7.5, color="#C2410C")
    from model import holder_screws
    holes = [(x - x0, y, "csk") for x, y, _ in P["pcb_fix"]] + [(x - x0, y, "m4") for x, y in P["mount_holes"]] + \
            [(x - x0, y, "fuse") for x, y in holder_screws(P)]
    xs, ys = set(), set()
    for x, y, k in holes:
        if k == "csk":
            ax.add_patch(plt.Circle((x, y), 3.3, fc="none", ec=MUT, lw=0.6, ls="--"))
            ax.add_patch(plt.Circle((x, y), 1.7, fc="white", ec=INK, lw=1))
        else:
            ax.add_patch(plt.Circle((x, y), 1.65, fc="white", ec="#1D4ED8" if k == "m4" else "#C2410C", lw=1.1))
            ax.add_patch(plt.Circle((x, y), 2.0, fc="none", ec="#1D4ED8" if k == "m4" else "#C2410C", lw=0.5))
        ax.plot([x - 5, x + 5], [y, y], color=MUT, lw=0.4); ax.plot([x, x], [y - 5, y + 5], color=MUT, lw=0.4)
        xs.add(round(x, 1)); ys.add(round(y, 1))
    for i, x in enumerate(sorted(xs)):
        yl = -W / 2 - 6 - 7 * (i % 2)
        ax.plot([x, x], [-W / 2, yl + 2], color=AC, lw=0.4, ls=":")
        ax.text(x, yl, f"{x:g}", ha="center", va="top", fontsize=7.5, color=AC)
    ax.text(L / 2, -W / 2 - 22, "in from the signal-end (left) edge, mm", ha="center", fontsize=8, color=MUT)
    ty = []
    for y in sorted(ys):                       # spread close values so no two labels touch
        ty.append(max(y, ty[-1] + 5.5) if ty else y)
    for y, t in zip(sorted(ys), ty):
        ax.plot([-9, -3, 0], [t, y, y], color=AC, lw=0.4, ls=":")
        ax.text(-10, t, f"{y:+g}", ha="right", va="center", fontsize=7.5, color=AC)
    ax.text(-34, 0, "from the centre line, mm\n(+ toward the B+ side)", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.text(L + 3, W / 2 - 4, "power end", fontsize=8, color=MUT, va="top")
    ax.text(3, W / 2 + 3, "signal end", fontsize=8, color=MUT, va="bottom")
    ax.set_xlim(-44, L + 25); ax.set_ylim(-W / 2 - 28, W / 2 + 14)
    fig.text(0.03, 0.965, "Base plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.925, "Seen from the top (the face the board sits on). Figures in mm, taken from the model.", fontsize=8.5, color=MUT, va="top")
    key = [("Board fixings (6)", INK), ("  3.4 mm, countersunk 90 degrees", INK), ("  to 6.6 mm from the BOTTOM face", INK),
           ("  (dashed circle: the countersink)", MUT), ("", INK),
           ("Mounting holes (4)", "#1D4ED8"), ("  M4 tapped (drill 3.3), through;", "#1D4ED8"), ("  screws from below, stop in the plate", "#1D4ED8"), ("", INK),
           ("Fuse holder holes (4)", "#C2410C"), ("  M4 tapped (drill 3.3), through;", "#C2410C"), ("  screws from above through the holder", "#C2410C"), ("", INK),
           ("Dashed outlines: where the gap pad", MUT), ("  and the fuse holder go", MUT)]
    fig.text(0.74, 0.86, "What each hole is", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, (t, c) in enumerate(key):
        fig.text(0.74, 0.83 - i * 0.03, t, fontsize=8, color=c, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/cellguard", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "plate-holes.png"


# ----------------------------------------------------------------- joints
def joints():
    import build123d as b
    out = []

    def win(sh, x0, x1, y0, y1, z0, z1):
        return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))
    top = D["top"]
    # 01 board fixing under a pillar, cut through the screw axis
    bx = (-80, -56, 40, 49, -1, D["cover_top"] + 4)
    out.append(bv.joint([
        part("Base plate", win(C["plate"], *bx), COL["plate"]),
        part("Spacer, 3 mm", win(C["spacers"], *bx), COL["spacers"]),
        part("M3 countersunk screw from below", win(C["pcb_screws"], *bx), "#1F2937"),
        part("Main board", win(C["pcb"], *bx), COL["pcb"]),
        part("Pillar, 20 mm", win(C["pillars"], *bx), COL["pillars"]),
        part("Cover", win(C["cover"], *bx), COL["cover"]),
        part("M3 pan-head cover screw", win(C["cover_screws"], *bx), "#1F2937")],
        OUT / "joint-01.png", "Joint 1: board fixing under a pillar (signal end), cut through the screw",
        subtitle="One screw from below clamps plate, spacer and board; the pillar threads onto it and carries the cover",
        elev=12, azim=-80, size=(8, 6)))
    # 02 MOSFET on the gap pad, cut across a MOSFET
    bx = (14, 44, 14, 30, -0.5, top + 0.5)
    out.append(bv.joint([
        part("Base plate", win(C["plate"], *bx), COL["plate"]),
        part("Gap pad, 1.0 mm squeezed to 0.7 mm", win(C["pad"], *bx), COL["pad"]),
        part("MOSFETs, soldered under the board", win(C["fets"], *bx), COL["fets"]),
        part("Main board", win(C["pcb"], *bx), COL["pcb"])],
        OUT / "joint-02.png", "Joint 2: MOSFETs on the gap pad (cut across one row)",
        subtitle="The spacers set a 3 mm gap; the 2.3 mm MOSFETs squeeze the pad to 0.7 mm against the plate",
        elev=8, azim=-78, size=(8, 6)))
    # 03 power end: B+ stud, outer board fixing, SCP fuse
    bx = (54, 80, 24, 50, -0.5, top + 22)
    out.append(bv.joint([
        part("Base plate", win(C["plate"], *bx), COL["plate"]),
        part("Spacer and screw", win(C["spacers"] + C["pcb_screws"], *bx), COL["spacers"]),
        part("Main board", win(C["pcb"], *bx), COL["pcb"]),
        part("M3 nyloc nut", win(C["nuts"], *bx), "#1F2937"),
        part("B+ stud terminal, soldered", win(C["studs"], *bx), COL["studs"]),
        part("SCP fuse", win(C["sec"], *bx), COL["sec"])],
        OUT / "joint-03.png", "Joint 3: B+ stud and the outer board fixing (power end, B+ corner)",
        subtitle="The nut sits 2 mm clear of the stud shoulder and 1.3 mm clear of the SCP fuse",
        elev=35, azim=-60, size=(8, 6)))
    # 04 fuse holder and link
    bx = (52, 136, 20, 56, -0.5, 34)
    out.append(bv.joint([
        part("Base plate", win(C["plate"], *bx), COL["plate"]),
        part("Main board (power end)", win(C["pcb"], *bx), COL["pcb"]),
        part("B+ stud", win(C["studs"], *bx), COL["studs"]),
        part("Fuse holder and fuse", win(C["fuse"], *bx), COL["fuse"]),
        part("M4 screws into the plate, cut", win(C["holder_screws"], 52, 136, 20, 30, -0.5, 34), "#1F2937"),
        part("M4 screws, far side", win(C["holder_screws"], 52, 136, 38, 56, -0.5, 34), "#1F2937"),
        part("Copper fuse link", win(C["link"], *bx), COL["link"])],
        OUT / "joint-04.png", "Joint 4: fuse holder on the plate and the copper link to the B+ stud",
        subtitle="The stud shoulder and the fuse blade are at the same height, so the link is a straight flat bar",
        elev=30, azim=-70, size=(8, 6)))
    # 05 signal end: connectors in the cover notch
    bx = (-100, -50, -32, 48, -0.5, D["cover_top"] + 3)
    out.append(bv.joint([
        part("Base plate", win(C["plate"], *bx), COL["plate"]),
        part("Main board", win(C["pcb"], *bx), COL["pcb"]),
        part("Balance header", win(C["bal_header"], *bx), COL["bal_header"]),
        part("CAN and UART connector", win(C["comm"], *bx), "#D4A017"),
        part("Cover, notch open at the bottom", win(C["cover"], *bx), "#94A3B8"),
        part("Balance harness plug", win(C["harness"], -94, -50, -32, 48, 5, 20), "#7C3AED"),
        part("CAN and UART plug", win(C["can_plug"], *bx), "#0EA5E9")],
        OUT / "joint-05.png", "Joint 5: connectors in the cover's signal-end notch",
        subtitle="Seen from the signal end. The notch is open at the bottom so the cover drops over the connectors",
        elev=22, azim=-150, size=(8, 6)))
    # 06 probe lead notch
    bx = (-46, -24, -66, -36, -0.5, top + 7)
    out.append(bv.joint([
        part("Base plate", win(C["plate"], *bx), COL["plate"]),
        part("Main board", win(C["pcb"], *bx), COL["pcb"]),
        part("Probe header", win(C["ntc_board"], *bx), COL["ntc_board"]),
        part("Probe leads (2)", win(C["probes"], *bx), COL["probes"]),
        part("Cover side wall and notch", win(C["cover"], *bx), COL["cover"])],
        OUT / "joint-06.png", "Joint 6: temperature probe leads through the side notch",
        subtitle="Cover cut off above the notch. The leads plug in before the cover goes on; the cover drops over them",
        elev=42, azim=-110, size=(8, 6)))
    return out


def joint7():
    """Light pipe over the status light, cut through the light pipe axis (2026-10-02, CGD-DEC-001)."""
    import build123d as b
    top = D["top"]
    lx, ly = P["led_xy"]

    def win(sh, x0, x1, y0, y1, z0, z1):
        return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0))
    bx = (lx - 14, lx + 14, ly - 12, ly, D["pcb_z0"] - 0.5, D["cover_top"] + 2)
    return bv.joint([
        part("Main board", win(C["pcb"], *bx), COL["pcb"]),
        part("Status light, three-colour", win(C["led"], *bx), "#16A34A"),
        part("Light pipe, 3 mm, flanged", win(C["light_pipe"], *bx), "#93C5FD"),
        part("Cover top, opaque", win(C["cover"], *bx), COL["cover"])],
        OUT / "joint-07.png", "Joint 7: light pipe over the status light, cut through its axis",
        subtitle="Pressed into the cover from above; its foot stops 0.5 mm over the light, so the cover lifts off freely",
        elev=10, azim=-90, size=(8, 6))


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
    pcb = part("Bare board", C["pcb"], COL["pcb"])
    st(1, [pcb], [mv(part("Front end, protector, controller, status light", S("afe", "sec", "mcu", "led"), "#111827"), (0, 0, 40)),
                  mv(part("Shunt and precharge parts", S("shunt", "pre"), COL["pre"]), (0, 0, 55)),
                  mv(part("Connectors and probe header", S("bal_header", "comm", "ntc_board"), COL["comm"]), (0, 0, 70)),
                  mv(part("Stud terminals (4)", C["studs"], COL["studs"]), (0, 0, 60)),
                  mv(part("MOSFETs (8), from below", C["fets"], COL["fets"]), (0, 0, -40))],
       "populate the main board", "Hot plate for the fine-pitch parts; MOSFETs from below; studs and connectors last, by hand",
       elev=25, azim=-55, label_done=False)
    pl = M["plate"]
    st(2, [pl], [mv(M["pad"], (0, 0, 40))], "gap pad onto the base plate",
       "Clean the plate with alcohol; peel one liner, press the pad down; keep the top liner on for now",
       elev=30, azim=-55, label_done=True)
    st(3, [pl, M["pad"]], [mv(part("M3 countersunk screws, from below", C["pcb_screws"], "#1F2937"), (0, 0, -40)),
                           mv(part("Spacers, 3 mm", C["spacers"], COL["spacers"]), (0, 0, 40))],
       "board screws and spacers", "Push each screw up through its countersink and slip a spacer over it; tape the heads",
       elev=6, azim=-60, label_done=False)
    fix = [pl, M["pad"], M["fix"]]
    st(4, fix, [mv(M["board"], (0, 0, 60))], "main board onto the spacers",
       "Peel the pad liner; lower the board over the six screws so the MOSFETs land on the pad",
       elev=22, azim=-55, label_done=False)
    st(5, fix + [M["board"]], [mv(part("Pillars (4)", C["pillars"], "#2563EB"), (0, 0, 50)),
                               mv(part("Nyloc nuts (2)", C["nuts"], "#1F2937"), (0, 0, 40))],
       "pillars and nuts", "Pillars on the four inner screws, nuts on the two outer; tighten evenly to 0.5 N.m",
       elev=24, azim=-55, label_done=False)
    bd = fix + [M["board"], M["pillars"]]
    st(6, bd, [mv(part("Fuse holder (fuse drawn in place)", C["fuse"], COL["fuse"]), (0, 0, 50)),
               mv(part("M4 screws (4)", C["holder_screws"], "#1F2937"), (0, 0, 80))],
       "fuse holder onto the plate", "Four M4 x 12 screws into the tapped holes, 2 N.m. Fit the holder without its fuse; the fuse goes in last",
       elev=28, azim=-50, label_done=False)
    st(7, bd + [M["fuse"]], [mv(M["link"], (0, 0, 40))], "fuse link",
       "Over the B+ stud and the holder's inner terminal; M6 and M8 nuts with spring washers",
       elev=30, azim=-50, label_done=False)
    st(8, bd + [M["fuse"], M["link"]], [mv(M["probes"], (0, 0, 45))], "temperature probe leads",
       "Plug both probe leads into the probe header and lay them in line with the side notch",
       elev=26, azim=-70, label_done=False)
    st(9, bd + [M["fuse"], M["link"], M["probes"]], [mv(M["cover"], (0, 0, 70))], "cover",
       "Light pipe pressed in first. Lower it over the pillars; leads and connectors in the notches; four M3 x 6 screws",
       elev=24, azim=-55, label_done=False)
    st(10, bd + [M["fuse"], M["link"], M["probes"], M["cover"]],
       [mv(M["harness"], (-50, 0, 0)), mv(M["can"], (-50, 0, 0))], "balance harness and CAN plug",
       "Seen from the signal end. Only at the safety stops: balance harness first to the cell simulator, then the CAN plug",
       elev=24, azim=-140, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 8.4), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 84); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    RED, BLK, BLU, PRB, CAN = "#B91C1C", "#111827", "#1D4ED8", "#0369A1", "#0F766E"
    ax.text(2, 82, "CellGuard prototype: how it connects to the pack, the load and the host", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 78.8, "Block level. Power cables are 10 mm² stranded copper with ring lugs; each balance lead carries a fuse or resistor at the cell end.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/cellguard", fontsize=7, color=CAN, ha="right", family="monospace")

    def blk(x, y, w, h, title, sub, color, fc="white"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc=fc, ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.2, title, ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
        if sub:
            ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=7.2, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.2, ls="-"):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round", zorder=1)

    def lab(x, y, t, color, ha="left", va="center"):
        ax.text(x, y, t, fontsize=7.4, color=color, ha=ha, va=va, zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    # pack, shown as 4S
    blk(3, 16, 22, 52, "Pack (shown 4S)", "4 to 16 LFP cells; first\npower-up on a cell simulator", "#C2410C", "#FFF7ED")
    taps = []
    for k in range(4):
        y0 = 22 + 9.5 * k
        ax.add_patch(plt.Rectangle((7, y0), 12, 7, fc="#FED7AA", ec="#C2410C", lw=0.8))
        ax.text(13, y0 + 3.5, f"cell {k + 1}", ha="center", va="center", fontsize=6.8, color="#9A3412")
        taps.append(y0 - 1.25)
    taps.append(22 + 9.5 * 3 + 8.25)
    for y in taps:
        ax.plot([7, 20], [y, y], color="#9A3412", lw=0.6)
    # board
    blk(48, 14, 46, 54, "", "", "#15803D", "#F0FDF4")
    ax.text(50, 66.6, "CellGuard board", fontsize=9, fontweight="bold", color=INK, va="top")
    studs = {"B+": 63, "P+": 46, "P-": 38, "B-": 28}
    for n, y in studs.items():
        ax.add_patch(plt.Circle((88, y), 1.3, fc="#CA8A04", ec=INK, lw=0.6, zorder=4))
        ax.text(86, y, f"{n} stud", ha="right", va="center", fontsize=7.6, color=INK)
    ax.text(50, 61.5, "Balance header\n(17 way)", fontsize=7.6, color=INK, va="top")
    ax.text(50, 25.5, "Probe header", fontsize=7.6, color=INK, va="center")
    ax.text(78, 58, "CAN and UART (6 way)", fontsize=7.6, color=INK, va="center", ha="right")
    # fuse and power
    blk(28, 70, 12, 7, "Fuse", "60 A DC", "#C2410C")
    wire([(14, 68.3), (14, 73.5), (28, 73.5)], RED); lab(16, 75.6, "B+ cable", RED)
    wire([(40.3, 73.5), (88, 73.5), (88, 64.3)], RED); lab(64, 75.6, "copper fuse link to the B+ stud", RED, "center")
    wire([(14, 15.7), (14, 11), (88, 11), (88, 26.7)], BLK); lab(50, 9.2, "B- cable", BLK, "center")
    blk(98, 32, 20, 18, "Load or charger", "first power-up: an\nelectronic load or a\ncurrent-limited supply", "#6B7280")
    wire([(89.3, 46), (98, 46)], RED); lab(93.6, 47.8, "P+", RED, "center")
    wire([(89.3, 38), (98, 38)], BLK); lab(93.6, 36.2, "P-", BLK, "center")
    blk(98, 54, 20, 12, "Host", "CAN 2.0B 250 kbit/s,\nUART 3.3 V, enable", CAN)
    wire([(78.5, 58), (98, 58)], CAN, 1.4); lab(90, 59.6, "6 way", CAN, "center")
    # balance leads, B- tap at the bottom, no crossings
    order = sorted(taps, reverse=True)
    for k, y in enumerate(order):
        xk, yh = 30 + 1.2 * k, 58 - 1.0 * k
        wire([(20, y), (xk, y), (xk, yh), (48, yh)], BLU, 1.0)
    lab(36, 47, "balance leads:\nB- first, then up", BLU)
    # temperature probes, taped to two cells
    wire([(19, 24.5), (22, 24.5), (22, 19), (46, 19), (46, 25.5), (48, 25.5)], PRB, 1.0, "--")
    lab(30, 17.4, "2 temperature probes", PRB, "center")
    ax.text(30, 6.2, "Connect in this order: B- and B+ cables with the fuse OUT; the balance harness from B- upward, checking each lead with a meter;",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(30, 3.8, "then the probes and the host; fit the fuse last. Disconnect in the reverse order.", fontsize=7.6, color="#B45309", fontweight="bold")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "wiring.png", facecolor="white"); plt.close(fig)
    return OUT / "wiring.png"


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "joint7", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring,
           "joint7": joint7, "sheets103-104": lambda: sheets(("103", "104"))}
    for w in what:
        print(w, "->", fns[w]())
