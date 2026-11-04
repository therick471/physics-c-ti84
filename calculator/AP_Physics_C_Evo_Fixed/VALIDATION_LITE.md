# Corrected-release validation

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
