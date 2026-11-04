# Coverage and solver routes

This toolkit spans the unit structure in the current [AP Physics C: Mechanics course](https://apcentral.collegeboard.org/courses/ap-physics-c-mechanics) and [AP Physics C: Electricity & Magnetism course](https://apcentral.collegeboard.org/courses/ap-physics-c-electricity-and-magnetism). Coverage includes calculation tools and concise conceptual references; it is not a substitute for a full course or a claim to solve every possible exam problem automatically.

| Unit | Topics represented | Calculator route |
|---|---|---|
| 1. Kinematics | Scalars/vectors, displacement, velocity, acceleration, motion graphs, reference frames, multidimensional motion | Unit 1 equations; vector and projectile tools; derivatives, integrals and motion plots |
| 2. Force and translational dynamics | Systems/COM, free-body diagrams, Newton's laws, gravitation, static/kinetic friction, springs, resistive forces, circular motion | Unit 2 equations/notes; COM and Atwood tools; linear systems for force balance; ODE for velocity-dependent forces |
| 3. Work, energy and power | Translational kinetic energy, work, conservative/nonconservative forces, potential energy, energy balance, power | Unit 3 equations; force-position integrals; potential derivatives; equilibrium/stability notes |
| 4. Linear momentum | Momentum, impulse, conservation, elastic/inelastic collisions and explosions | Unit 4 equations; restitution collision tool; total momentum/COM; force-time integrals |
| 5. Torque and rotational dynamics | Angular kinematics, linear/angular relations, torque, inertia, rotational equilibrium and dynamics | Unit 5 equations and standard-shape inertias; cross products; inertia integrals; linear systems; pulley tool |
| 6. Rotating-system energy and momentum | Rotational energy, torque/work, angular momentum/impulse, conservation, rolling, orbiting satellites | Unit 6 equations; rolling tool; torque integrals; orbital equations also in Units 2 and 3 |
| 7. Oscillations | SHM definitions, frequency/period, graphs and phase, energy, simple/physical pendulums | Unit 7 equations; initial-state SHM solver; SHM plots; small-angle and equilibrium references |
| 8. Electric charges, fields and Gauss's law | Charge/force, charge conservation and charging, electric fields, continuous distributions, flux, Gauss's law | Unit 8 equations; 2D charge superposition; sphere tool; derived-component integrals; charging/symmetry notes |
| 9. Electric potential | Potential energy, potential, electric energy conservation, field-potential relation | Unit 9 equations; superposition/sphere tool; rod and ring formulas; integrals and derivatives |
| 10. Conductors and capacitors | Electrostatic conductors, charge redistribution, capacitors, dielectrics | Unit 10 equations; charge-sharing solvers; equivalent-C tool; conductor and battery/isolated dielectric notes |
| 11. Electric circuits | Current, simple/compound DC circuits, resistance/resistivity, Ohm's law, power, KVL, KCL, RC circuits | Unit 11 equations; resistor reductions; multi-source circuit solver; RC state solver and graph |
| 12. Magnetic fields and electromagnetism | Magnetic fields/materials, moving charges, current-generated fields, Biot-Savart and Ampère's law | Unit 12 equations; vector cross products; orbit/selector/loop/arc/wire/solenoid/toroid formulas; integral/symmetry notes |
| 13. Electromagnetic induction | Magnetic flux, induction, induced current/force, inductance, RL circuits and LC circuits | Unit 13 equations; motional rod tool; RL state solver/graph; LC formulas; derivatives for changing flux/current |

Science practices appear in the concept references and Lab / reasoning guide: constructing and interpreting graphs, identifying a system and model, explaining signs/limits, linearizing experimental data, fitting lines, comparing values, designing controlled experiments, and distinguishing random and systematic uncertainty. The program does not generate a correct diagram, choose a physical system, or justify a claim for you.

The formula catalog contains 160 equations. Each variable can be selected as the unknown; 525 targets use explicit algebra/polynomial solving and 41 use a user-supplied numerical bracket. This includes inverse uses, rather than only evaluating a fixed output. `FORMULAS.md` lists the individual equations and which targets require brackets.

For continuous mass/charge distributions, variable forces, time-dependent currents or flux, use the general calculus tools after deriving the integrand. The numerical integrator is one-dimensional. Arbitrary 3D fields, simultaneous nonlinear systems and symbolic proofs are outside the program. Use the calculator's built-in facilities or hand analysis when a problem needs methods beyond the listed models.
