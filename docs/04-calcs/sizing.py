"""CellGuard sizing calculations for CGD-CAL-001 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number that CGD-CAL-001 quotes and writes docs/04-calcs/results.csv.
Reads part volumes and the envelope from cad/src/model.py and costs from bom/bom.csv.
All values are first-principles estimates from stated assumptions; nothing is measured.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))

# ---------------------------------------------------------------- assumptions
LFP_MAX, LFP_NOM, LFP_MIN = 3.65, 3.20, 2.50     # V per cell, default thresholds
NMC_MAX = 4.20                                   # V per cell, SwapCell-type NMC
S_MIN, S_MAX = 4, 16
V_LIMIT = 60.0                                   # extra-low-voltage ceiling, V DC
FET_VDS = 100.0                                  # MOSFET rating, V

I_CONT, I_PEAK, T_PEAK = 40.0, 80.0, 10.0        # A, A, s (R5)
T_AMB = 40.0                                     # degC (R5)
RDS25 = 2.5e-3                                   # ohm per FET at 25 degC, maximum (BOM line 4)
RDS_TC = 0.0067                                  # per K; about 1.5 x at 100 degC
N_PAR = 4                                        # FETs in parallel per direction
SHARE = 1.10                                     # hottest FET carries 10 % more than its share
R_SHUNT = 0.25e-3
R_SCP = 0.40e-3                                  # self-control protector fuse, assumed (no data sheet yet)
R_FUSE = 1.0e-3                                  # main fuse, holder and links (external to R6)
CU_SHEET = 1.72e-8 / 70e-6                       # ohm per square, 2 oz copper at 20 degC
CU_TC = 0.0039
LAYERS = 4
POS_PATH = (60.0, 25.0)                          # mm length, mm width: B+ stud, SCP, FETs, P+ stud
NEG_PATH = (90.0, 25.0)                          # B- stud, shunt, P- stud
R_JOINT = 0.05e-3                                # per stud joint, 4 studs
T_PCB = 50.0                                     # degC copper temperature at 40 A (checked below)

H_PLATE = 8.0                                    # W/(m2 K) effective, both faces, natural convection plus radiation
PCB_TO_PLATE = 0.5                               # share of PCB copper and shunt loss reaching the plate
RJC_TOLT, RJC_TOLL = 0.5, 20.0                   # K/W junction to top: top-cooled package vs through the mold
PAD_T, PAD_K, PAD_A = 0.5e-3, 3.0, 1.0e-4        # m, W/(m K), m2 per FET

AL_RHO, AL_CP = 2700.0, 896.0

BAL_R = 33.0                                     # ohm bleed resistor
BAL_V = 3.40                                     # V cell voltage while balancing
BAL_N = 8                                        # channels at once (non-adjacent)
H_PCB = 6.0                                      # W/(m2 K), PCB under the cover
RTH_RES = 50.0                                   # K/W, 2512 resistor to local board

CAN_BITRATE = 250_000                            # SwapCell interface v0.3
CAN_FRAME_BITS = 135                             # 8 data bytes, 11-bit ID, worst-case stuffing
CAN_RATES = {"PACK_STATUS": 10, "PACK_LIMITS": 10, "CELL_SUMMARY": 1, "TEMPERATURES": 1,
             "FAULTS": 1, "STATE_OF_HEALTH": 0.1, "HOST_HEARTBEAT": 10, "CHARGER_STATUS": 1}

REC_BYTES, FLASH_BYTES, REC_NEED = 32, 2 * 1024 * 1024, 2000

C_LOAD, R_PRE = 2e-3, 100.0                      # F, ohm (R13)

CC_LSB = 1 / 131590                              # V per LSB (mean of the data sheet gain range)
CC_OFF_CAL = 1e-6                                # V, offset after calibration (TI typical, < 1 uV)
GAIN_CAL = 0.005                                 # 0.5 % residual gain error after calibration
SOC_ANCHOR, SOC_CAP = 2.0, 2.0                   # points: anchor detection, capacity estimate
CYCLES_7D = 3.5                                  # equivalent full cycles in 7 days of partial cycling

# ---------------------------------------------------------------- helpers
rows = []


def out(key, value, unit="", fmt="{:.2f}"):
    s = fmt.format(value) if isinstance(value, (int, float)) else str(value)
    print(f"{key:58s} {s:>12s} {unit}")
    rows.append((key, s, unit))


def section(t):
    print(f"\n== {t}")


# ---------------------------------------------------------------- 1 voltage range (R1)
section("1 Voltage range (R1)")
out("LFP pack voltage, 4S nominal", S_MIN * LFP_NOM, "V")
out("LFP pack voltage, 16S nominal", S_MAX * LFP_NOM, "V")
out("LFP pack voltage, 16S maximum", S_MAX * LFP_MAX, "V")
out("MOSFET voltage margin at 16S maximum", FET_VDS / (S_MAX * LFP_MAX), "x")
out("NMC maximum series count under 60 V", math.floor(V_LIMIT / NMC_MAX), "cells", "{:.0f}")
out("NMC 13S maximum (SwapCell)", 13 * NMC_MAX, "V")

# ---------------------------------------------------------------- 2 losses and thermal (R5, R6)
section("2 Power path loss and thermal (R5, R6)")
r_pos = CU_SHEET * POS_PATH[0] / POS_PATH[1] / LAYERS
r_neg = CU_SHEET * NEG_PATH[0] / NEG_PATH[1] / LAYERS
r_cu20 = r_pos + r_neg + 4 * R_JOINT
r_cu = r_cu20 * (1 + CU_TC * (T_PCB - 20))
out("PCB copper and stud joints at 20 degC", r_cu20 * 1e3, "mOhm", "{:.3f}")
out("PCB copper and stud joints at 50 degC", r_cu * 1e3, "mOhm", "{:.3f}")

from model import PARAMS, build_parts, envelope  # noqa: E402
area_plate = 2 * PARAMS["plate_l"] * PARAMS["plate_w"] * 1e-6
ua_plate = H_PLATE * area_plate
r_pad = PAD_T / (PAD_K * PAD_A)


def thermal(i, rjc):
    """Iterate FET resistance with junction temperature; return a dict of results."""
    tj = T_AMB + 10
    for _ in range(50):
        r_fet = RDS25 * (1 + RDS_TC * (tj - 25))
        r_dir = r_fet / N_PAR
        p_fet = i ** 2 * 2 * r_dir
        p_shunt = i ** 2 * R_SHUNT
        p_cu = i ** 2 * r_cu
        p_scp = i ** 2 * R_SCP
        p_fuse = i ** 2 * R_FUSE
        p_plate = p_fet + p_fuse + PCB_TO_PLATE * (p_cu + p_shunt + p_scp)
        dt_plate = p_plate / ua_plate
        p_each = (i / N_PAR * SHARE) ** 2 * r_fet
        tj_new = T_AMB + dt_plate + p_each * (rjc + r_pad)
        if abs(tj_new - tj) < 1e-4:
            break
        tj = tj_new
    return dict(r_fet=r_fet, p_fet=p_fet, p_shunt=p_shunt, p_cu=p_cu, p_scp=p_scp, p_fuse=p_fuse,
                p_board=p_fet + p_shunt + p_cu + p_scp, p_board_noscp=p_fet + p_shunt + p_cu,
                dt_plate=dt_plate, p_each=p_each, tj=tj)


a = thermal(I_CONT, RJC_TOLT)
b = thermal(I_CONT, RJC_TOLL)
p_fet25 = I_CONT ** 2 * 2 * RDS25 / N_PAR
out("MOSFET loss at 40 A, 25 degC junction", p_fet25, "W")
out("MOSFET loss at 40 A, converged junction (TOLT)", a["p_fet"], "W")
out("Shunt loss at 40 A", a["p_shunt"], "W")
out("PCB copper and stud loss at 40 A", a["p_cu"], "W")
out("SCP fuse loss at 40 A (assumed 0.40 mOhm)", a["p_scp"], "W")
out("Board loss at 40 A with SCP (R6)", a["p_board"], "W")
out("Board loss at 40 A without SCP", a["p_board_noscp"], "W")
out("Board loss at 40 A, 25 degC FETs, with SCP", p_fet25 + a["p_shunt"] + a["p_cu"] + a["p_scp"], "W")
out("Fuse, holder and links loss at 40 A (external)", a["p_fuse"], "W")
p_total = a["p_board"] + a["p_fuse"]
out("Total power path loss at 40 A", p_total, "W")
out("Power path efficiency, 16S at 40 A", 100 * (1 - p_total / (S_MAX * LFP_NOM * I_CONT)), "%", "{:.2f}")
out("Plate area, both faces", area_plate, "m2", "{:.4f}")
out("Plate temperature rise at 40 A", a["dt_plate"], "K", "{:.1f}")
out("Hottest FET loss at 40 A", a["p_each"], "W", "{:.3f}")
out("Saving with 1.5 mOhm MOSFETs at 40 A", a["p_fet"] * (1 - 1.5e-3 / RDS25), "W", "{:.2f}")
out("FET junction at 40 A, 40 degC, top-cooled TOLT", a["tj"], "degC", "{:.1f}")
out("FET junction at 40 A, 40 degC, TOLL through the mold", b["tj"], "degC", "{:.1f}")
m_plate_al = PARAMS["plate_l"] * PARAMS["plate_w"] * PARAMS["plate_t"] * 1e-9 * AL_RHO
c_plate = m_plate_al * AL_CP
out("Plate heat capacity", c_plate, "J/K", "{:.0f}")
out("Plate time constant", c_plate / ua_plate / 60, "min", "{:.1f}")
pk = thermal(I_PEAK, RJC_TOLL)
extra = (pk["p_fet"] + pk["p_fuse"] + PCB_TO_PLATE * (pk["p_cu"] + pk["p_shunt"] + pk["p_scp"])) - \
        (a["p_fet"] + a["p_fuse"] + PCB_TO_PLATE * (a["p_cu"] + a["p_shunt"] + a["p_scp"]))
dt_peak_plate = extra * T_PEAK / c_plate
p_each_pk = (I_PEAK / N_PAR * SHARE) ** 2 * a["r_fet"] * (1 + RDS_TC * 20)
tj_peak_tolt = a["tj"] + dt_peak_plate + p_each_pk * (RJC_TOLT + r_pad)
tj_peak_toll = b["tj"] + dt_peak_plate + p_each_pk * (RJC_TOLL + r_pad)
out("Extra plate rise, 80 A for 10 s", dt_peak_plate, "K", "{:.2f}")
out("Hottest FET loss at 80 A", p_each_pk, "W", "{:.2f}")
out("FET junction after 80 A for 10 s, TOLT (steady bound)", tj_peak_tolt, "degC", "{:.1f}")
out("FET junction after 80 A for 10 s, TOLL (steady bound)", tj_peak_toll, "degC", "{:.1f}")

# ---------------------------------------------------------------- 3 protection (R3)
section("3 Protection thresholds on a 0.25 mOhm shunt (R3)")
scd_mv, scd_us = 100, 15
ocd1_mv, ocd1_ms = 24, 320
ocd2_mv, ocd2_ms = 40, 20
occ_mv = 12
out("SCD threshold (100 mV)", scd_mv * 1e-3 / R_SHUNT, "A", "{:.0f}")
out("SCD delay set (15 to 450 us available)", scd_us, "us", "{:.0f}")
out("OCD1 threshold (24 mV), 320 ms", ocd1_mv * 1e-3 / R_SHUNT, "A", "{:.0f}")
out("OCD2 threshold (40 mV), 20 ms", ocd2_mv * 1e-3 / R_SHUNT, "A", "{:.0f}")
out("OCC threshold (12 mV)", occ_mv * 1e-3 / R_SHUNT, "A", "{:.0f}")
out("Smallest SCD step (10 mV)", 10e-3 / R_SHUNT, "A", "{:.0f}")
out("SCD trip complete (delay plus turn-off)", scd_us + 10, "us", "{:.0f}")

section("4 Prospective short circuit and turn-off (R3, fuse)")
L_LOOP, T_OFF = 1.0e-6, 10e-6                    # H loop inductance (assumed), s FET turn-off (assumed)
R_BOARD = 2 * RDS25 / N_PAR + R_SHUNT + r_cu20 + R_SCP + R_FUSE
R_CABLE = 2 * 1.72e-8 * 0.5 / 10e-6              # two 0.5 m, 10 mm2 cables
packs = {"16S 20 Ah": (16, 3.0e-3, 0.3e-3), "16S 280 Ah": (16, 0.25e-3, 0.1e-3),
         "4S 280 Ah": (4, 0.25e-3, 0.1e-3), "4S 20 Ah": (4, 3.0e-3, 0.3e-3)}
out("Board and fuse resistance in the short-circuit loop", R_BOARD * 1e3, "mOhm", "{:.2f}")
out("Power cable resistance, 2 x 0.5 m of 10 mm2", R_CABLE * 1e3, "mOhm", "{:.2f}")
for name, (s, rc, rb) in packs.items():
    v = s * LFP_NOM
    r = s * (rc + rb) + R_CABLE + R_BOARD
    isc = v / r
    tau = L_LOOP / r
    for d in (15e-6, 60e-6):
        i_off = isc * (1 - math.exp(-(d + T_OFF) / tau))
        out(f"{name}: current at FET turn-off, SCD delay {d * 1e6:.0f} us", i_off, "A", "{:.0f}")
        out(f"{name}: inductive energy at turn-off, delay {d * 1e6:.0f} us", 0.5 * L_LOOP * i_off ** 2, "J", "{:.2f}")
        if d == 15e-6:
            out(f"{name}: current per discharge MOSFET at turn-off, 15 us", i_off / N_PAR, "A", "{:.0f}")
    out(f"{name}: prospective short-circuit current", isc, "A", "{:.0f}")

# ---------------------------------------------------------------- 5 balancing (R7)
section("5 Balancing (R7)")
i_bal = BAL_V / BAL_R
p_bal = BAL_V ** 2 / BAL_R
out("Balance current per cell", i_bal * 1e3, "mA", "{:.0f}")
out("Balance power per channel", p_bal, "W", "{:.3f}")
out("Balance power, 8 channels at once", BAL_N * p_bal, "W", "{:.2f}")
for cap in (20, 100, 280):
    out(f"Time to correct 1 % on {cap} Ah", 0.01 * cap / i_bal, "h", "{:.1f}")
a_pcb = 2 * PARAMS["pcb_l"] * PARAMS["pcb_w"] * 1e-6
dt_pcb = BAL_N * p_bal / (H_PCB * a_pcb)
out("PCB bulk rise while balancing (no plate conduction)", dt_pcb, "K", "{:.1f}")
out("PCB bulk temperature at 40 degC ambient", T_AMB + dt_pcb, "degC", "{:.1f}")
out("Balance resistor hotspot at 40 degC ambient", T_AMB + dt_pcb + p_bal * RTH_RES, "degC", "{:.1f}")

# ---------------------------------------------------------------- 6 current and SoC (R8, R9)
section("6 Current measurement and state of charge (R8, R9)")
off_uncal = CC_LSB / R_SHUNT
off_cal = CC_OFF_CAL / R_SHUNT
gain_spread = (132335 - 130845) / 2 / 131590
out("Coulomb counter 1 LSB referred to the shunt", CC_LSB * 1e6, "uV", "{:.2f}")
out("Offset current, uncalibrated (1 LSB)", off_uncal * 1e3, "mA", "{:.1f}")
out("Offset current, calibrated (1 uV)", off_cal * 1e3, "mA", "{:.1f}")
out("Front-end gain spread (half range)", gain_spread * 100, "%", "{:.2f}")
out("Gain error uncalibrated (shunt 1 % + front end)", 100 * (0.01 + gain_spread), "%", "{:.2f}")
out("Gain error after one-point calibration", GAIN_CAL * 100, "%", "{:.2f}")
out("Current error at 80 A after calibration", 80 * GAIN_CAL + off_cal, "A", "{:.3f}")
out("R9 limit at 80 A", 80 * 0.01 + 0.05, "A", "{:.3f}")
soc_full = SOC_ANCHOR + SOC_CAP + 1.0            # anchor, capacity estimate, 1 % gain over one full cycle
out("SoC error after a full charge (anchor + capacity + 1 cycle gain)", soc_full, "points", "{:.1f}")
for cap in (20, 100, 280):
    drift_typ = off_cal * 168 / cap * 100
    drift_wc = off_uncal * 168 / cap * 100
    gain = GAIN_CAL * CYCLES_7D * 100
    out(f"SoC error after 7 days, {cap} Ah, calibrated offset", soc_full + gain + drift_typ, "points", "{:.1f}")
    out(f"SoC error after 7 days, {cap} Ah, uncalibrated offset", soc_full + gain + drift_wc, "points", "{:.1f}")
out("Offset allowed for 10 points on 20 Ah", (10 - soc_full - GAIN_CAL * CYCLES_7D * 100) / 100 * 20 / 168 * 1e3,
    "mA", "{:.1f}")

# ---------------------------------------------------------------- 7 sleep (R10)
section("7 Quiescent current (R10)")
V_PACK = S_MAX * LFP_NOM
rail_ua = 5 + 10 + 1                             # MCU stop, CAN standby with wake, flash deep power-down (uA at 3.3 V)
buck_eff, buck_iq = 0.70, 10.0
sleep = {"Front end SLEEP, DSG on (TI typical)": 41.0,
         "3.3 V rail loads through the buck": rail_ua * 3.3 / (V_PACK * buck_eff),
         "Buck regulator quiescent (assumed)": buck_iq,
         "Secondary protector (TI typical)": 1.0,
         "TVS leakage (assumed)": 1.0}
for k, v in sleep.items():
    out(f"Sleep: {k}", v, "uA", "{:.1f}")
i_sleep = sum(sleep.values())
out("Sleep current total", i_sleep, "uA", "{:.1f}")
out("Sleep current with SwapCell INTERLOCK loop (+30 uA)", i_sleep + 30, "uA", "{:.1f}")
ship = {"Front end SHUTDOWN": 1.0, "Buck disabled (assumed)": 3.0, "Secondary protector": 1.0, "TVS leakage": 1.0}
out("Ship-mode current total", sum(ship.values()), "uA", "{:.1f}")
out("Self-discharge from sleep, 20 Ah pack", i_sleep * 1e-6 * 730 / 20 * 100, "% per month", "{:.2f}")

# ---------------------------------------------------------------- 8 interface and log (R11, R12)
section("8 CAN bus load and log (R11, R12)")
fps = sum(CAN_RATES.values())
out("CAN frames per second (pack and host)", fps, "1/s", "{:.1f}")
out("CAN bus load at 250 kbit/s", 100 * fps * CAN_FRAME_BITS / CAN_BITRATE, "%", "{:.2f}")
out("Log capacity in 2 MiB flash", FLASH_BYTES // REC_BYTES, "records", "{:.0f}")
out("Flash needed for 2,000 records", REC_NEED * REC_BYTES, "bytes", "{:.0f}")

# ---------------------------------------------------------------- 9 precharge (R13)
section("9 Precharge (R13)")
v_max = S_MAX * LFP_MAX
tau = R_PRE * C_LOAD
out("Precharge time constant", tau, "s", "{:.2f}")
out("Time to 90 %", tau * math.log(10), "s", "{:.2f}")
out("Energy in resistor to 90 %", C_LOAD * v_max ** 2 * (0.9 - 0.81 / 2), "J", "{:.2f}")
out("Peak current", v_max / R_PRE, "A", "{:.3f}")
out("Peak resistor and switch power", v_max ** 2 / R_PRE, "W", "{:.1f}")
out("Energy into a shorted load in the 1 s timeout", v_max ** 2 / R_PRE * 1.0, "J", "{:.1f}")

# ---------------------------------------------------------------- 10 size and mass (R14)
section("10 Size and mass (R14)")
e = envelope()
out("Envelope length", e[1] - e[0], "mm", "{:.0f}")
out("Envelope width", e[3] - e[2], "mm", "{:.0f}")
out("Envelope height", e[5] - e[4], "mm", "{:.0f}")
vol = {bom: s.volume / 1e3 for _, s, _, bom, _ in build_parts()}   # cm3
dens = {1: 2.70, 13: 1.20, 8: 2.50, 9: 8.50, 4: 2.50, 7: 2.70, 12: 1.50}    # g/cm3 (8: average fuse and holder)
mass = {"1 Base plate": vol[1] * dens[1],
        "2 PCB with copper (60 % fill)": vol[2] * 1.85 + 4 * PARAMS["pcb_l"] * PARAMS["pcb_w"] * 0.07e-3 * 8.96 * 0.6,
        "4 MOSFETs": vol[4] * dens[4], "7 Precharge": vol[7] * dens[7],
        "8 Fuse and holder": vol[8] * dens[8], "9 Studs": vol[9] * dens[9],
        "9 Nuts, washers, lugs (assumed)": 32.0, "10 Balance connector and harness (assumed)": 45.0,
        "11 Temperature sensors (assumed)": 10.0, "12 CAN and UART connector": vol[12] * dens[12],
        "13 Cover": vol[13] * dens[13], "3, 5, 6, 14, 15 Other components (assumed)": 15.0,
        "17 Thermal pad and screws (assumed)": 13.0}
for k, v in mass.items():
    out(f"Mass: {k}", v, "g", "{:.0f}")
m_tot = sum(mass.values())
out("Mass total without power cables", m_tot / 1000, "kg", "{:.3f}")
m_3mm = m_tot - PARAMS["plate_l"] * PARAMS["plate_w"] * 1.0 * 1e-3 * dens[1]   # 1 mm less plate
out("Mass total with a 3 mm plate", m_3mm / 1000, "kg", "{:.3f}")

# ---------------------------------------------------------------- 11 cost (R16)
section("11 Cost (R16)")
with open(ROOT / "bom/bom.csv") as f:
    bom = list(csv.DictReader(f))
tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
sec = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r["item"].startswith("14 "))
out("BOM lines", len(bom), "", "{:.0f}")
out("BOM total", tot, "USD")
out("BOM total without the secondary protector", tot - sec, "USD")
out("Against budget_usd 120", 100 * (tot / 120 - 1), "% over", "{:.1f}")
out("Margin against recommended 140", 140 - tot, "USD")

with open(ROOT / "docs/04-calcs/results.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["quantity", "value", "unit"])
    w.writerows(rows)
print(f"\nwrote docs/04-calcs/results.csv ({len(rows)} rows)")
