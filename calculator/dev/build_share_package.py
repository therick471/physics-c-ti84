"""Assemble a clean, complete handoff with distinct Evo and CE Python profiles."""
from pathlib import Path
import ast
import hashlib
import json
import shutil
import sys
import zipfile

DEV=Path(__file__).resolve().parent
CALC=DEV.parent
WORKSPACE=CALC.parent
BASE=CALC/'EField_EM/TRANSFER'
DEST=WORKSPACE/'Share_AP_Physics_C_EM'
ARCHIVE=WORKSPACE/'Share_AP_Physics_C_EM.zip'
sys.path.insert(0,str(DEV))
from package_toolkit import minify

CE_RAW='''def raw_key():
    from ti_system import wait_key
    while True:
        code=wait_key()
        if code is not None and code!=0 and code!='':return code
'''
CE_ACTION='''def key_action(code):
    if code in KEYMAP:return KEYMAP[code]
    if isinstance(code,str):
        code=code.strip().lower()
        if code in ('0','q','b','clear','esc'):return 'back'
        if code in ('8','left'):return 'prev'
        if code in ('9','right'):return 'next'
        if code in ('up','down','enter'):return code
        if code in ('1','2','3','4','5'):return code
        return ''
    if code in (9,62):return 'back'
    if code in (13,5):return 'enter'
    if code in (14,2,250):return 'prev'
    if code in (15,1,251):return 'next'
    if code==3:return 'up'
    if code==4:return 'down'
    if 243<=code<=247:return str(code-242)
    return ''
'''

def ce_gui(source):
    tree=ast.parse(source)
    replacements={'raw_key':ast.parse(CE_RAW).body[0],
                  'key_action':ast.parse(CE_ACTION).body[0]}
    for i,node in enumerate(tree.body):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEXT_ASCENT' for t in node.targets):
            node.value=ast.Constant(0)
        if isinstance(node,ast.FunctionDef) and node.name in replacements:
            tree.body[i]=replacements[node.name]
    ast.fix_missing_locations(tree)
    return minify(ast.unparse(tree)+'\n')

EVO_INSTALL='''TI-84 EVO — INSTALL

Use the TI Connect Evo website: https://connectevo.ti.com/
Official guide: https://education.ti.com/en/product-resources/eguides/eguide-84-evo/evo-connect-user-guide

1. Extract the ZIP first. Open TI84_EVO/TRANSFER on your computer.
2. Turn on your Evo and connect it with a USB DATA cable. Open TI Connect Evo
   in Chrome or another browser the site accepts. Allow its calculator connection.
3. Click CONNECT TO CALCULATOR, choose your Evo, and Connect.
4. Open SEND FILES, then SEND TO CALCULATOR. Select ALL 34 .py files from
   TI84_EVO/TRANSFER together. Click the first file, hold Shift, and click the
   last file if you need to select a complete range.
5. Keep the original names and choose RAM. For an update, enable replacement
   of matching names after backing up any copies you edited yourself.
6. Click SEND once. Wait for FILES SENT TO CALCULATOR. Keep the connection
   open until all 34 files finish. Reconnect and retry only if a transfer failed.
7. Continue with FIRST RUN in README.txt. Run programs in the Python app.

The desktop TI Connect CE app is for the CE installation below. Use the Evo
website for this model. Do not send the ZIP, this guide, or the CE profile.
'''

CE_INSTALL='''TI-84 PLUS CE PYTHON EDITION — INSTALL

Get TI Connect CE for Windows or Mac from TI:
https://education.ti.com/en/products/computer-software/ti-connect-ce-sw
Official Python-transfer guide:
https://education.ti.com/html/eguides/connectivity/TI-Connect-CE/EN/Content/EG_84_TIConnect/M_UsePython/M_UsePython.HTML

1. Check the model: it must be the TI-84 Plus CE PYTHON edition and have a
   working Python app. A regular TI-84 Plus CE without Python cannot run this.
2. Extract the ZIP. Install/open TI Connect CE on a supported Windows or Mac
   computer. Connect the powered-on calculator with a USB DATA cable.
3. Open Calculator Explorer and select your calculator. Back up any matching
   programs you edited before replacing them.
4. Select ALL 34 .py files in TI84_PLUS_CE_PYTHON/TRANSFER and drag the group
   into Calculator Explorer, or use Actions > Send to Calculators.
5. Keep all original names. Set Location to RAM. Enable replacement of matching
   names for an update, select the intended calculator, and click Send.
6. Wait until all files finish. TI Connect CE automatically converts .py files
   to Python AppVars. You do not need to generate .8xv files yourself.
7. Open the calculator's Python app and continue with FIRST RUN in README.txt.

Use Calculator Explorer, not the TI-BASIC Program Editor. Python programs need
to be in RAM to load/run in the Python app. Do not send the Evo profile or ZIP.
If Python or TI_DRAW is missing, see TROUBLESHOOTING.txt and the official
CE OS/apps page: https://education.ti.com/en/software/update/84-ce-software-update
'''

FIRST_RUN='''FIRST RUN — BOTH MODELS

1. After transfer, restart/reinitialize the PYTHON SHELL using its Tools menu
   (Reinitialize Shell). On Evo this may be labeled differently; use the Python
   app's shell-restart/reinitialize action. This clears old imported modules.
2. Run EFCHK from the Python file list. Expected output:
      EFIELD CHECK START v2
      PASS: 12 physics + 2 UI
   This checks calculations and text layout; it does not test physical keys.
3. Restart the Python shell again. Run EFKEY. Press and RELEASE each requested
   key: UP, DOWN, LEFT, RIGHT, ENTER, CLEAR. Press ENTER at its prompt, then
   follow the DOWN -> ENTER menu test. It should print:
      PASS: hardware navigation
   Press ENTER when asked to open EFIELD. Learned keys last for this Python
   session. Run EFKEY again after restarting if calibration is needed.
4. For ordinary use, run EFIELD for field models or APC for the full E&M toolkit.
   Both can also use their built-in key defaults without EFKEY.
5. APC > Final formulas opens the answer-only formula browser. EFIELD has the
   same section and a Final formulas shortcut inside each field model.

Optional extra check: APCHECK prints SELF CHECK PASS and 8 numeric checks
passed. Restart the shell after checks before normal use.

TRANSFER ALL FILES, but normally run only APC, EFIELD, EFCHK, EFKEY or APCHECK.
Files such as APCORE, EFGUI, APU08 and EFN0 are support modules, not launchers.
'''

CONTROLS='''CONTROLS AND QUICK REFERENCE

Menus: UP/DOWN selects; ENTER opens; LEFT/RIGHT changes pages; CLEAR or 0 returns.
Numbers 1–5 select a displayed entry; 8/9 moves to the previous/next menu page.
Guide/formula cards: ENTER or RIGHT advances, LEFT goes back a page,
CLEAR or 0 exits. UP/DOWN also moves between guide pages.
Graphs and sketches: CLEAR dismisses the view. ON interrupts a running program.
At numeric/expression prompts: type q then ENTER to cancel. CLEAR alone is not
the same as canceling a numeric prompt. ENTER accepts a displayed default.

Main programs:
  EFIELD    Ring, rod, line and arc field studio.
  APC       Field studio + six E&M equation units + math and graphing tools.
  EFKEY     Calibrate navigation and launch EFIELD in the same session.
  EFCHK     12 physics checks + 2 text/menu layout checks.
  APCHECK   8 arithmetic/expression/root checks.

Units: SI. Enter charge in coulombs (example: 1e-9 for 1 nC), length in meters.
Use * for multiplication and ^ for powers. pi, sqrt(2), sin(pi/2), ln(2),
scientific notation and the last computed ans are supported in numeric inputs.
R is ring/arc radius. L is FULL rod length. Ring x is from the center;
bisector-rod x is perpendicular from the midpoint; end-rod x is from the near end.
Most trig inputs use radians. Arc geometry prompts explicitly ask for degrees
and convert internally; formulas use sweep phi in radians.

Try this after installation:
  EFIELD > Ring: on its axis > Calculate E, V and force
  Choose Total Q, then R=1, Q=1e-9, x=1 (follow the prompt order shown).
  Expected E about 3.1775794 N/C and V about 6.3551588 V.

Included: five complete field guides; E and V solvers; exact model limits and
extrema; backward solves; graphing; two-ring and charge/arc superposition;
84 E&M reference equations and final-formula cards; numerical calculus, linear
systems and ODE tools. Mechanics units are not included in this E&M edition.
Custom limit/extremum sampling is an estimate, not a symbolic proof.
'''

TROUBLE='''TROUBLESHOOTING

Calculator is not detected
  Use a data-capable USB cable, turn the calculator on, reconnect, and select it
  in the connection dialog. Close another calculator connection using the same
  USB port. Evo uses the TI Connect Evo website; CE Python uses TI Connect CE.
  For browser/OS requirements, consult the linked TI product pages.

ImportError / module not found / only the launcher was sent
  Send ALL 34 .py files from ONE model's TRANSFER folder, not just APC/EFIELD.
  Keep names and capitalization. Names must not become PYTHON01, etc.
  Restart Python after transfer. On CE, make sure program AppVars are in RAM.

It still runs an old menu after an update
  Reinitialize/restart the Python shell, then run APC or EFIELD again.
  Merely returning to the file list can leave imported modules cached.

MemoryError while running
  Restart the Python shell and run EFIELD directly before opening other tools.
  Calculator storage and Python runtime heap are different. If transfer itself
  reports low storage, back up and archive unused programs/AppVars first.
  Keep this package's program files in RAM when using them on CE Python.
  Do not delete TI_DRAW/TI_IMAGE or individual toolkit dependencies to save space.

Menus do not respond / a key does the wrong thing
  Confirm you used the correct model folder. Restart Python and run EFKEY;
  follow each press-and-release prompt, then the DOWN/ENTER test.
  Calibration lasts until the Python shell is restarted.

The highlight is above/below the selected entry
  The profiles use different text alignment. Reinstall EFGUI.py from the correct
  model folder, restart Python and try again. Do not mix profile files.

Missing Python app, TI_DRAW, or ti_plotlib
  Python itself must work on the calculator first. TI_DRAW supplies graphical
  menus/sketches; ti_plotlib supplies plots. The program uses text menus when
  TI_DRAW cannot load. Install the official OS/apps bundle for YOUR model if a
  built-in module is missing. Obtain TI software through the official links;
  do not copy Evo binary modules to CE or CE binary modules to Evo.

  CE OS/apps: https://education.ti.com/en/software/update/84-ce-software-update
  CE module guide: https://education.ti.com/html/webhelp/eg_ti84pluscepy/uk/content/eg_pythonappprog/m_pyentry/m_addon.HTML
  Evo updates: https://education.ti.com/en/product-resources/eguides/eguide-84-evo/evo-connect-user-guide

Errors on a numeric input
  Use SI units and the domain shown. R,L must be positive; ideal rod/line models
  cannot be evaluated on their charge. Infinite-line input is charge per length,
  not a finite total charge. A ring inverse may have TWO positive distances.

To uninstall
  Back up anything you edited, then remove only the toolkit .py/Python AppVar
  names listed in MANIFEST.json. Leave calculator system modules in place.

When asking for help
  Include calculator model, OS/Python version, program name, selected menu,
  entered values and the exact error or a screen photo. The Plus CE profile has
  desktop checks with simulated TI APIs; physical CE memory/display behavior
  still needs verification on the recipient's device.
'''

LINKS='''OFFICIAL SOFTWARE AND DOCUMENTATION

TI Connect Evo (browser-based): https://connectevo.ti.com/
Evo transfer/connection guide:
https://education.ti.com/en/product-resources/eguides/eguide-84-evo/evo-connect-user-guide
TI Connect CE (Windows/Mac download and system requirements):
https://education.ti.com/en/products/computer-software/ti-connect-ce-sw
CE Python .py transfer and RAM instructions:
https://education.ti.com/html/eguides/connectivity/TI-Connect-CE/EN/Content/EG_84_TIConnect/M_UsePython/M_UsePython.HTML
CE OS/apps downloads:
https://education.ti.com/en/software/update/84-ce-software-update
CE drawing modules and text coordinates:
https://education.ti.com/html/webhelp/eg_ti84pluscepy/uk/content/eg_pythonappprog/m_pyentry/m_addon.HTML
CE Python key-code reference:
https://education.ti.com/html/webhelp/eg_ti84pluscepy/en/content/eg_pythonappprog/m_appendix/m_keypadmap.HTML
CE interactive drawing with wait_key():
https://education.ti.com/en/activities/ti-codes/python/ti-84p-ce-python/python-modules

Links checked while preparing this package on 2026-11-02. TI software, firmware,
binary add-on modules and installers are obtained from TI, not redistributed
inside this ZIP. All toolkit Python programs needed for transfer are included.
'''

README='''AP PHYSICS C E&M / E-FIELD STUDIO
Complete sharing package — 2026-11-02

START HERE

Send the entire Share_AP_Physics_C_EM.zip to your friend. They should extract it
before installing. No Python installation, pip, coding tools or compiling is
needed on their computer. Use the official TI transfer tool for their model.

CHOOSE EXACTLY ONE PROFILE

Calculator                       Files to send                    Transfer tool
TI-84 Evo                        TI84_EVO/TRANSFER/*.py           TI Connect Evo
TI-84 Plus CE Python edition     TI84_PLUS_CE_PYTHON/TRANSFER/*.py TI Connect CE

Each TRANSFER folder contains all 34 programs. Send every .py file from the
chosen folder together. Both installs are complete, not patches. Their file
names overlap: do not merge the two folders on one calculator.

This package is the E&M edition: Mechanics was intentionally removed. It
includes the latest final-formula section, plain menu styling, keyboard support
and selection-highlight correction. Evo navigation/alignment were checked on
the original physical Evo. CE-specific keys/layout are adapted from TI's
documentation and checked with simulated TI APIs; a physical CE was not
available for testing. Run the included checks on the recipient's calculator.

YOU NEED

- The indicated calculator with a working Python app.
- A computer, internet for the TI software/website, and a USB DATA cable that
  fits the calculator (plus an adapter if your computer needs one).
- Free storage for about 68 KB of program source per profile, plus calculator
  storage overhead and Python runtime heap. Exact sizes are in MANIFEST.json.
- TI's Python runtime modules. TI_DRAW is used for graphic menus and sketches;
  ti_plotlib is used for plots. See troubleshooting if a module is missing.

A regular TI-84 Plus CE WITHOUT Python cannot run this program. This is not a
TI-BASIC program, and the TI-Nspire is not a target of this package.

FOLDER MAP

  README.txt / README.md       These complete installation instructions.
  TI84_EVO/INSTALL.txt         Evo-specific steps.
  TI84_EVO/TRANSFER/           All 34 Evo program files.
  TI84_PLUS_CE_PYTHON/INSTALL.txt   CE-specific steps.
  TI84_PLUS_CE_PYTHON/TRANSFER/     All 34 CE Python program files.
  QUICK_REFERENCE.txt         Controls, main programs, units and a worked input.
  TROUBLESHOOTING.txt         Transfer, memory, keys, missing modules and updates.
  OFFICIAL_LINKS.txt          TI software and reference links.
  VALIDATION.txt              Checks performed and hardware-testing limits.
  CHECKS/                    Desktop test logs.
  MANIFEST.json / SHA256SUMS.txt   File lists, source sizes and integrity hashes.

'''+EVO_INSTALL+'\n'+CE_INSTALL+'\n'+FIRST_RUN+'''
FOR SHARING OR REINSTALLING

Use the ZIP of this complete folder, not old update/patch folders from another
installation. Preserve all names. To update an existing toolkit, back up edited
copies, resend the matching profile's complete TRANSFER contents with replacement
enabled, then restart Python. Your friend's calculator does not need any of
your personal files, class PDFs, login, or account to run the toolkit.

See QUICK_REFERENCE.txt for controls and TROUBLESHOOTING.txt if a check fails.
Official install behavior is documented in the TI guides linked above and in
OFFICIAL_LINKS.txt. Source storage is not a measurement of runtime memory use.
'''

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8')

def main():
    programs=sorted(BASE.glob('*.py'))
    assert len(programs)==34,'Refresh program list and instructions if the install changes'
    DEST.mkdir(exist_ok=True)
    for profile in ['TI84_EVO','TI84_PLUS_CE_PYTHON']:
        target=DEST/profile/'TRANSFER';target.mkdir(parents=True,exist_ok=True)
        for p in programs:
            source=p.read_text('ascii')
            if p.name=='EFGUI.py' and profile=='TI84_PLUS_CE_PYTHON':source=ce_gui(source)
            if p.name=='EFKEY.py':
                source=source.replace('EVO KEY SETUP  v3','KEY SETUP  v3').replace('Keys learned from this Evo:','Keys learned:')
            ast.parse(source)
            write(target/p.name,source)
        write(DEST/profile/'INSTALL.txt',EVO_INSTALL if profile=='TI84_EVO' else CE_INSTALL)
    write(DEST/'README.txt',README)
    write(DEST/'README.md',README)
    write(DEST/'QUICK_REFERENCE.txt',CONTROLS)
    write(DEST/'TROUBLESHOOTING.txt',TROUBLE)
    write(DEST/'OFFICIAL_LINKS.txt',LINKS)
    checks=DEST/'CHECKS';checks.mkdir(exist_ok=True)
    shutil.copyfile(CALC/'dev/efield-v2-test-results.txt',checks/'shared_solver_tests.txt')
    # finalize_share_package.py adds the profile log, validation, hashes and ZIP
    # only after its checks pass.
    print('Prepared',DEST)
    for profile in ['TI84_EVO','TI84_PLUS_CE_PYTHON']:
        entries=list((DEST/profile/'TRANSFER').glob('*.py'))
        print(profile,len(entries),'files,',sum(p.stat().st_size for p in entries),'source bytes')

if __name__=='__main__':main()
