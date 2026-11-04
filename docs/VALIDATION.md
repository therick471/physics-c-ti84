# Validation

The repository assembly passed **87 desktop tests**: 29 full-course/Lite, 33 field-studio, 12 sharing-profile, 11 Exam 2, and 2 banner-layout tests. Package integrity and documentation-link checks also passed. Current logs are in `checks/`. Run from the repository root on a computer with Python and SymPy:

```sh
python -m pip install -r requirements-dev.txt
python tools/run_checks.py
```

The suites cover the corrected full-course release (including all formula targets), independent field-model integration and limits, two sharing profiles and their TI API behavior, Exam 2 physics/menu routes, and the banner-safe layout. Each suite runs separately so identically named calculator modules do not leak between release tests. The package check verifies preserved-source hashes, ZIP integrity, file counts, import completeness, ASCII program syntax/names, current Exam 2 ZIP/source equality and documentation links.

GitHub Actions runs the same checks on pushes and pull requests. Test logs stored under older source snapshots describe historical states and can include failures; consult `checks/` for this repository assembly.

## What hardware evidence supports

- In the October 30 chat, the user confirmed that Evo keys worked after the keyboard repair. The chat also records screen-capture verification of highlight alignment and installation of final formulas. This is targeted historical evidence, not a fresh full device test.
- The November 2 CE Python profile was checked against documented CE key/drawing conventions and simulated TI APIs. No physical CE test was recorded.
- The November 3 Exam 2 rebuild and banner fix have desktop tests. Their transfer, physical display and runtime-memory behavior still require an on-device check.
- The full-course plain-source edition fixes observed startup/string-method problems; current desktop tests do not prove every physical Evo memory state can run it.

Run the checks and worked examples in [Install](INSTALL.md) after transferring. Inspect navigation, text, and one graph on the actual calculator. Source file size is a storage measurement, not runtime-heap usage. Numerical integration, extrema sampling, graphing and bracketed roots have the model and numerical limitations documented in the original guides.
