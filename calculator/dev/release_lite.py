"""Package only tested plain Python; optional extras stay outside the base install."""
import ast, shutil, json, hashlib, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REL=ROOT/'AP_Physics_C_Evo_Fixed'
BASE=REL/'TRANSFER_FIRST'
EXTRA=REL/'OPTIONAL_TOOLS'
BASE.mkdir(parents=True,exist_ok=True)
EXTRA.mkdir(exist_ok=True)
optional={'APTOOLS.py','APMECH.py','APEM.py','APLAB.py'}
for p in (ROOT/'APC_LITE').glob('*.py'):
    shutil.copyfile(p,(EXTRA if p.name in optional else BASE)/p.name)
base_bytes=sum(p.stat().st_size for p in BASE.glob('*.py'))
extra_bytes=sum(p.stat().st_size for p in EXTRA.glob('*.py'))
notes=ast.parse((ROOT/'APC_EVO/APNOTES.py').read_text())
values={n.targets[0].id:ast.literal_eval(n.value) for n in notes.body if isinstance(n,ast.Assign)}
concepts='# AP Physics C concept reference\n\nThese notes stay on your computer to reduce calculator memory use. Formula assumptions and variable definitions still appear on the calculator.\n\n'
for u,items in values['N'].items():
    concepts+='## Unit '+str(u)+'\n\n'
    for title,text in items: concepts+='### '+title+'\n\n'+text+'\n\n'
concepts+='## Labs and reasoning\n\n'
for title,text in values['LAB']: concepts+='### '+title+'\n\n'+text+'\n\n'
(ROOT/'CONCEPTS.md').write_text(concepts)
readme=f'''# AP Physics C - corrected TI-84 Evo release

Use this release instead of the original packed edition. TI's Python Run action imports programs; both launchers now start automatically when imported. The compressed loader has been removed. This v3 revision also removes the unsupported isalnum call and the related character-predicate methods. APCHECK prints APCHECK START v3 so you can confirm the new files loaded.

## Replace the original toolkit

1. Unzip **AP_Physics_C_Evo_Fixed.zip** on your computer.
2. In [TI Connect Evo](https://connectevo.ti.com/), transfer all **22 Python files in TRANSFER_FIRST**. Allow them to replace the old files with the same names. Keep names and capitalization.
3. Remove the old toolkit's **APLOAD**, **APNOTES**, and **APTOOLS** Python files if present. APTOOLS has a new optional replacement. Other programs do not need to be deleted to fix the silent startup bug.
4. Restart or reinitialize the Python shell to clear earlier imports, then run **APCHECK**. You should see **APCHECK START**, then **SELF CHECK PASS**, then **8 numeric checks passed.** Press Enter to finish. A failure or memory error prints an explicit message.
5. Restart the Python shell again and run **APC**. The menu should appear immediately. Try Mechanics -> Forces/dynamics -> Newton second law -> Solve -> F. Enter m=2 and a=3: expect **F N = 6**.

The main install is **{base_bytes:,} bytes of plain source**. Source size is not a measurement of runtime memory. Actual Evo heap usage and screen behavior still require your calculator to verify.

## What remains included

All **13 AP Physics C units**, **160 equations**, and **566 unknown targets** remain: 525 direct targets and 41 numerical targets requiring a bracket. Each equation shows its variable definitions, SI units, and assumptions. The menus show five choices per page: **1-5 select, 0 back, 8 previous, 9 next**, followed by Enter. At numeric prompts **q** cancels, Enter reuses a displayed value, and **ans** uses the last answer. Inputs accept scientific notation and expressions such as `pi/4`, `sqrt(2)`, and `ke*qe`. Angles are always radians; default g is 9.8 m/s^2.

Math tools include derivatives, definite integrals, bracketed roots, stable quadratic solutions, linear systems, a first-order numerical ODE solver, and percent comparisons. Graphs include formula-variable sweeps, custom f(x), projectile paths, motion, SHM, RC voltage, and RL current. They use TI's ti_plotlib. Preset plots sample **40 points** to save memory. Poles and narrow peaks can be missed; use narrow windows. Use equation graphs or custom f(x) for other fields, potentials, velocities, and accelerations.

## Optional multi-step tools

The **OPTIONAL_TOOLS** folder contains the original 15 multi-step solvers in smaller groups. Transfer **APTOOLS.py** plus the group you want, if sufficient Python program space remains:

- **APMECH.py**: vectors, projectiles, collisions, COM/momentum, Atwood machines, SHM initial states, and rolling inclines.
- **APEM.py**: charge superposition, spheres, equivalent components, multi-battery resistor circuits, RC/RL transients, and motional emf/drag.
- **APLAB.py**: linear regression.

All four add-ons total **{extra_bytes:,} source bytes**. Uninstalled groups show an explanatory message when selected. The ordinary equation solvers remain available without these add-ons. If all add-ons exceed available space, keep only the group needed or keep the main install alone.

## Memory and scope changes

The main menu loads only a selected unit or tool module. Equation catalogs remain as text until a selected row is needed. Finished unit/tool imports are removed from the import cache when supported and garbage collection runs. No compressed source is expanded or executed. Full concept notes are in **CONCEPTS.md** on your computer; model assumptions remain on the calculator. The last answer replaces the old eight-answer history.

If MemoryError repeats, restart the Python shell and record the program, selected menu, and traceback line. Do not repeatedly delete unrelated work to troubleshoot it. The program has been checked on desktop Python, including TI-style import startup; it has not been run on a physical Evo.

See **FORMULAS.md**, **COVERAGE.md**, and **VALIDATION_LITE.md** for details. These tools evaluate models you select; they do not interpret every word problem or supply symbolic derivations. Numerical brackets must be continuous and sign-changing. Calculus and graph results are numerical estimates.
'''
(ROOT/'README.md').write_text(readme)
validation='''# Corrected-release validation

Verified on desktop Python on October 7, 2026. The plain install passes **29 test groups**.

- All 160 formula entries were compared against the original catalog. Every explicit and numerical target was exercised using consistent states generated from independent symbolic evaluation: **525 direct targets and 41 bracketed targets**.
- Physics fixtures cover projectile flight, collision conservation, pulley dynamics, SHM initial conditions and energy, RC/RL limits, signed charge superposition, sphere continuity, equivalent components, regression, and multi-battery circuits including a floating voltage source.
- Numerical checks cover arithmetic precedence, scientific notation, rejection of invalid/complex input, cancellation residuals, stable roots, zero acceleration, domains and geometry, integration, derivatives, and singular linear systems.
- A regression test removes isalnum, isdigit, and isalpha from an input string and verifies expression parsing still works. The two-file APCORE/APCHECK patch was also checked against the prior corrected install, including its self-check and the Newton example.
- APC and APCHECK were executed under an imported module name, matching TI's launch behavior. APC displayed its menu without a manual main() call; APCHECK printed its start and pass messages. An end-to-end menu calculation returned F=6 N for m=2 kg and a=3 m/s^2.
- All 13 units were visited in one simulated session, verifying that catalog and solver imports are evicted on return. Expression temporary values are removed after success and errors.
- Graph tests mock ti_plotlib and verify method order, windows, 40-point default data, and breaks at undefined samples. These are API tests; no physical rendering is asserted.
- Every transferred file is plain ASCII Python, has a name at most eight characters long, and contains neither APLOAD nor exec-based source decoding. The developer fixture materializes full unit tables solely for independent verification; calculator code parses one selected row.

Actual results are in dev/lite-test-results.txt. Reproduce with `python dev/build_lite.py` followed by `python dev/test_lite.py` in a development environment with SymPy available. SymPy is used only by the desktop oracle, never by calculator programs.

Physical Evo memory, file transfer, key behavior, and plot rendering remain unverified. File sizes do not establish that every Evo memory state can run the program. After replacement, use the eight-check APCHECK smoke test, then the Newton example and a manual graph check. Restart the Python shell between APCHECK and APC to clear its imports.

The original packed edition's validation did not test TI-style startup or hardware heap behavior. It is superseded by this release. Its numerical tests alone did not establish device compatibility.
'''
(ROOT/'VALIDATION_LITE.md').write_text(validation)
for name in ['README.md','FORMULAS.md','COVERAGE.md','CONCEPTS.md','VALIDATION_LITE.md']:
    shutil.copyfile(ROOT/name,REL/name)
shutil.copyfile(ROOT/'dev/lite-test-results.txt',REL/'TEST_RESULTS.txt')
manifest={str(p.relative_to(REL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(REL.rglob('*')) if p.is_file()}
(REL/'SHA256.json').write_text(json.dumps(manifest,indent=2))
archive=ROOT/'AP_Physics_C_Evo_Fixed.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(REL.rglob('*')):
        if p.is_file(): z.write(p,str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len([n for n in z.namelist() if '/TRANSFER_FIRST/' in n and n.endswith('.py')])==22
print('Base:',base_bytes,'bytes; optional:',extra_bytes,'bytes; archive:',archive.name)
