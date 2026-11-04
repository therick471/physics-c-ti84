from pathlib import Path
import json,ast,zipfile,hashlib,shutil,re
ROOT=Path(__file__).resolve().parents[1]
REL=ROOT/'EField_EM'
files=list((REL/'TRANSFER').glob('*.py'))
count=len(files);size=sum(p.stat().st_size for p in files)
test_count=re.search(r'Ran (\d+) tests',(ROOT/'dev/efield-v2-test-results.txt').read_text()).group(1)
readme=f'''# E-Field Studio v2 - TI-84 Evo / E&M only

Run **EFIELD** for the new field solver. **APC** opens the E&M-only toolkit. Mechanics units APU01-APU07 are excluded; APU08-APU13 remain. This release uses {count} plain Python files, totaling {size:,} source bytes. Source storage and runtime heap are different; real-device execution must be checked.

## Final formulas

**APC > Final formulas** and **EFIELD > Final formulas** open the answer-only browser. Each of the five field-model menus also has a **Final formulas** shortcut. This section asks for no numerical inputs and contains no derivation steps. It shows final E and V expressions, variable definitions and domains, useful limit/extremum results, and superposition formulas for rings, point charges and arc sectors. **All other E&M equations** browses every equation in all six retained E&M units with its conditions.

For the already installed toolkit, **EField_Final_Formulas_Update.zip** contains the three required files: APC, EFAPP and EFFINAL. Send all three in one batch with replacement enabled, then restart Python. Existing graphic styling, keyboard bindings in EFGUI, and highlight alignment are retained; rerun EFKEY after restarting if you use calibrated keys.

## Evo keyboard repair (v3 patch)

The previous menu recognized CE Python codes but omitted Evo keypad codes. The repair adds Evo bindings and prefers its blocking `get_key(1)` API when available. CE and named-string events remain supported. Unknown key presses are ignored without redrawing the menu.

For an already installed E-Field Studio, send the TWO files from **EField_Studio_v3_Keyboard_Patch.zip** in one batch with replacement enabled. Restart Python. Run **EFKEY** to measure UP, DOWN, LEFT, RIGHT, ENTER and CLEAR directly on this calculator, then follow the DOWN/ENTER menu test. A successful test prints **PASS: hardware navigation** and opens EFIELD using the learned bindings. Calibration applies for that Python session; ordinary EFIELD starts with the built-in defaults. Run EFKEY again if you need to recalibrate after restarting Python.

The desktop suite now has 26 test groups, including both numeric key families, named events, unknown/no-key events, and calibration with arbitrary measured codes followed by an actual menu selection. Desktop tests do not verify a physical keyboard.

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
'''
(REL/'README.md').write_text(readme.replace('26 test groups',test_count+' test groups'))
coverage='''# Coverage of 8.4 corrected.pdf

| Notes / requested feature | Included location |
|---|---|
| Page 1: discrete vector sums; continuous dq; Coulomb integral; lambda | Point charges / arc-sector sums; all five derivation guides |
| Page 2: finite rod axis, near-end bounds x..x+L, field, limits and graph | Rod: beyond an end; calculate, derivation, extrema, graph |
| Pages 3-4: perpendicular bisector, symmetry, projection, trig change of variable, endpoint bounds | Rod: perpendicular bisector; all ten guide chapters |
| Page 4: finite answer in Q or lambda, a->0 and far limit | Bisector rod: density input choice, guide chapters 4,7,8 |
| Page 4: infinite line with +/-90-degree bounds | Infinite straight line; trig integral and Gauss check |
| Pages 4-5: arc length R*phi, dq=lambda*R*dtheta, symmetry and sine result | Arc: center / sectors; chapters 1-5 |
| Page 5: arc maximum at phi=pi | Arc extrema; explicitly distinguishes fixed lambda from fixed Q |
| Pages 5-6: ring density, azimuth variable, projection cos(theta), full integral | Ring: on its axis; chapters 1-4 |
| Pages 6-7: ring limits at zero/infinity, point-charge approximation, derivative and +/-R/sqrt(2), graph | Ring guide chapters 5-10; exact numeric extrema and plots |
| Requested x->R limit | Ring guide: kQ/(2sqrt(2)R^2); bisector guide states R=L/2 if that symbol denotes half-length |
| Minima / maxima and signed charge | Exact ring signed extrema and |E| extrema; monotonic rod/line behavior; fixed-Q versus fixed-density arc extrema |
| Additional useful information | Potential, test-charge force, backward source/distance solves, inverse ring's two branches, domains and units |
| Linked two-ring question | Two rings / point charges -> Two rings: charge ratio; ratio 2^(5/2)/5^(3/2)=0.505964426 |

In these guides R is not silently reused as full rod length. Rod formulas use full L. Observation x is distinguished from the source-integration coordinate and from ring azimuth.
'''
(REL/'COVERAGE.md').write_text(coverage)
shutil.copyfile(ROOT/'dev/efield-v2-test-results.txt',REL/'TEST_RESULTS.txt')
update=REL/'UPDATE'
update.mkdir(exist_ok=True)
for f in files:
 if f.stem.startswith('EF') or f.stem in ['APC','APCORE','APDATA','APGRAPH']:
  shutil.copyfile(f,update/f.name)
patchfiles=['APC','APCORE','EFAPP','EFGUI','EFCHK','EFCALC','EFPLOT','EFFINAL']
patchdir=ROOT/'EField_Navigation_Fix'
patchdir.mkdir(exist_ok=True)
for name in patchfiles:shutil.copyfile(REL/'TRANSFER'/(name+'.py'),patchdir/(name+'.py'))
patchreadme='''E-Field Studio v2 patch with Evo keyboard repair\n\nUnzip, select all seven .py files in PATCH together, and send them in one TI Connect Evo batch. Enable replacement of matching names. Restart the Python shell, run EFCHK (expect PASS: 12 physics + 2 UI), restart once more, then run EFIELD.\n\nUP/DOWN selects; ENTER opens. LEFT/RIGHT changes pages. In a guide ENTER/RIGHT advances, LEFT returns, CLEAR/0 exits. Full labels wrap and no longer require CLEAR then ENTER.\n\nDesktop verification: 26 test groups passed. If keys still need calibration, also install EFKEY from the v3 keyboard patch and run EFKEY instead of EFIELD. Physical key handling and rendering require an on-calculator check.\n'''
for name in ['EField_Studio_v2_Patch.zip','EField_Navigation_Fix.zip']:
 with zipfile.ZipFile(ROOT/name,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('README.txt',patchreadme.replace('all seven','all eight').replace('26 test groups',test_count+' test groups'))
  for f in sorted(patchdir.glob('*.py')):z.write(f,'PATCH/'+f.name)
keyboard=ROOT/'EField_Keyboard_Fix'
keyboard.mkdir(exist_ok=True)
for name in ['EFGUI.py','EFKEY.py']:shutil.copyfile(REL/'TRANSFER'/name,keyboard/name)
keyreadme='''Evo keyboard repair - E-Field Studio v3 patch\n\nSend BOTH .py files in PATCH together using TI Connect Evo, with replacement enabled. Restart Python, then run EFKEY. Press and RELEASE each requested key: UP, DOWN, LEFT, RIGHT, ENTER, CLEAR. Then complete the DOWN/ENTER menu test. It prints PASS: hardware navigation and opens EFIELD with your measured bindings. Bindings last for this Python session. Run EFKEY again to recalibrate after restarting, or run EFIELD to use the repaired built-in defaults.\n\nThe previous version recognized CE Python codes but omitted Evo keypad codes. This repair supports Evo, CE, and named-string keys, prefers get_key(1) on Evo, and ignores unknown events. EFKEY learns the actual codes instead of depending on a hard-coded mapping.\n\n26 desktop test groups passed. Physical keyboard success is confirmed only when the EFKEY menu test passes on your calculator.\n'''
with zipfile.ZipFile(ROOT/'EField_Studio_v3_Keyboard_Patch.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('README.txt',keyreadme.replace('26 desktop test groups',test_count+' desktop test groups'))
 for f in sorted(keyboard.glob('*.py')):z.write(f,'PATCH/'+f.name)
plain=ROOT/'EField_Plain_UI_Update'
plain.mkdir(exist_ok=True)
shutil.copyfile(REL/'TRANSFER/EFGUI.py',plain/'EFGUI.py')
with zipfile.ZipFile(ROOT/'EField_Plain_UI_Update.zip','w',zipfile.ZIP_DEFLATED) as z:z.write(plain/'EFGUI.py','EFGUI.py')
formula=ROOT/'EField_Final_Formulas_Update'
formula.mkdir(exist_ok=True)
for name in ['APC.py','EFAPP.py','EFFINAL.py']:shutil.copyfile(REL/'TRANSFER'/name,formula/name)
with zipfile.ZipFile(ROOT/'EField_Final_Formulas_Update.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('README.txt','Send all three .py files in PATCH together with replacement enabled. Restart Python. Open APC > Final formulas, EFIELD > Final formulas, or a model > Final formulas. This is a read-only browser of answers and conditions; no numeric inputs or derivation steps. All six E&M equation catalogs are also accessible. '+test_count+' desktop test groups passed.\n')
 for f in sorted(formula.glob('*.py')):z.write(f,'PATCH/'+f.name)
manifest={str(p.relative_to(REL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in REL.rglob('*') if p.is_file() and p.suffix!='.pyc' and p.name!='SHA256.json'}
(REL/'SHA256.json').write_text(json.dumps(manifest,indent=2))
p=ROOT/'EField_Studio_Evo.zip'
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
 for folder in ['TRANSFER']:
  for f in sorted((REL/folder).glob('*.py')):z.write(f,'EField_EM/'+folder+'/'+f.name)
 for f in ['README.md','COVERAGE.md','TEST_RESULTS.txt']:z.write(REL/f,'EField_EM/'+f)
with zipfile.ZipFile(p) as z:assert z.testzip() is None
print('Packaged',count,'files;',size,'source bytes')
