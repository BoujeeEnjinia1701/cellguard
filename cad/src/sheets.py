"""CellGuard general arrangement drawing CGD-DWG-001 (Rev P1).

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
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True,
          material="Plate 6061 Al 4 mm; PCB FR-4 4-layer 2 oz; cover PC UL 94 V-0. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA (CGD-CAL-001, CGD-DDR-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Board envelope {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.0f} (harness tail and probes extra)",
    f"Base plate {P['plate_l']:.0f} x {P['plate_w']:.0f} x {P['plate_t']:.0f}; 4 standoffs at "
    f"+/-{P['standoff_x']:.0f}, +/-{P['standoff_y']:.0f}",
    f"PCB {P['pcb_l']:.0f} x {P['pcb_w']:.0f} x {P['pcb_t']}; top face at z {P['pcb_z0'] + P['pcb_t']:.1f}",
    f"Power studs M6 at x {P['stud_x']:.0f}: B-, P-, P+, B+ at y -33, -11, 11, 33",
    "Pack fuse on plate at +X: 60 A, 80 V DC, 10 kA or more",
    "Balance: 17-way connector at -X; CAN and UART 6-way at -X",
    "MOSFETs 2 x 4 under PCB on 0.5 mm insulating pad",
    "Secondary protector and SCP fuse in the B+ path (part 14)",
    "CAN 2.0B 250 kbit/s, SwapCell v0.3 message set profile",
    "40 A continuous, 80 A for 10 s; 4 to 16 LFP cells, under 60 V",
    "Mass about 0.65 kg (CGD-CAL-001)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=128, width=140)
s.save(ROOT / "cad/drawings/CGD-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/CGD-DWG-001.svg, .pdf, .png")
