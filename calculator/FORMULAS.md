# Formula inventory

160 equations across all 13 units. Every variable can be selected as an unknown. Numerical targets require a bracket; all angles use radians.

## 1 Kinematics

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Velocity update | `v=u+a*t` | None | Constant acceleration; signed 1D. |
| Displacement | `dx=u*t+a*t^2/2` | None | Constant acceleration; keep physical time branch. |
| Speed-distance | `v^2=u^2+2*a*dx` | None | Constant acceleration; both velocity signs may fit. |
| Average velocity | `dx=(u+v)*t/2` | None | Constant acceleration only. |
| Relative velocity | `vr=v1-v2` | None | Same axis; velocity of 1 as seen from 2. |
| Horizontal component | `v=u*cos(th)` | th | Angles radians. Angle solved by numeric bracket. |
| Vertical component | `v=u*sin(th)` | th | Angles radians. Angle solved by numeric bracket. |
| Projectile range | `R=v0^2*sin(2*th)/g` | th | Same launch/landing height; no air; g=9.8. |
| Projectile peak | `h=v0^2*sin(th)^2/(2*g)` | th | Height above launch; no air; rising launch. |

## 2 Forces / dynamics

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Newton second law | `F=m*a` | None | F is NET force along selected axis. |
| Kinetic friction | `F=mu*N` | None | Magnitude; direction opposes slipping. |
| Static friction limit | `F=mu*N` | None | MAXIMUM static friction, not actual friction. |
| Spring force | `F=-ks*x` | None | x measured from spring equilibrium. |
| Gravity force | `F=G*M*m/r^2` | None | Magnitude; point masses or external spheres. |
| Circular acceleration | `a=v^2/r` | None | Radial magnitude; inward direction. |
| Centripetal net force | `F=m*v^2/r` | None | NET radial force; not an additional force. |
| Incline gravity | `F=m*g*sin(th)` | th | Component downhill; g=9.8. |
| Incline normal | `N=m*g*cos(th)` | th | No other perpendicular forces; g=9.8. |
| Ideal banked turn | `v^2=r*g*tan(th)` | th | No friction; angle from horizontal. |
| Linear drag terminal | `v=m*g/b` | None | Downward terminal speed; drag=-b*v. |
| Fall with linear drag | `v=m*g/b*(1-exp(-b*t/m))` | m, b | Starts at rest; positive downward; g=9.8. |
| Orbital speed | `v^2=G*M/r` | None | Circular orbit; r from source center. |
| Orbit period | `T^2=4*pi^2*r^3/(G*M)` | None | Circular orbit; negligible orbiting mass. |

## 3 Work / energy / power

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Kinetic energy | `K=m*v^2/2` | None | K>=0; velocity sign cannot follow from K alone. |
| Constant-force work | `W=F*d*cos(th)` | th | th between force and displacement; radians. |
| Work-energy | `W=Kf-Ki` | None | W is total net work. |
| Height potential | `U=m*g*h` | None | Near Earth; chosen zero; g=9.8. |
| Spring energy | `U=ks*x^2/2` | None | x from unstretched length; energy>=0. |
| Gravity potential | `U=-G*M*m/r` | None | Zero at infinity; point/spherical source. |
| Energy balance | `Kf+Uf=Ki+Ui+W` | None | W is external/nonconservative work. |
| Average power | `P=W/t` | None | t>0; work over this interval. |
| Instant force power | `P=F*v*cos(th)` | th | th between vectors; radians. |
| Escape speed | `v^2=2*G*M/r` | None | Neglect drag; zero final speed at infinity. |
| Circular orbit energy | `E=-G*M*m/(2*r)` | None | Total K+U for circular orbit. |

## 4 Linear momentum

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Linear momentum | `p=m*v` | None | Signed 1D component. |
| Constant-force impulse | `J=F*t` | None | F constant or average NET force. |
| Impulse change | `J=m*(v-u)` | None | Constant mass; net external impulse. |
| Stick collision | `m1*v1+m2*v2=(m1+m2)*vf` | None | Perfectly inelastic; isolated 1D system. |
| Momentum balance | `m1*u+m2*v=m1*v1+m2*v2` | None | Signed 1D; negligible external impulse. |
| Center of mass 2 | `x=(m1*x0+m2*dx)/(m1+m2)` | None | x0 and dx are the two positions. |

## 5 Torque / rotation

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Angular velocity | `w=w0+alpha*t` | None | Constant angular acceleration. |
| Angular displacement | `dtheta=w0*t+alpha*t^2/2` | None | Constant angular acceleration; radians. |
| Angular speed-angle | `w^2=w0^2+2*alpha*dtheta` | None | Constant angular acceleration. |
| Arc length | `dx=r*dtheta` | None | Angles radians. |
| Tangential speed | `v=r*w` | None | Signed tangential component. |
| Tangential acceleration | `a=r*alpha` | None | Signed tangential acceleration. |
| Rotational dynamics | `tor=I*alpha` | None | NET torque about fixed axis. |
| Force torque | `tor=r*F*sin(th)` | th | th between r and F; radians. |
| Parallel axis | `I=I1+m*d^2` | None | I1 about parallel axis through COM. |
| Point mass inertia | `I=m*r^2` | None | r perpendicular distance to axis. |
| Disk cylinder inertia | `I=m*R^2/2` | None | Uniform solid disk/cylinder; symmetry axis. |
| Hoop inertia | `I=m*R^2` | None | Thin hoop; central symmetry axis. |
| Solid sphere inertia | `I=2*m*R^2/5` | None | Uniform solid sphere through center. |
| Shell sphere inertia | `I=2*m*R^2/3` | None | Thin spherical shell through center. |
| Rod center inertia | `I=m*l^2/12` | None | Uniform thin rod; perpendicular center axis. |
| Rod end inertia | `I=m*l^2/3` | None | Uniform thin rod; perpendicular end axis. |

## 6 Rotation energy / L

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Rotational energy | `K=I*w^2/2` | None | Fixed-axis rotation. |
| Angular momentum | `ang=I*w` | None | Fixed axis, rigid-body component. |
| Angular impulse | `ang=tor*t` | None | ang here means CHANGE in angular momentum. |
| Spin conservation | `I1*w0=I2*wf` | None | Zero net external torque. |
| Rotation work | `W=tor*dtheta` | None | Constant torque; radians. |
| Rotation power | `P=tor*w` | None | Same-axis components. |
| Rolling total energy | `K=m*v^2/2+I*v^2/(2*r^2)` | None | Rolling without slipping; I through COM. |
| Rolling incline accel | `a=g*sin(th)/(1+I/(m*r^2))` | th | Rolling without slipping; enough static friction. |
| Particle angular mom | `ang=m*v*r*sin(th)` | th | th between r and v; about chosen origin. |

## 7 Oscillations

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Spring period | `T=2*pi*sqrt(m/ks)` | None | Ideal mass-spring; no damping. |
| Pendulum period | `T=2*pi*sqrt(l/g)` | None | Small angle; point bob; g=9.8. |
| Physical pendulum | `T=2*pi*sqrt(I/(m*g*d))` | None | Small angle; d pivot-to-COM positive. |
| Torsion period | `T=2*pi*sqrt(I/kap)` | None | Linear restoring torque=-kap*angle. |
| Frequency period | `f=1/T` | None | Positive frequency and period. |
| Angular frequency | `w=2*pi*f` | None | w here is positive oscillation frequency. |
| Spring frequency | `w^2=ks/m` | None | Choose positive angular frequency. |
| SHM acceleration | `a=-w^2*x` | None | x from equilibrium; positive frequency. |
| SHM energy | `E=ks*amp^2/2` | None | Total mass-spring energy; amp>=0. |
| SHM speed-position | `v^2=w^2*(amp^2-x^2)` | None | abs(x)<=amp; choose sign from motion. |
| SHM position | `x=amp*cos(w*t+ph)` | w, t, ph | Undamped sinusoid; phase in radians. |

## 8 Charge / fields / Gauss

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Coulomb magnitude | `F=ke*abs(q1*q2)/r^2` | q1, q2 | Magnitude; use signs to decide attract/repel. |
| Point charge field | `Ef=ke*q/r^2` | None | Signed outward radial component. |
| Electric force | `F=q*Ef` | None | Same-axis signed components. |
| Uniform electric flux | `flux=Ef*A*cos(th)` | th | th between E and outward area normal. |
| Gauss law | `flux=q/eps0` | None | q is enclosed NET charge; closed surface. |
| Infinite line field | `Ef=lam/(2*pi*eps0*r)` | None | Signed radial; infinite uniform line. |
| Infinite sheet field | `Ef=sig/(2*eps0)` | None | Nonconducting infinite isolated sheet; one side. |
| Conductor surface | `Ef=sig/eps0` | None | Just outside electrostatic conductor; outward. |
| Uniform sphere inside | `Ef=ke*Q*r/R^3` | None | Only 0<r<=R; uniform volume charge. |
| Uniform cylinder inside | `Ef=rhoq*r/(2*eps0)` | None | Infinite uniform volume cylinder; r inside. |
| Ring axis field | `Ef=ke*Q*x/(x^2+R^2)^(3/2)` | x | Uniform ring; x along axis from center. |
| Disk axis field | `Ef=sig/(2*eps0)*(1-x/sqrt(x^2+R^2))` | x, R | Uniform disk; x>=0 on positive axis. |
| Charge quantization | `Q=nc*qe` | None | nc is signed integer count of elementary charges. |
| Uniform sphere charge | `Q=rhoq*4*pi*R^3/3` | None | Uniform volume charge density. |

## 9 Electric potential

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Point potential | `V=ke*q/r` | None | Zero potential at infinity. |
| Charge potential energy | `U=ke*q1*q2/r` | None | Signed pair energy; zero at infinity. |
| Potential energy change | `U=q*dV` | None | U here means CHANGE in potential energy. |
| Uniform field voltage | `dV=-Ef*d` | None | d along chosen field axis; uniform field. |
| Electric work | `W=-q*dV` | None | Work done by electric force. |
| Ring axis potential | `V=ke*Q/sqrt(x^2+R^2)` | None | Uniform ring; zero at infinity. |
| Sphere inside potential | `V=ke*Q*(3-r^2/R^2)/(2*R)` | R | Uniform solid sphere; r<=R; V infinity=0. |
| Shell inside potential | `V=ke*Q/R` | None | Thin charged sphere/conductor; inside. |
| Line potential diff | `dV=-lam*ln(R/r)/(2*pi*eps0)` | None | Infinite line; dV=V(R)-V(r). |
| Electric kinetic energy | `Kf-Ki=-q*dV` | None | Only electric force does work. |
| Rod axis field | `Ef=ke*lam*(1/x-1/(x+l))` | None | Uniform rod; target x>0 beyond near end. |
| Rod axis potential | `V=ke*lam*ln((x+l)/x)` | None | Uniform rod; target x>0 beyond near end. |

## 10 Conductors / capacitors

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Capacitance definition | `Q=C*V` | None | V across capacitor; signed plate charge. |
| Parallel plate C | `C=kd*eps0*A/d` | None | Full dielectric fill; d>0; neglect fringing. |
| Capacitor energy CV | `U=C*V^2/2` | None | Stored energy>=0. |
| Capacitor energy Q | `U=Q^2/(2*C)` | None | Stored energy>=0. |
| Capacitor energy QV | `U=Q*V/2` | None | Consistent signs for Q and V. |
| Capacitors parallel 2 | `C=C1+C2` | None | Same potential difference. |
| Capacitors series 2 | `1/C=1/C1+1/C2` | None | Same charge magnitude; ideal initially uncharged. |
| Electric energy density | `ue=kd*eps0*Ef^2/2` | None | Linear dielectric; kd=1 in vacuum. |
| Spherical conductor C | `C=4*pi*eps0*R` | None | Isolated sphere; potential relative infinity. |
| Spherical capacitor | `C=4*pi*eps0*r*R/(R-r)` | None | Concentric vacuum shells; 0<r<R. |
| Coaxial capacitor | `C=2*pi*eps0*l/ln(R/r)` | None | Vacuum cylinders; 0<r<R; ignore ends. |
| Capacitor charge sharing | `V=(C1*V0+C2*Vb)/(C1+C2)` | None | Parallel after disconnecting batteries; charge conserved. |
| Sphere charge sharing | `q=Q*r/(r+R)` | None | Far-separated conducting spheres joined by wire; Q total. |

## 11 Electric circuits

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Current charge | `Q=cur*t` | None | Constant or average current. |
| Ohm law | `V=cur*res` | None | Ohmic resistor; V is voltage drop. |
| Resistance geometry | `res=rhoe*l/A` | None | Uniform cross-section and resistivity. |
| Drift current | `cur=n*qe*A*vd` | None | Current magnitude; qe is elementary magnitude. |
| Current density | `cur=jcur*A` | None | Uniform current density normal to cross-section. |
| Resistors series 2 | `res=res1+res2` | None | Same current. |
| Resistors parallel 2 | `1/res=1/res1+1/res2` | None | Same voltage. |
| Electrical power IV | `P=cur*V` | None | Passive sign convention. |
| Electrical power IR | `P=cur^2*res` | None | Resistor dissipated power. |
| Electrical power VR | `P=V^2/res` | None | Resistor dissipated power. |
| Battery terminal V | `V=emf-cur*ri` | None | Discharging positive current; internal ri>0. |
| RC time constant | `tau=res*C` | None | Equivalent R seen by capacitor. |
| RC voltage charging | `V=Vb*(1-exp(-t/(res*C)))` | None | Initially uncharged; constant ideal source. |
| RC voltage discharge | `V=V0*exp(-t/(res*C))` | None | Source-free discharge; t>=0. |
| RC current charging | `cur=Vb/res*exp(-t/(res*C))` | res | Initially uncharged; resistor current. |

## 12 Magnetic fields

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Magnetic force qv | `F=q*v*B*sin(th)` | th | Signed scalar factor; direction via q(v cross B). |
| Wire magnetic force | `F=cur*l*B*sin(th)` | th | Uniform B; direction via L cross B. |
| Charged orbit radius | `r=m*v/(abs(q)*abs(B))` | q, B | Speed v>0; v perpendicular B; q,B nonzero. |
| Cyclotron period | `T=2*pi*m/(abs(q)*abs(B))` | q, B | Nonrelativistic; nonzero charge and field. |
| Long wire field | `B=mu0*cur/(2*pi*r)` | None | Infinite straight wire; sign via right hand rule. |
| Loop center field | `B=mu0*Nm*cur/(2*R)` | None | Nm identical circular loops; center. |
| Solenoid field | `B=mu0*nt*cur` | None | Long air-core solenoid, interior. |
| Toroid field | `B=mu0*Nm*cur/(2*pi*r)` | None | Ideal toroid inside windings. |
| Wire-wire force | `F=mu0*cur*cur0*l/(2*pi*r)` | None | Parallel long wires; same-direction attracts. |
| Magnetic moment | `mom=Nm*cur*A` | None | Planar loop; normal by right hand rule. |
| Loop torque | `tor=mom*B*sin(th)` | th | th between moment normal and B. |
| Dipole energy | `U=-mom*B*cos(th)` | th | th between magnetic moment and B. |
| Velocity selector | `v=Ef/B` | None | Magnitudes for crossed perpendicular E,B; undeflected beam. |
| Solid wire inside B | `B=mu0*cur*r/(2*pi*R^2)` | None | Uniform current density in long solid wire; r<=R. |
| Arc center field | `B=mu0*cur*th/(4*pi*r)` | None | Circular arc subtends th radians; radial leads contribute zero. |

## 13 Induction / RL / LC

| Solver | Equation | Numerical targets | Assumptions |
|---|---|---|---|
| Magnetic flux | `fluxB=B*A*cos(th)` | th | Uniform field; angle to area normal. |
| Faraday average emf | `emf=-Nm*dflux/t` | None | dflux per turn; fixed sign convention. |
| Motional emf | `emf=B*l*v` | None | Perpendicular rod, velocity and field. |
| Self-induced emf | `emf=-ind*cur/t` | None | cur here is CHANGE in current over t. |
| Inductor energy | `U=ind*cur^2/2` | None | Ideal inductor energy>=0. |
| Solenoid inductance | `ind=mu0*Nm^2*A/l` | None | Long air-core solenoid; ignore ends. |
| Magnetic energy density | `ub=B^2/(2*mu0)` | None | Vacuum. |
| RL time constant | `tau=ind/res` | None | Equivalent series resistance. |
| RL current rise | `cur=Vb/res*(1-exp(-res*t/ind))` | res | Initially zero current; constant source. |
| RL current decay | `cur=cur0*exp(-res*t/ind)` | None | Source-free series RL circuit. |
| LC period | `T=2*pi*sqrt(ind*C)` | None | Ideal LC; no resistance. |
| LC angular frequency | `w^2=1/(ind*C)` | None | Choose positive angular frequency. |
| LC peak current | `cur^2=Q0^2/(ind*C)` | None | Magnitude from total LC energy; choose positive peak. |
| LC charge vs time | `Q=Q0*cos(w*t+ph)` | w, t, ph | Ideal LC; phase radians; current is dQ/dt. |
| Rotating coil emf | `emf=Nm*B*A*w*sin(w*t+ph)` | w, t, ph | Uniform B; flux=Nm*B*A*cos(w*t+ph). |

