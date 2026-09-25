# CellGuard

**Area:** Shared Components · **Status:** Concept · **Prototype budget:** about $120 USD · **Difficulty:** 4 of 5

An open battery management board for small LiFePO4 packs (4 to 16 cells) with cell balancing, protection and a documented state-of-charge estimate, reusable across the lab's vehicles, storage and field kits.

## Concept rationale

A single, openly documented BMS removes the riskiest unknown from every battery project in the lab and gives SwapCell, PowerBox and FieldNode a common safety layer.

## Burning platform

Battery fires in e-bikes and home storage are rising as cheap packs with poor protection spread, and repairers cannot inspect or fix closed battery management systems.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. SwapCell, PowerBox, SunSpoke and the smart city nodes all rely on lithium packs whose protection was left unspecified.

## Problem

Small builders either buy closed battery management boards with unknown firmware and limits, or skip protection altogether. Both lead to damaged packs and fires, and neither teaches anything.

## Concept

An open battery management board for small LiFePO4 packs (4 to 16 cells) with cell balancing, protection and a documented state-of-charge estimate, reusable across the lab's vehicles, storage and field kits.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Cell voltage monitor IC with passive balancing
- Charge and discharge MOSFET switches
- Current shunt and amplifier
- Temperature sensors, 3 points
- Microcontroller with CAN and UART
- Fuse and precharge circuit
- Enclosure and harness

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Lithium cells can overheat, vent and burn. Use protected cells or LiFePO4, fuse every pack, charge only within the cell maker's limits and never leave a first build charging unattended.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Shared components set.
