"""CellGuard general arrangement drawing CGD-DWG-001 (Rev P3: status light and light pipe, 1.5 mOhm-class switches, CGD-DEC-001).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/CGD-DWG-001.svg, .pdf and .png from the parametric model.
The concept sheet in media/ uses CGD-DWG-010, so DWG-001 is the first free number.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts, envelope  # noqa: E402

parts = build_parts()
asm = assemblies(parts)["cellguard-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
e = envelope()

s = Sheet(project="CellGuard", title="General arrangement, BMS board", dwg_no="CGD-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Plate 6061 Al 4 mm; PCB FR-4 4-layer 2 oz; cover PC UL 94 V-0, opaque. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA (CGD-CAL-001, CGD-DDR-001)", "2026-09-25", "AC"),
                     ("P2", "Made buildable: fixings, fuse link, cover notches (CGD-DDR-003)", "2026-09-30", "AC"),
                     ("P3", "Status light, light pipe, 1.5 mOhm switches (CGD-DEC-001)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 37, 140, 78, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Board envelope {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.0f} (harness tail and probes extra)",
    f"Base plate {P['plate_l']:.0f} x {P['plate_w']:.0f} x {P['plate_t']:.0f}, flat; board on 6 spacers 3 mm",
    "PCB fixings: M3 countersunk from below; 4 pillars 20 mm carry the cover",
    f"PCB {P['pcb_l']:.0f} x {P['pcb_w']:.0f} x {P['pcb_t']}; top face at z {P['pcb_z0'] + P['pcb_t']:.1f}",
    f"Power studs M6 at x {P['stud_x']:.0f}: B-, P-, P+, B+ at y -33, -11, 11, 33",
    "Pack fuse on plate in line with B+: 60 A, 80 V DC, 10 kA or more",
    "Copper link 14 x 3 joins the B+ stud to the fuse holder",
    "Plate mounting: 4 x M4 tapped, screws from below",
    "Balance: 17-way connector at -X; CAN and UART 6-way at -X",
    "MOSFETs 2 x 4, 1.5 mOhm class, under PCB on gap pad 1.0 to 0.7",
    f"Status light at x {P['led_xy'][0]:.0f}, y {P['led_xy'][1]:.0f}; 3 mm light pipe in the opaque cover",
    "Secondary protector and SCP fuse in the B+ path (part 14)",
    "CAN 2.0B 250 kbit/s, SwapCell v0.3 message set profile",
    "40 A continuous, 80 A for 10 s; 4 to 16 LFP cells, under 60 V",
    "Mass about 0.66 kg (CGD-CAL-001 v0.6)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/CGD-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/CGD-DWG-001.svg, .pdf, .png")
