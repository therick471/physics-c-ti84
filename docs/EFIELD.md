# APC E&M / E-Field Studio

Use this edition for field derivations, formulas, and E&M reference tools.

## Install and open

**Evo:** send all 34 `.py` files in `TI84_EVO/EFIELD/TRANSFER`. Restart calculator Python. Run EFIELD for the models or APC for the E&M menu.

**CE Python:** use `TI84_PLUS_CE_PYTHON/TOPICS/FIELD_STUDIO/TRANSFER` for calculations, inverses, extrema and plots; FIELD_GUIDES for the complete derivations; FINAL_FORMULAS for all final equations. The CE download includes every topic, but only one can be installed at a time. [CE instructions](CE_PYTHON.md).

The older sharing ZIP retains an archived CE profile. Use the current **APC_CE_Python.zip** or the complete pack for a new CE installation.

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
