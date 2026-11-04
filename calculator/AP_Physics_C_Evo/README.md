# AP Physics C toolkit for TI-84 Evo

Start with **APC_INSTALL**. It contains **21 Python files**, totaling about **48 KB**. Run **APC** to open the toolkit; **APCHECK** runs the transfer self-check. The readable, editable originals are in **APC_EVO**.

The toolkit covers the seven Mechanics units and six Electricity & Magnetism units with **160 equations**, one-unknown solvers, **15 multi-step tools**, numerical calculus, lab calculations, concept references, and graphing. It helps evaluate a model you select; it cannot automatically interpret every word problem or supply symbolic derivations.

## Install on the Evo

1. Unzip **AP_Physics_C_Evo.zip** on your computer.
2. Open [TI Connect Evo](https://connectevo.ti.com/) in a supported Chrome browser and connect your powered-on Evo with its USB-C data cable.
3. Use the file-transfer control to send **every `.py` file inside `APC_INSTALL`**. Keep their names and capitalization. These are Python files; do not convert them into TI-BASIC `.8xp` files. Do not transfer a second copy from `APC_EVO`.
4. Open the calculator's Python app and run **APCHECK**. It should report **SELF CHECK PASS** after 24 numerical checks.
5. Run **APC**. Try Mechanics → Forces/dynamics → Newton second law → Solve an unknown → F. Enter `m=2`, `a=3`; the result should be **6 N**. Try the next/previous menu pages and a projectile or SHM graph.

TI's current [Evo guide confirms Python support](https://education.ti.com/en/product-resources/eguides/eguide-84-evo/python), and [TI Connect Evo supports transferring Python programs](https://education.ti.com/en/products/calculators/graphing-calculators/ti-84-evo/ti-connect-evo). On-device execution, memory use, and screen/key behavior have **not** been verified on a physical Evo. Desktop checks are described in `VALIDATION.md`; the on-device self-check is included to make the remaining check straightforward.

## Navigate quickly

Each menu has at most five choices per page:

| Input | Action |
|---|---|
| `1`–`5`, then Enter | Select the displayed item |
| `9` | Next page, wrapping to the first |
| `8` | Previous page, wrapping to the last |
| `0` | Back; at the main menu, exit |
| `q` or `b` at a numerical prompt | Cancel the current calculation |
| Enter at a prompt with a displayed previous value | Reuse that value |
| `ans` in an expression | Reuse the last displayed numerical result |

The main menu's second page contains the lab/reasoning guide, constants, recent answers and help. Recent answers retain the last eight calculations for the session. A formula remembers its known inputs while its unknown-selection screen remains open. Changing default `g` under Constants lasts for the current session.

For an equation, choose **Solve an unknown**, **Graph this relation**, or **Equation / variables**. References show the variable definitions, units and model assumptions. Multiple real roots are displayed when appropriate; choose the physical branch yourself.

## Inputs and units

Use **SI units**. Angles are **always radians**, independent of the calculator's degree/radian setting.

Examples: `2.5e-6`, `pi/4`, `sqrt(2)`, `3*10^8`, `ke*qe`, `30*pi/180`. Powers can use `^` or `**`. Write multiplication explicitly: `2*x`, not `2x`. Available functions are `sqrt`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `exp`, `ln`/`log` (natural logarithm), and `abs`.

Named constants: `pi`, `e`, `g`, `G`, `ke`, `eps0`, `mu0`, `qe` (positive elementary charge magnitude), `me`, `mp`, `c0`. Enter electron charge as `-qe`. Default `g` is **9.8 m/s²**.

Convert before entry: cm × `0.01`; mm × `0.001`; micro × `1e-6`; nano × `1e-9`; kilo × `1000`. Capacitance is in **farads**, charge in **coulombs**, inertia in **kg·m²**, angular velocity in **rad/s**, and resistance in **ohms**. The program displays seven significant digits and does not infer measurement uncertainty or significant figures.

## Included tools

The formula inventory is in `FORMULAS.md`; curriculum coverage is in `COVERAGE.md`.

Multi-step solvers include 3D vector products, unequal-height projectile flight, collisions with restitution, center of mass and total momentum, Atwood machines with pulley inertia, SHM initial conditions, point-charge superposition, inside/outside charged spheres, equivalent resistor/capacitor groups, multi-battery DC circuits, RC and RL step responses, rolling inclines, linear regression, and motional emf/drag.

Math/lab tools include numerical derivatives, definite integrals, bracketed roots, function evaluation, stable quadratic roots, simultaneous linear equations, a first-order ODE integrator, and percent comparisons. To integrate a continuous charge or mass distribution, first derive the relevant scalar/component integrand, then enter it as `f(x)` with numerical parameters.

The DC circuit solver supports ground plus up to **six other nodes**, **12 resistors**, and **four ideal voltage sources**, including sources between non-ground nodes. It returns node voltages and branch currents. It handles resistor/ideal-cell DC networks; use RC/RL tools for their supported transient models. It rejects singular or badly conditioned systems. For general equilibrium or manually assembled Kirchhoff equations, use the linear-system solver.

Graphs include custom `f(x)`/`g(x)`, formula-variable sweeps, projectile paths, position/velocity/acceleration, SHM, RC/RL responses and radial electrostatic fields/potentials. They use TI's `ti_plotlib`, with colored curves, axes, grids and labels. Clear dismisses a TI plot. Desktop Python shows a small sample table when `ti_plotlib` is unavailable. Graphs do not write into the calculator's native function editor or provide native interactive tracing.

## Practical limits

- A formula's stated assumptions matter. For example, constant-acceleration equations require constant acceleration, small-angle pendulum formulas require small angles, and Gauss/Ampère shortcuts require symmetry. Several geometry constraints are checked automatically; references remain necessary.
- Most unknowns have direct algebraic solutions. Non-algebraic or periodic targets request a **continuous sign-changing bracket**, giving one root per bracket. Avoid singularities. A tangent root may not change sign. Angles and oscillation times can have multiple branches.
- Numerical derivatives, integrals and ODE results are estimates. Refinement changes are shown; these are not certified error bounds. Split discontinuities and compare step sizes.
- Graphs sample 80 points by default. Narrow peaks, fast oscillations and unsampled poles may be missed. Shrink the interval when needed. A formula branch may cease to exist within the plotted interval.
- For an isolated LC circuit, the formula tools cover period, angular frequency, peak current and charge versus time; derivative/evaluation tools can calculate other states. Arbitrary coupled ODE systems and symbolic multivariable integration are outside this toolkit.
- A numerical answer does not replace the AP exam's diagrams, derivations, explanations or experimental design. Follow your instructor's and exam administrator's rules for stored programs.

## Files and development

`APC_INSTALL` is losslessly packed Python source to reduce calculator storage. `APLOAD` reconstructs each module and executes that source using Python's built-in `exec`; it has no network or filesystem access. Polynomial coefficients replace redundant inverse-expression strings in the packed catalogs. Every packed module was checked for exact reconstruction and tested using the same physics/UI tests as the readable originals. Use `APC_EVO` for editing, then rebuild the install files; do not edit the encoded strings.

On a computer, run `python3 APC_EVO/APC.py`. Only catalog regeneration uses SymPy; calculator runtime and packing require no third-party libraries. Developer checks are in `dev`. Keep readable source and packed install files in separate folders.

If transfer succeeds but an import fails, confirm all 21 install files arrived with their original names and reopen the Python app. If memory is insufficient, check the calculator's available memory and your installed Python programs; this release does not delete or change them automatically. Preserve existing work before making memory changes. `APCHECK` verifies numerical behavior, while a manual graph check verifies plotting separately.
