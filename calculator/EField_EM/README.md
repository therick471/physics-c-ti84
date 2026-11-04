# E-Field Studio v2 - TI-84 Evo / E&M only

Run **EFIELD** for the new field solver. **APC** opens the E&M-only toolkit. Mechanics units APU01-APU07 are excluded; APU08-APU13 remain. This release uses 34 plain Python files, totaling 67,943 source bytes. Source storage and runtime heap are different; real-device execution must be checked.

## Final formulas

**APC > Final formulas** and **EFIELD > Final formulas** open the answer-only browser. Each of the five field-model menus also has a **Final formulas** shortcut. This section asks for no numerical inputs and contains no derivation steps. It shows final E and V expressions, variable definitions and domains, useful limit/extremum results, and superposition formulas for rings, point charges and arc sectors. **All other E&M equations** browses every equation in all six retained E&M units with its conditions.

For the already installed toolkit, **EField_Final_Formulas_Update.zip** contains the three required files: APC, EFAPP and EFFINAL. Send all three in one batch with replacement enabled, then restart Python. Existing graphic styling, keyboard bindings in EFGUI, and highlight alignment are retained; rerun EFKEY after restarting if you use calibrated keys.

## Evo keyboard repair (v3 patch)

The previous menu recognized CE Python codes but omitted Evo keypad codes. The repair adds Evo bindings and prefers its blocking `get_key(1)` API when available. CE and named-string events remain supported. Unknown key presses are ignored without redrawing the menu.

For an already installed E-Field Studio, send the TWO files from **EField_Studio_v3_Keyboard_Patch.zip** in one batch with replacement enabled. Restart Python. Run **EFKEY** to measure UP, DOWN, LEFT, RIGHT, ENTER and CLEAR directly on this calculator, then follow the DOWN/ENTER menu test. A successful test prints **PASS: hardware navigation** and opens EFIELD using the learned bindings. Calibration applies for that Python session; ordinary EFIELD starts with the built-in defaults. Run EFKEY again if you need to recalibrate after restarting Python.

The desktop suite now has 33 test groups, including both numeric key families, named events, unknown/no-key events, and calibration with arbitrary measured codes followed by an actual menu selection. Desktop tests do not verify a physical keyboard.

## First use

1. Restart/reinitialize the Python shell after transfer to clear cached modules.
2. Run **EFCHK**. It should print **EFIELD CHECK START v2**, then **PASS: 12 physics + 2 UI**. Restart Python again.
3. Run **EFIELD**. Pick a model, then Calculate, Full derivation + limits, Maxima/minima, Graph, Solve backward, or Geometry sketch.
4. **UP/DOWN** highlights a choice; **ENTER** opens it. **LEFT/RIGHT** changes menu pages. **CLEAR** or **0** returns. Number keys 1-5 select a displayed choice directly; 8/9 changes pages. Numeric inputs still require Enter. Expressions such as `1e-9`, `pi/4`, `sqrt(2)` work. Use SI units.

Menus and guide cards use TI_DRAW with immediate key handling. Titles and navigation hints appear on a plain white background; the colored top and bottom bars have been removed. The selected menu item keeps its light highlight, aligned with the Evo text baseline so it covers the item that ENTER opens, including wrapped labels. For an already installed keyboard repair, **EField_Plain_UI_Update.zip** contains just the one EFGUI file needed for this visual change. Restart Python after transfer; run EFKEY again if using calibrated bindings.

**ENTER/RIGHT** advances a guide, **LEFT** returns one page, and **CLEAR/0** returns to the menu. The old CLEAR-then-ENTER sequence is removed. Pages show at most five body lines and 28 characters per line. Labels wrap; they are not shortened. Long formulas prefer line breaks at equation operators. Use Display: graphic/text to switch to text; fallback is automatic if graphics cannot load. Graphs and geometry sketches still use CLEAR to dismiss their view.

## Fast update from the first E-Field release

Use **EField_Studio_v2_Patch.zip** rather than resending the full installation. Unzip it and select all eight Python files inside PATCH in ONE file-picker selection. Enable **Replace existing content with the same name**, then send once. It includes APC, APCORE, EFAPP, EFGUI, EFCHK, EFCALC, EFPLOT and EFFINAL. The installed E&M catalogs and derivation notes remain in place.

TI Connect CE was checked and did not detect the connected Evo. TI Connect Evo is the supported transfer application for this model; it is web-based. Keep its tab open until the transfer finishes. Restart the Python shell after replacing files so it does not keep old imported code.

## Included models and guidance

- Ring on its axis: density, dq, projection, integral, exact E and V, direction, limits at x=0, x=R, +/-infinity, near/far approximations, derivative, signed and magnitude extrema, curvature, and solving for Q or either positive distance corresponding to E.
- Finite rod on its perpendicular bisector: FULL length L, midpoint coordinates, cancellation, Cartesian and trig integrations with both endpoint bounds, exact field, potential, limits, derivative, monotonicity, near infinite-line and far point-charge behavior. If R means half rod length, R=L/2 is stated explicitly.
- Finite rod beyond an end: x is measured from the NEAR END. Includes integral, limits, derivative, potential, inverse distance, and semi-infinite limit.
- Infinite line: integration and Gauss-law checks, signed field, reference potential V(R)=0, limits, and extrema. V(infinity)=0 is not possible for the ideal infinite line.
- Arc at its center: lambda versus Q, arc length, radians, signed component integration, arbitrary midpoint direction, semicircle/quarter-circle/full-ring cases, potential, and maxima under both fixed-lambda and fixed-Q constraints. The notes' 180-degree maximum applies at fixed lambda.

The new derivations were checked against all seven pages of the user-provided **8.4 corrected.pdf**. **COVERAGE.md** maps the pages and requested features to calculator menus.

## Additional tools

Two-ring cancellation ratios and net signed axial fields; 2D point-charge superposition; signed sums of arc sectors for ranking problems; potential and test-charge force; E&M equation reference; numerical derivatives, integrals, linear systems and ODE tools; custom function plots; custom numerical limit tables and sampled interval extrema.

Custom limit/extrema results are numerical evidence rather than symbolic proofs. Narrow peaks, poles, cusps, and oscillations can defeat sampling. Exact limits and extrema for the standard five models are given in the derivation cards.

Arc prompts explicitly ask for degrees and convert internally. All math-expression trig functions use radians. For the ring, R is radius and x is distance from the CENTER. For the bisector rod L is full length; for the axial rod x is distance from the NEAR END. Ideal line models are singular on the charge itself.

## Files / recovery

TRANSFER is the complete installation for a fresh calculator. UPDATE contains the new EF files and updated shared support files for an older AP Physics installation. Do not transfer both folders. For the already-installed E-Field release, use the seven-file patch above. Keep names and capitalization. Local generated Mechanics restore copies are in the sibling Mechanics_Restore_2026-10-30 folder; those are the original local sources, not an export of possible calculator edits.

GUI and solver code are split into small action modules and released on return to reduce memory pressure. No compressed code loader or exec-based decoding is used. If MemoryError appears, restart Python and run EFIELD directly. Actual heap use, key handling and graphical rendering require your calculator to verify.
