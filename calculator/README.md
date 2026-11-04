# AP Physics C - corrected TI-84 Evo release

Use this release instead of the original packed edition. TI's Python Run action imports programs; both launchers now start automatically when imported. The compressed loader has been removed. This v3 revision also removes the unsupported isalnum call and the related character-predicate methods. APCHECK prints APCHECK START v3 so you can confirm the new files loaded.

## Replace the original toolkit

1. Unzip **AP_Physics_C_Evo_Fixed.zip** on your computer.
2. In [TI Connect Evo](https://connectevo.ti.com/), transfer all **22 Python files in TRANSFER_FIRST**. Allow them to replace the old files with the same names. Keep names and capitalization.
3. Remove the old toolkit's **APLOAD**, **APNOTES**, and **APTOOLS** Python files if present. APTOOLS has a new optional replacement. Other programs do not need to be deleted to fix the silent startup bug.
4. Restart or reinitialize the Python shell to clear earlier imports, then run **APCHECK**. You should see **APCHECK START**, then **SELF CHECK PASS**, then **8 numeric checks passed.** Press Enter to finish. A failure or memory error prints an explicit message.
5. Restart the Python shell again and run **APC**. The menu should appear immediately. Try Mechanics -> Forces/dynamics -> Newton second law -> Solve -> F. Enter m=2 and a=3: expect **F N = 6**.

The main install is **48,189 bytes of plain source**. Source size is not a measurement of runtime memory. Actual Evo heap usage and screen behavior still require your calculator to verify.

## What remains included

All **13 AP Physics C units**, **160 equations**, and **566 unknown targets** remain: 525 direct targets and 41 numerical targets requiring a bracket. Each equation shows its variable definitions, SI units, and assumptions. The menus show five choices per page: **1-5 select, 0 back, 8 previous, 9 next**, followed by Enter. At numeric prompts **q** cancels, Enter reuses a displayed value, and **ans** uses the last answer. Inputs accept scientific notation and expressions such as `pi/4`, `sqrt(2)`, and `ke*qe`. Angles are always radians; default g is 9.8 m/s^2.

Math tools include derivatives, definite integrals, bracketed roots, stable quadratic solutions, linear systems, a first-order numerical ODE solver, and percent comparisons. Graphs include formula-variable sweeps, custom f(x), projectile paths, motion, SHM, RC voltage, and RL current. They use TI's ti_plotlib. Preset plots sample **40 points** to save memory. Poles and narrow peaks can be missed; use narrow windows. Use equation graphs or custom f(x) for other fields, potentials, velocities, and accelerations.

## Optional multi-step tools

The **OPTIONAL_TOOLS** folder contains the original 15 multi-step solvers in smaller groups. Transfer **APTOOLS.py** plus the group you want, if sufficient Python program space remains:

- **APMECH.py**: vectors, projectiles, collisions, COM/momentum, Atwood machines, SHM initial states, and rolling inclines.
- **APEM.py**: charge superposition, spheres, equivalent components, multi-battery resistor circuits, RC/RL transients, and motional emf/drag.
- **APLAB.py**: linear regression.

All four add-ons total **12,103 source bytes**. Uninstalled groups show an explanatory message when selected. The ordinary equation solvers remain available without these add-ons. If all add-ons exceed available space, keep only the group needed or keep the main install alone.

## Memory and scope changes

The main menu loads only a selected unit or tool module. Equation catalogs remain as text until a selected row is needed. Finished unit/tool imports are removed from the import cache when supported and garbage collection runs. No compressed source is expanded or executed. Full concept notes are in **CONCEPTS.md** on your computer; model assumptions remain on the calculator. The last answer replaces the old eight-answer history.

If MemoryError repeats, restart the Python shell and record the program, selected menu, and traceback line. Do not repeatedly delete unrelated work to troubleshoot it. The program has been checked on desktop Python, including TI-style import startup; it has not been run on a physical Evo.

See **FORMULAS.md**, **COVERAGE.md**, and **VALIDATION_LITE.md** for details. These tools evaluate models you select; they do not interpret every word problem or supply symbolic derivations. Numerical brackets must be continuous and sign-changing. Calculus and graph results are numerical estimates.
