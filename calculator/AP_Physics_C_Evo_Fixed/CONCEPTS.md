# AP Physics C concept reference

These notes stay on your computer to reduce calculator memory use. Formula assumptions and variable definitions still appear on the calculator.

## Unit 1

### Vectors / scalars

Scalars have magnitude; vectors have magnitude and direction. Add vector components, not magnitudes. A dot B=Ax*Bx+Ay*By+Az*Bz. Cross products give a vector perpendicular to both; use the right hand rule. Components: vx=v*cos(th), vy=v*sin(th).

### Motion / graphs

v=dx/dt, a=dv/dt. Slope of x(t) gives v; slope of v(t) gives a. Signed area under v(t) gives displacement; area under speed gives distance. Area under a(t) gives change in v. Use Math derivative/integral for arbitrary functions. Constant-a equations cannot be used for variable a.

### Projectile / frames

No air: ax=0 and ay=-g when up is positive. Solve vertical motion for time, then horizontal motion. A higher landing platform may be reached twice; the projectile tool returns the later crossing. Relative velocity: v(A/B)=v(A/ground)-v(B/ground). Inertial frames have zero frame acceleration.

## Unit 2

### Systems / center of mass

Choose a system boundary before classifying internal and external forces. rCOM=sum(m*r)/M; for continuous material use integral(r dm)/M with dm=lambda dx, sigma dA, or rho d(volume). M*aCOM=Fexternal. Use the COM multi-step tool; for continua derive integrands and use Math integrals.

### Forces / free bodies

Choose the system and axes. Draw only forces ON that system. sum(Fx)=m*ax and sum(Fy)=m*ay. Normal force is not always mg. An ideal massless rope over a massless frictionless pulley has equal tension. Newton third-law forces act on different objects and do not cancel on one free-body diagram.

### Friction / springs

Kinetic friction magnitude=mu_k*N and opposes relative slipping. Static friction adjusts from 0 to mu_s*N; do not set it to the maximum unless slipping is imminent. Hooke force=-ks*x about equilibrium. For an incline resolve gravity parallel and perpendicular to the slope.

### Gravity / orbits

F=G*M*m/r^2 points toward source; r is center-to-center. g=G*M/r^2. Circular orbit: net radial force supplies m*v^2/r. Escape and orbital energy need gravitational potential -G*M*m/r. Newton shell theorem: external spherical source acts like a central point; inside a thin shell, gravitational field=0.

### Circular / drag

Radial acceleration=v^2/r inward; tangential acceleration=d(speed)/dt. Centripetal is the NET radial force, not a new force. At the top of a vertical circle, identify which forces point inward. Linear drag=-b*v; m*dv/dt=forces. Terminal velocity occurs when net force=0. Use ODE for other drag laws.

## Unit 3

### Work / potential

W=integral(F dot dr). Constant force: W=F*d*cos(th). Net work=delta K. Conservative force along x: F=-dU/dx; delta U=-work by conservative force. Work is path independent only for conservative forces. Include external work when mechanical energy is not conserved.

### Energy / stability

Kf+Uf=Ki+Ui+W_external_or_nonconservative. Spring U=ks*x^2/2; near Earth U=m*g*h; gravity U=-G*M*m/r with zero at infinity. Stable equilibrium: minimum U; unstable: maximum U. Allowed motion requires E-U>=0; turning points have K=0.

### Power / graphs

Power=dW/dt=F dot v. Average power=W/time. The area under F(x) is work; slope of U(x) is negative force. A linear spring F(x) gives triangular area, not final force times displacement.

## Unit 4

### Impulse / momentum

p=m*v; J=integral(F dt)=delta p. Area under NET force-time graph gives impulse. Momentum is conserved when net external impulse is negligible. Choose a system enclosing all colliding objects; track signs in each dimension.

### Collisions / explosions

Elastic: momentum and kinetic energy conserved. Perfectly inelastic: objects stick; momentum conserved but K generally decreases. Explosion: momentum may remain conserved while stored internal energy becomes K. The collision tool uses restitution e: 0 stick, 1 elastic.

### Center of mass

rCOM=sum(m*r)/sum(m), or integral(r dm)/M for a continuum. vCOM=Ptotal/M. M*aCOM=Fexternal. Internal forces cannot change total momentum. Use COM tool for discrete masses or Math integrals for rods with nonuniform density.

## Unit 5

### Rotational kinematics

w=dtheta/dt; alpha=dw/dt. Constant-alpha equations match constant-a equations by x->theta, v->w, a->alpha. Angles in radians. Tangential speed=r*w; tangential acceleration=r*alpha; radial acceleration=r*w^2. Different points share w but not tangential speed.

### Torque / equilibrium

torque=r cross F; magnitude=r*F*sin(th). Lever arm is perpendicular distance from axis to force line. Rigid-body equilibrium requires BOTH net force=0 and net torque=0. Choose a pivot to eliminate unknown forces. Use Linear system tool to solve equilibrium equations.

### Inertia / density

I=sum(m*r_perp^2)=integral(r_perp^2 dm). For a rod dm=lambda(x) dx; for a disk ring dm=sigma*2*pi*r dr. Parallel axis: I=I_COM+M*d^2, only if the reference axis passes through COM and axes are parallel. Rotation obeys net torque=I*alpha for a fixed axis.

### Pulleys / massive axes

A massive pulley can have unequal tensions: (T2-T1)*r=I*alpha. No slip implies a=r*alpha. Use the Atwood tool for two hanging masses. Frictionless axle does not imply zero inertia.

## Unit 6

### Orbiting satellites

For circular orbits use Unit 2 Orbital speed and Orbit period, and Unit 3 Circular orbit energy. Gravity is a central force: torque about the source center is zero, so orbital angular momentum is conserved. For circular motion L=m*r*v. Use Particle angular mom for general position/velocity angle.

### Rotation energy / work

Krot=I*w^2/2. Work=integral(torque dtheta); power=torque*w. Energy can transfer between translation and rotation. For rigid-body rolling: K=M*vCOM^2/2+I_COM*w^2/2.

### Angular momentum

Particle L=r cross p; rigid body fixed-axis component L=I*w. Net external torque=dL/dt; angular impulse=integral(torque dt). Conserve L about the chosen origin when external torque about THAT origin is zero. Changing inertia changes angular speed even though L stays fixed.

### Rolling / collisions

No-slip rolling: vCOM=r*w and aCOM=r*alpha. Static friction may provide torque without dissipating energy on a stationary surface. Larger I/(M*r^2) gives smaller downhill acceleration. For an impact, angular momentum may be conserved about a pivot even when linear momentum is not.

## Unit 7

### SHM definitions

SHM restoring force=-ks*x leads to a=-w^2*x. x=A*cos(w*t+phase), v=-A*w*sin(w*t+phase). x is measured from EQUILIBRIUM, which can differ from unstretched spring position. Period does not depend on amplitude for ideal linear SHM.

### Energy / phase

E=ks*A^2/2=K+U. At equilibrium speed is maximal; at turning points speed=0. A=sqrt(x0^2+(v0/w)^2). phase=atan2(-v0/w,x0). The SHM tool calculates state from x0,v0 and t.

### Pendulums

Simple pendulum T=2*pi*sqrt(l/g), small angle only. Physical pendulum T=2*pi*sqrt(Ipivot/(M*g*d)), d pivot-to-COM. Torsion pendulum T=2*pi*sqrt(I/kap). Damping lowers amplitude; a driven system can resonate. Use ODE for nonideal models.

## Unit 8

### Charge / charging

Charge is conserved and quantized: Q=N*qe. Electrons carry -qe. Conduction transfers charge by contact; induction redistributes charge without contact. Grounding allows exchange with Earth. Polarization separates charge locally without changing net charge. Like signs repel, unlike attract.

### Electric fields

E=F/q_test, independent of the test charge in the ideal model. Positive test force follows E; negative reverses. Fields add as VECTORS. Field lines leave positive charge and enter negative; closer lines indicate larger magnitude. Zero E does not imply zero potential.

### Continuous charge

dq=lambda dx, sigma dA, or rho d(volume). dE=ke*dq*r_vector/r^3. Integrate components using symmetry; transverse components may cancel. Ring axis field and disk axis field are in Unit 8 solvers. For other shapes use Math integrals with the derived component integrand.

### Flux / Gauss

Flux=integral(E dot dA); outward normal on a CLOSED surface. Closed flux=Qenclosed/eps0. External charges can affect E but contribute zero net closed flux. To solve E via Gauss, symmetry must make E constant on useful surface portions: spheres, infinite lines/cylinders, infinite planes. E=0 inside conductor material at electrostatic equilibrium.

## Unit 9

### Potential / work

V is scalar; V=sum(ke*q/r) with chosen zero. Pair U=ke*q1*q2/r; total U sums DISTINCT pairs once. delta U=q*delta V; work by field=-q*delta V. Electric force conserves K+U when other forces do no work. Negative charge accelerates toward higher V.

### Field from potential

delta V=-integral(E dot dl). Ex=-dV/dx. Equipotentials are perpendicular to E; no electric work along an equipotential. A steep V(x) slope means large E. Potential is continuous across an ordinary charged surface, while normal field may jump.

### Distributions / energy

For continuous charge, dV=ke*dq/r; integrate a SCALAR. Infinite line needs a reference radius, not infinity. Uniform solid sphere and conducting sphere differ inside. Use Sphere tool to handle both pieces without using an outside formula inside.

## Unit 10

### Conductors / sharing

Electrostatic equilibrium: E=0 in conductor material, V constant, excess charge on surfaces, external E normal to surface. A charge in a cavity induces opposite net charge on the inner wall; account for the conductor total charge on the outer wall. Connected conductors reach equal potential, not generally equal charge.

### Redistribution solver

For far-separated spheres connected by a wire: q1+q2=Qtotal, ke*q1/R1=ke*q2/R2. Thus q1=Qtotal*R1/(R1+R2). For connected capacitors: conserve total charge and use common final V=Qtotal/(C1+C2). Energy may be dissipated during sharing even though charge is conserved.

### Capacitor networks

C=Q/V. Parallel capacitors share V and capacitances add. Series capacitors share charge magnitude when initially uncharged; reciprocals add. U=Q^2/(2*C)=C*V^2/2=Q*V/2. Use Equivalent tool for groups and reuse ans in the next reduction.

### Dielectrics / batteries

Full-fill dielectric increases C by kd. Battery connected: V fixed, Q increases, stored U increases; battery supplies energy. Isolated capacitor: Q fixed, V and stored U decrease. Partial filling requires reducing series/parallel regions; eps=kd*eps0. A dielectric is pulled toward a stronger field.

## Unit 11

### Current / resistance

I=dQ/dt; conventional current follows positive charge flow, opposite electron drift. J=I/A and magnitude J=n*qe*vd. R=rho*l/A. Resistivity is a material property; resistance also depends on geometry. Ohm law V=I*R for an ohmic component. ammeter in series; voltmeter in parallel.

### Networks / Kirchhoff

Series resistors share current; parallel share voltage. KCL: sum currents in=sum currents out, charge conservation. KVL: sum voltage changes around loop=0, energy conservation. Crossing a cell negative to positive adds emf; moving with resistor current subtracts I*R. Negative solved current reverses assumed direction.

### Power / batteries

Resistor power=I^2*R=V^2/R. Source supplied power depends on sign of terminal current. A discharging battery terminal V=emf-I*r_internal. DC circuit tool solves resistor networks with sources between arbitrary nodes using KCL and source voltage constraints.

### RC / switching

Capacitor voltage cannot jump in the ideal finite-current model. Initially uncharged capacitor behaves like a short at t=0+, and as an open at long-time DC. tau=R_seen_by_C*C. Vc=Vfinal+(Vinitial-Vfinal)*exp(-t/tau). Charging current decays; find R seen by capacitor with ideal voltage sources replaced by wires.

## Unit 12

### Magnetism / materials

Magnetic field lines form closed loops; closed magnetic flux=0. No isolated magnetic monopoles. Compass moment tends to align with B. Ferromagnetic domains can stay aligned; paramagnets weakly align only in applied field; diamagnetic response opposes applied field. Vacuum formulas use mu0; a material may have different permeability.

### Moving charges

F=q*(v cross B). Use right hand for positive q and reverse for negative. Magnetic force does no work: perpendicular to velocity. With v perpendicular B, circular radius=m*speed/(abs(q)*B). Parallel component remains unchanged, producing a helix. Electric AND magnetic fields: F=q*(E+v cross B).

### Biot-Savart / wires

dB=mu0/(4*pi)*I*(dl cross rhat)/r^2. Field wraps around a straight current by the right hand rule. Integrate components for finite wires, loops or arcs; loop center and long wire formulas are in solvers. Loop moment=Nm*I*A*normal; torque=moment cross B; U=-moment dot B.

### Ampere law

Closed integral(B dot dl)=mu0*Ienclosed for steady currents. Symmetry gives B for a long wire, long solenoid or toroid. Inside a uniform-current solid cylinder B=mu0*I*r/(2*pi*R^2); outside B=mu0*I/(2*pi*r). Current enclosed must be the portion inside the chosen loop.

## Unit 13

### Flux / Faraday

FluxB=integral(B dot dA). emf=-Nm*d(flux_per_turn)/dt. Area normal matters, not angle to the surface plane. Flux can change via B, area or orientation. Lenz law: induced current opposes CHANGE in flux, not necessarily the field itself. Choose a normal, then use the right hand to define positive loop direction.

### Motional / induced force

For a perpendicular sliding rod, emf=B*l*v. More generally integrate (v cross B) dot dl. Induced current creates drag when mechanical energy is converted to resistor heating; mechanical power=I^2*R for the ideal rod setup. An induced electric field can circulate, so a single electrostatic potential cannot describe it globally.

### Inductance / RL

Self-emf=-L*dI/dt. Inductor U=L*I^2/2. Current cannot jump with finite ideal voltage. At t=0+ an initially current-free inductor behaves like an open; at long-time DC like a wire. RL tau=L/R. I=Ifinal+(Iinitial-Ifinal)*exp(-t/tau); decay can create a voltage of opposite sign.

### LC oscillations

Ideal LC: w=1/sqrt(L*C), q=Qmax*cos(w*t+phase), I=dq/dt. Energy alternates between Q^2/(2*C) and L*I^2/2; total constant. Maximum current=Qmax/sqrt(L*C). Resistance causes decay; ideal LC equations do not apply unchanged to a dissipative circuit.

## Labs and reasoning

### Design / uncertainty

Identify independent, dependent and controlled variables. Measure multiple trials, vary one input systematically, calibrate sensors and record units. State which quantities are measured directly. Distinguish random scatter from systematic offset. Error bars and uncertainty must reflect actual measurement resolution and procedure.

### Linearization / slopes

Derive the model before choosing axes. Example T^2=(4*pi^2/ks)*m: plot T^2 against m, then ks=4*pi^2/slope. For RC, ln(abs(V)) vs t has slope=-1/tau during discharge. The line-fit tool reports slope, intercept and R^2; R^2 alone does not prove the physical model.

### FRQ / checks

State a governing equation, define the system and signs, then substitute. Show units and the selected physical branch. Compare limiting cases: zero time, infinity, zero charge, no friction. A numerical answer alone does not replace derivations, diagrams, explanations or experimental design.

