AP PHYSICS C E&M / E-FIELD STUDIO
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

TI-84 EVO — INSTALL

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

TI-84 PLUS CE PYTHON EDITION — INSTALL

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

FIRST RUN — BOTH MODELS

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

FOR SHARING OR REINSTALLING

Use the ZIP of this complete folder, not old update/patch folders from another
installation. Preserve all names. To update an existing toolkit, back up edited
copies, resend the matching profile's complete TRANSFER contents with replacement
enabled, then restart Python. Your friend's calculator does not need any of
your personal files, class PDFs, login, or account to run the toolkit.

See QUICK_REFERENCE.txt for controls and TROUBLESHOOTING.txt if a check fails.
Official install behavior is documented in the TI guides linked above and in
OFFICIAL_LINKS.txt. Source storage is not a measurement of runtime memory use.
