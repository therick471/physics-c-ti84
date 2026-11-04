> Superseded: the original packed edition has a TI import-startup bug and excessive decoding allocations. Use the corrected plain-Python release and VALIDATION_LITE.md.

# Validation

Verified on desktop Python on October 7, 2026. The readable sources and packed install edition each pass **22 test groups**.

- All **160 formula entries** were exercised through consistent generated states. **525 explicit inverse targets** round-tripped through the calculator arithmetic parser and were compared to independent symbolic evaluation. **41 numerical targets** recovered a known state with a local sign-changing bracket.
- Independent numerical fixtures cover unequal-height projectiles, collision momentum/energy, pulley tensions, SHM initial conditions and energy, RC/RL initial and long-time limits, signed electrostatic superposition, sphere fields/potentials, equivalent components, regression, and multiple-battery circuits.
- Circuit tests include batteries referenced to ground and a floating voltage source between two nodes; currents, node voltages and power balance were checked. Singular networks and linear systems are rejected.
- Numerical checks cover operator precedence and scientific notation, invalid/complex inputs, stable quadratic roots, the zero-acceleration time case, two displacement-zero roots, geometry restrictions, very small bracketed roots, signed integrals and derivatives.
- UI tests cover page wrapping, back navigation, default-value reuse, prompt cancellation, and a main-menu → unit → back flow. Plot API tests verify TI plotting method order, sampled data sizes and graph bounds with a mock module. These are API checks, not a physical rendering test.
- Every install module reconstructs its intended source exactly before execution. Catalog packing removes redundant inverse-expression strings for polynomial targets while preserving solver behavior. Names are at most eight characters, sources use ASCII, literal lists/tuples contain at most 100 elements, and graphs use at most 80 samples per segment.

`dev/source-test-results.txt` and `dev/packed-test-results.txt` contain the actual test results. Calculator runtime uses only Python's built-ins, `math`, `ti_system` for clearing text and `ti_plotlib` for graphs. Build-time algebra generation uses SymPy; it is not needed on the calculator.

## Remaining physical-calculator verification

A physical TI-84 Evo was not available. File transfer, import behavior, actual runtime memory, loading speed, screen layout and key handling are **not confirmed on hardware**. TI's [Evo Python page](https://education.ti.com/en/product-resources/eguides/eguide-84-evo/python) links the Python guide used to check the supported language and plotting APIs. Its linked reference guide includes CE-era limits; the release is compact, but that does not establish the exact capacity of every Evo OS version.

The install edition contains 21 files and about 48 KB of source. Runtime memory use differs from source storage, especially during decoding/importing. Do not treat the file-size check as proof that every memory state on a calculator can run it.

After transferring, run **APCHECK** for 24 quick numerical checks. Then run **APC**, solve Newton's `F=m*a`, navigate both menu pages, and plot a projectile or SHM curve. Clear should return from a TI graph. These steps complete the display/input checks that desktop tests cannot establish.

Numerical root recovery uses a valid local bracket; it does not demonstrate global root finding. Integrals, derivatives, ODE solutions and graphs are numerical estimates subject to the stated limitations. The program shows assumptions and refinement differences instead of claiming certified numerical error or universal problem coverage.
