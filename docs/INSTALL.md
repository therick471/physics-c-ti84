# Download and install

## Which TI-84 do you have?

Read the model printed on the calculator and check whether it has the Python app.

| Model | This collection | Transfer software / action |
|---|---|---|
| **TI-84 Evo** | Supported target: Exam 2, E&M sharing profile, full-course corrected toolkit | [TI Connect Evo](https://connectevo.ti.com/) in a supported WebUSB browser |
| **TI-84 Evo-T** | TI lists Evo-T as supported by Connect Evo. These source files are an unverified regional target; no separate Evo-T test was performed | Same Evo transfer route; run checks on the device |
| **TI-84 Plus CE Python edition** | Separate 34-file E&M profile; desktop/profile checks, physical CE verification pending | [TI Connect CE for Windows/Mac](https://education.ti.com/en/products/computer-software/ti-connect-ce-sw) |
| **TI-84 Plus CE-T Python edition** | Use the CE Python profile as an unverified regional target; TI supports Python transfer on this family, but this project has no CE-T hardware test | TI Connect CE; verify Python and drawing modules on the device |
| TI-84 Plus CE / CE-T **without Python** | Cannot run these Python programs | No compatible download in this collection; a separate TI-BASIC port would be needed |
| TI-84 Plus / Plus T | Cannot run these Python programs | TI Connect CE can transfer supported native files, but it does not make these Python files executable |
| TI-84 Plus Silver Edition | Cannot run these Python programs | Same limitation; no TI-BASIC build is included |
| TI-84 Plus C Silver Edition | Cannot run these Python programs | Same limitation; color screen does not imply Python support |
| Pocket / Pocket SE and other TI-84-branded regional variants without Python | Cannot run these Python programs | Identify the exact model; no compatible Python profile is claimed |

Installing transfer software or renaming `.py` to `.8xp` does not add a Python interpreter to older hardware. No native TI-BASIC programs were found in the reviewed project. Model support and transfer behavior are based on TI's [connectivity guide](https://education.ti.com/html/eguides/graphing/84plusce/en/content/eg_84tic/m_introtic-ce/tc_intrototiconnect.HTML), [legacy model support](https://education.ti.com/en/customer-support/knowledge-base/ti-83-84-plus-family/product-usage/37036), and [Evo guide](https://education.ti.com/en/product-resources/eguides/eguide-84-evo/evo-connect-user-guide).

## 1. Download to your computer

1. From the repository README, click the ZIP for your calculator and course topic.
2. On GitHub's ZIP file page, click **Download raw file** / the download icon. For everything, choose **Code → Download ZIP** on the repository home page.
3. Extract the ZIP. On Windows use **Extract All**; on Mac double-click the ZIP.
4. Open the correct folder below. Do not transfer the ZIP itself.

| Bundle | Select these files | Count | Launch |
|---|---|---:|---|
| `Exam2_Evo.zip` | `Exam2_Evo/TRANSFER/*.py` | 40 | `EXAM2` |
| `Share_AP_Physics_C_EM.zip` for Evo | `Share_AP_Physics_C_EM/TI84_EVO/TRANSFER/*.py` | 34 | `EFIELD` / `APC` |
| Same sharing ZIP for CE Python | `Share_AP_Physics_C_EM/TI84_PLUS_CE_PYTHON/TRANSFER/*.py` | 34 | `EFIELD` / `APC` |
| `AP_Physics_C_Evo_Fixed.zip` | `AP_Physics_C_Evo_Fixed/TRANSFER_FIRST/*.py` | 22 | `APC` |

The ZIP may open directly into the listed top-level folder depending on your extraction tool. Keep all original filenames and capitalization. Select all files from **one** transfer folder in one batch. Developer folders are for computer use.

## 2A. TI-84 Evo / Evo-T

1. Use a computer, a USB **data** cable that fits the calculator, and a WebUSB-capable browser accepted by [TI Connect Evo](https://connectevo.ti.com/). A charging-only cable cannot transfer files.
2. Power on the calculator, connect it, open the site, and choose **CONNECT TO CALCULATOR**. Select the intended calculator and grant the connection.
3. Choose **SEND FILES → SEND TO CALCULATOR**. Select every `.py` file in the chosen complete transfer folder. Send once; keep the tab connected until the transfer finishes.
4. Keep names unchanged. For an update, back up your edits and allow replacement of matching names. Use RAM where offered.
5. Open Python on the calculator and restart/reinitialize its shell to clear old imports. Continue with the first-run check below.

Follow TI's [sending files guide](https://education.ti.com/en/product-resources/eguides/eguide-84-evo/evo-connect-user-guide) for browser/device requirements. Use Connect Evo for this calculator. TI Connect CE did not detect the Evo during the original project work.

## 2B. TI-84 Plus CE Python / CE-T Python

1. Confirm **Python edition**, with a working Python app. Obtain [TI Connect CE](https://education.ti.com/en/products/computer-software/ti-connect-ce-sw) from TI on a supported Windows or Mac computer. Check TI's current system requirements.
2. Connect the powered-on calculator with a USB data cable. In TI Connect CE, open **Calculator Explorer** and select the calculator.
3. Select all **34 `.py` files from `TI84_PLUS_CE_PYTHON/TRANSFER`**, then drag them into Calculator Explorer or use **Actions → Send to Calculators**.
4. Keep names unchanged; choose **RAM**. Back up your edits before allowing replacement of matching names. Send the group and wait for completion.
5. Open Python and reinitialize the shell, then run the checks below.

TI Connect CE converts `.py` files into Python AppVars during transfer. The Python app runs them from RAM. You do not need to create `.8xv` files yourself; use Calculator Explorer, not the TI-BASIC Program Editor. See TI's [Python transfer instructions](https://education.ti.com/html/eguides/connectivity/TI-Connect-CE/EN/Content/EG_84_TIConnect/M_UsePython/M_UsePython.HTML). CE hardware testing remains pending.

The browser-based Evo instructions are not a CE installation route. For a Chromebook or an unsupported computer OS, check TI's current connectivity options; this collection does not claim a verified CE Python transfer workflow there.

## 3. First run

**Exam 2 Evo:** run `EXAM2`, choose **Exam 2 self-check**, and look for a PASS message. Restart Python, then reopen `EXAM2`. Try a uniform solid sphere with Q=2e-9 C, R=1 m, r=0.5 m: E ≈ 8.99 N/C. The full transfer already includes the banner fix; no patch is needed for a fresh installation.

**E&M sharing profiles:** run `EFCHK`; expect `EFIELD CHECK START v2` and `PASS: 12 physics + 2 UI`. Restart Python. Run `EFKEY`, press/release each requested navigation key, and complete the DOWN → ENTER selection test. Expect `PASS: hardware navigation`. Calibration lasts for that Python session. Launch `EFIELD` for field models or `APC` for the E&M toolkit.

**Full-course corrected Evo:** run `APCHECK`; expect `APCHECK START v3`, `SELF CHECK PASS`, and `8 numeric checks passed.` Restart Python and run `APC`. Choose Mechanics → Forces/dynamics → Newton second law → Solve → F; m=2 and a=3 should give F=6 N.

The full-course install has optional tools. Transfer `OPTIONAL_TOOLS/APTOOLS.py` plus `APMECH.py`, `APEM.py`, or `APLAB.py` for the groups you need. All four optional files can be sent together if space allows. On an old compressed install, remove only that toolkit's obsolete `APLOAD`, `APNOTES`, and old `APTOOLS` after backing up edits; then install the optional replacement if desired. Do not remove unrelated programs.

## Updating an existing installation

Prefer the matching complete profile and restart Python afterward. Exam 2's `UPDATE` folder is only for an existing compatible E-Field Studio Evo install; send all **eight** files, including `EFGUI.py`. Do not send both `TRANSFER` and `UPDATE`. Historical patch dependencies are documented in [Versions](VERSIONS.md).

## Everyday controls

Graphic E-Field / Exam 2 menus: ↑/↓ selects, ENTER opens, ←/→ changes pages, CLEAR/0 goes back. Number keys select a displayed row. Guide cards use ENTER/RIGHT to advance and LEFT to go back. The corrected full-course text menus use 1–5 and ENTER, 0 back, 8 previous page, 9 next page.

At number prompts use SI units; `q` then ENTER cancels. Scientific notation and expressions such as `2e-9`, `pi/4`, and `sqrt(2)` work. Trig expression inputs are radians; arc and some Exam 2 angle prompts explicitly request degrees. Follow the prompt. For rods, L is **full length**; ring R is radius; axial-rod x is measured from the **near end**.
