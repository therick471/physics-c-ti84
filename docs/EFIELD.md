# APC E&M / E-Field Studio

Use this edition for field derivations, formulas, and E&M reference tools.

## Install and open

From the complete download, send all **34 `.py` files** in `TI84_EVO/EFIELD/TRANSFER` for Evo, or `TI84_PLUS_CE_PYTHON/TRANSFER` for CE Python. Restart calculator Python. Run **EFIELD** for the field models or **APC** for the E&M menu.

The smaller sharing ZIP has the same profiles under `TI84_EVO/TRANSFER` and `TI84_PLUS_CE_PYTHON/TRANSFER`. [Installation steps](INSTALL.md).

## Models and menus

| Model | Meaning of the dimensions |
|---|---|
| Ring axis | R is ring radius; x is measured from its center along the axis |
| Finite rod, perpendicular bisector | L is the full rod length; x is the perpendicular distance from its midpoint |
| Finite rod, beyond an end | x is measured from the near end of the rod |
| Infinite line | Distance is measured perpendicular to the line |
| Arc center | Follow the angle prompt; arc inputs explicitly request degrees |

Choose a model, then Calculate, Full derivation + limits, Maxima/minima, Graph, Solve backward, Geometry sketch, or Final formulas. APC also contains the six E&M reference units.

For **Quiz 8.4**, use the finite-rod bisector and ring-axis derivations. The finite rod uses trig substitution; the ring uses angular integration and symmetry.

## Controls and inputs

**↑/↓** selects; **ENTER** opens; **←/→** changes pages; **CLEAR/0** returns. In guide cards, ENTER/RIGHT advances and LEFT goes back.

If keys do not respond, run **EFKEY** and press/release each requested key. Calibration lasts for the current Python session.

Use SI units. Expression trig functions use radians; follow prompts that explicitly request degrees. `q` then ENTER cancels a number prompt. Final formulas require no numerical input. [Troubleshooting](TROUBLESHOOTING.md).
