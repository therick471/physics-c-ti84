# Download and install APC

## 1. Download everything

Use **Download APC — complete pack** on the repository home page. Extract the ZIP on your computer, then open **START_HERE.md**. You do not need to install Python or coding tools on your computer.

## 2. Find your calculator

| Model | Folder inside `APC_Complete` | What is available |
|---|---|---|
| TI-84 Evo | `TI84_EVO/FULL_APC/TRANSFER` | Full Mechanics + E&M toolkit: 26 files |
| TI-84 Evo, focused electrostatics | `TI84_EVO/EXAM2/TRANSFER` | Exam 2 and E-Field Studio: 40 files |
| TI-84 Evo, E-Field Studio only | `TI84_EVO/EFIELD/TRANSFER` | Studio and E&M reference: 34 files |
| TI-84 Plus CE Python | `TI84_PLUS_CE_PYTHON/TRANSFER` | Exam 2 starting install: 13 files; every other tool is included under TOPICS |
| TI-84 Evo-T | Corresponding Evo folder | Same family instructions; regional device behavior has not been checked |
| TI-84 Plus CE-T Python | CE Python folder | Same family instructions; regional device behavior has not been checked |
| TI-84 Plus / Plus T / Silver Edition / Pocket / Pocket SE | None | These models do not run the included Python programs |
| TI-84 Plus C Silver Edition | None | These programs require Python |
| TI-84 Plus CE / CE-T without Python | None | A color screen alone does not mean Python support |

Both models receive the full feature library. CE Python uses smaller topic installs to fit its memory limit. [CE topic guide](CE_PYTHON.md). Choose one complete folder; do not merge folders or apply Evo interface files to a CE Python installation.

## 3. Send to an Evo

1. Turn on the calculator and connect it to your computer using a USB **data** cable.
2. Open [TI Connect Evo](https://connectevo.ti.com/) in a browser the site supports, such as Chrome. Choose **CONNECT TO CALCULATOR**, select your calculator, and allow the connection.
3. Choose **SEND FILES → SEND TO CALCULATOR**. Select **every `.py` file** from the chosen `TRANSFER` folder in one batch.
4. Keep the original filenames. Back up any copies you edited before allowing replacement. Send once and wait until every file finishes.
5. Open Python on the calculator and restart/reinitialize its shell. Run **APC**.

## 4. Send to a Plus CE Python

1. Confirm that the calculator is the **Python edition** and has the Python app.
2. Install/open [TI Connect CE for Windows or Mac](https://education.ti.com/en/products/computer-software/ti-connect-ce-sw). Connect the powered-on calculator with a USB data cable.
3. Open **Calculator Explorer**. For Exam 2, drag in all 13 `.py` files from `TI84_PLUS_CE_PYTHON/TRANSFER`; for another topic, use only that topic's TRANSFER folder. Do not send all topics together. Use drag-and-drop or **Actions → Send to Calculators**.
4. Keep filenames unchanged and choose **RAM**. Back up your own edits before replacing matching names, then send all files.
5. Quit/reopen the calculator's Python app and run **APC**. Before changing topics, back up and archive/remove the previous topic's APC files using its file list. [Detailed switching steps](CE_PYTHON.md).

TI Connect CE converts `.py` files automatically. Use Calculator Explorer rather than the TI-BASIC editor. The Python app runs the files from RAM. The CE interface still needs a check on the recipient's physical calculator.

## First use

Full APC: run `APC`. Try Mechanics → Forces/dynamics → Newton second law → Solve → F, with m=2 and a=3; the answer should be 6 N.

E-Field Studio: run `EFIELD` for the models, or `APC` for the E&M reference. If keys do not respond, run `EFKEY` and follow its prompts.

Exam 2: run `APC → Exam 2 electrostatics` or `EXAM2`. For a uniform sphere with Q=2e-9 C, R=1 m and r=0.5 m, the field should be about 8.99 N/C.

After a replacement, always restart calculator Python so it loads the new files. Do not send the ZIP itself, guides, or all model folders at once.
