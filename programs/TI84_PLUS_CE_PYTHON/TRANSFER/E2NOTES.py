from APCORE import menu
from EFGUI import cards
GROUPS=[
('Choose a method',[
('What is asked?','Force/field from point charges: sum x/y components. Potential: signed scalar sum kQ/r. Work/speed: DeltaK=-q*DeltaV. Continuous finite source: integrate projected dE. Infinite plane/line or spherical symmetry: consider Gauss.'),
('Always show work','Draw source and observation point. State symmetry, equation, dq or Qenc, bounds, substitution, result and direction. Check SI units and limiting cases. Calculator output alone does not explain the physics.'),
('SI / constants','k=8.98755e9; eps0=8.85419e-12; e=1.60218e-19 C; me=9.10938e-31 kg; mp=1.67262e-27 kg. micro=1e-6, nano=1e-9, cm=1e-2 m. N/C=V/m. Enter 2e-9, not 2 for 2 nC.'),
('Exam scope','Canvas: notes 8.1-6,9.1. Electric force, electric field, potential, Gauss law. Corrected 8.4: axial rod, bisector rod, infinite line, arc center, ring axis and maximum. Later capacitors/circuits are retained in original menus, not confirmed Exam 2 topics.')]),
('Charge / force concepts',[
('Conservation','q=n*e. Charge is conserved. Electrons move in ordinary charging; protons stay bound in nuclei. Like charges repel; unlike attract. Coulomb force pair is equal and opposite regardless of masses. F=k*abs(q1*q2)/r^2.'),
('Contact / friction','Friction transfers electrons, leaving opposite net charges. Conduction allows transfer on contact. Identical isolated spheres equally share TOTAL charge. Nonidentical connected conductors reach equal potential, not necessarily equal charge.'),
('Polarization','Neutral objects can attract charges: electrons shift, nearer side is opposite the external charge. No transfer means net charge remains zero. An electroscope may show leaf separation from induction while its net charge is zero.'),
('Induction sequence','Bring rod close without contact. Ground conductor with rod still near. Disconnect ground FIRST. Then remove rod. Conductor ends with sign opposite rod. Negative rod drives electrons to ground; positive rod draws electrons from ground.'),
('Ground / balance','Ground is an electron reservoir. Grounding without nearby sources tends to neutralize conductor; with nearby charge it may charge it. For hanging charge in horizontal E: Tsin(theta)=abs(q)*E; Tcos(theta)=mg; tan(theta)=abs(q)*E/(mg).'),
('Vector forces','Draw forces on TARGET. Resolve components, add Fx and Fy, magnitude sqrt(Fx^2+Fy^2). Direction uses quadrant. Include gravity/tension. At equilibrium sumF=0. A source never exerts Coulomb force on itself.')]),
('Fields / conductors',[
('Field versus force','E=F/q; source point field=kQ*rhat/r^2. Field is force on a POSITIVE test charge. F=qE; negative test charge reverses force, not E. Small test charge has negligible effect on source configuration. a=qE/m.'),
('Field lines','Lines leave + and enter - or infinity. Tangent gives field direction; density shows strength. Lines never cross. Lines are generally NOT particle trajectories; velocity and inertia matter.'),
('Zero field on line','Like source signs: zero lies BETWEEN and nearer smaller magnitude. Unlike signs: fields add between; zero is OUTSIDE smaller-charge side. Equal opposite charges have no finite zero. Equate magnitudes only where directions oppose.'),
('Equilibrium conductor','E=0 within conducting MATERIAL. V constant throughout conductor. Excess charge resides on surfaces. External E perpendicular to surface. Tangential E would move charges. More charge concentration at sharp regions.'),
('Cavities','Empty fully enclosed cavity has E=0 with no internal charge. A charge q inside a cavity induces -q total on inner wall. If conductor net charge is Q, outer wall has Q+q. Do not assume E=0 in a cavity containing charge.'),
('Sphere / zero traps','Spherical conductor: E=0 inside; V=kQ/R constant with V(infinity)=0. Outside E=kQ/r^2, V=kQ/r. Midpoint equal + charges: E=0,V>0. Midpoint equal opposite: V=0,E nonzero. Zero flux does NOT imply E=0.')]),
('Gauss derivations',[
('Flux definition','Phi=integral(E dot dA). Flat uniform: E*A*cos(theta). theta to area NORMAL, not plane. Closed dA outward; outgoing positive, incoming negative. Units N*m^2/C. A Gaussian surface is imaginary.'),
('Gauss law','Closed integral(E dot dA)=Qenc/eps0. Include enclosed NET charge only. External charges give zero net flux but can change local E. Law always true; useful to solve E easily only with sufficient symmetry.'),
('Spherical symmetry','Choose concentric sphere r. E radial, constant magnitude on surface. E*4*pi*r^2=Qenc/eps0. For radial density rho(s), Qenc=integral(4*pi*s^2*rho(s) ds,0,r). Outside bounded sphere, Qenc=Qtotal.'),
('Uniform solid insulator','Inside r<R: Qenc=rho*4*pi*r^3/3=Q*r^3/R^3. E=kQ*r/R^3. Outside E=kQ/r^2. Field grows linearly from zero, continuous at R, then falls as 1/r^2. Insulator charges cannot move freely.'),
('Shell / conductor','Thin uniform shell: inside E=0 because Qenc=0 AND spherical symmetry. Outside E=kQ/r^2. Spherical conducting solid also has E=0 inside. At charged surface E jumps; use specified side/limit.'),
('Nonuniform sphere','rho(s)=alpha*s^n, integer n>=0. Qenc=4*pi*alpha*r^(n+3)/(n+3) inside. E=alpha*r^(n+1)/(eps0*(n+3)). Outside replace enclosed radius by R then divide by 4*pi*eps0*r^2. Do not multiply local rho(r) by volume.'),
('Infinite line','Coaxial Gaussian cylinder radius r length ell. E radial, constant on side; caps zero flux. E*2*pi*r*ell=lambda*ell/eps0. E=lambda/(2*pi*eps0*r). Finite rod lacks this symmetry; integrate it instead.'),
('Uniform solid cylinder','Infinite insulating cylinder radius R. Inside Qenc=rho*pi*r^2*ell; E=rho*r/(2*eps0). Outside Qenc=rho*pi*R^2*ell; E=rho*R^2/(2*eps0*r). End effects neglected.'),
('Infinite sheet','Isolated insulating sheet sigma: pillbox has two area-A faces. Equal fields on sides by reflection symmetry. Side flux zero. 2EA=sigma*A/eps0 so E=sigma/(2*eps0) outward for sigma>0.'),
('Conductor surface','Pillbox one face in conductor: Einside=0, so only outside face contributes. EA=sigma*A/eps0 -> Eoutside=sigma/eps0 along outward normal. sigma is local surface density. Factor differs from isolated insulating sheet.'),
('Opposite plates','Superpose +sigma and -sigma infinite-sheet fields. Between: E=sigma/eps0 from + toward -. Outside: cancellation. For finite large plates this works away from edges.'),
('Flux face traps','q at cube center: TOTAL flux=q/eps0; EACH face=q/(6eps0) by symmetry. Off-center q still inside: total unchanged; faces generally unequal. Qenc=0 -> net flux=0, not zero field. Open faces need their own integral or justified symmetry.')]),
('Potential / energy',[
('Scalar potential','V=U/q, volts=J/C. Point source V=kQ/r. Multiple sources: V=sum(kQi/ri), signed scalar. Finite isolated source uses V(infinity)=0. Potential depends on source, not test charge. Utest=qtest*Vsource.'),
('Work signs','DeltaU=q*DeltaV. Wfield=-DeltaU. Wexternal=DeltaU ONLY for DeltaK=0. With only electric work: DeltaK=-q*DeltaV. Use Kf=Ki-q*DeltaV, vf=sqrt(2Kf/m). If Kf<0, destination not reachable with stated initial energy.'),
('Motion','Released from rest, +q initially accelerates toward lower V; -q toward higher V. Both lower U. Initial velocity may carry a charge uphill while it slows. Force gives acceleration; it need not point along velocity.'),
('Uniform field','DeltaV=-E dot displacement=-E*d*cos(theta). Along E, V decreases; perpendicular displacement gives DeltaV=0. Parallel plates: E magnitude=abs(DeltaV)/spacing, away from edges.'),
('Equipotentials','E perpendicular to equal-V lines toward decreasing V. Equal voltage intervals closer together mean stronger E. Along equipotential, field work zero. Conductors at equilibrium are equipotentials. V=constant need not equal zero.'),
('Graphs / calculus','Ex=-dV/dx. E vector=-gradient V. DeltaV=-integral(Ex dx,A,B). E graph signed area -> negative voltage change. V flat locally -> Ex=0 locally. A point where V=0 need not have zero slope.'),
('Pair energy','Usystem=sum over DISTINCT pairs kqi*qj/rij. Count each pair ONCE. First charge from infinity costs zero; each later interacts with previous charges. Three equal q at equilateral d: U=3kq^2/d. +q,+q,-q there: U=-kq^2/d.'),
('Electron-volt','1 eV=1.60218e-19 J, an ENERGY unit. Charge +2e accelerating through a 10 V drop gains 20 eV. Electron through 200 V rise gains 200 eV. Nonrelativistic speed sqrt(2K/m); near light speed requires relativity.'),
('Reference limits','Inside spherical shell/conductor V=kQ/R constant, E=0. Infinite line: cannot choose V(infinity)=0; use V(r)-V(R)=-lambda*ln(r/R)/(2*pi*eps0). Potential reference shifts never change E or voltage differences.')]),
('Quick final formulas',[
('Forces and fields','F=k*abs(q1*q2)/r^2; Epoint=kQ/r^2 signed radially. F=qE; a=qE/m. Ex=sum(kQi*dx/ri^3); Ey=sum(kQi*dy/ri^3). V=sum(kQi/ri). q=n*e.'),
('Rods','FULL rod length L, total Q. Beyond end, a from NEAR END: E=kQ/[a*(a+L)]. Perpendicular bisector distance a>0: E=kQ/[a*sqrt(a^2+(L/2)^2)]. Infinite line: E=lambda/(2*pi*eps0*a). Negative charge reverses direction.'),
('Ring','Uniform ring R,Q; x from CENTER on axis: Ex=kQx/(R^2+x^2)^(3/2). V=kQ/sqrt(R^2+x^2). |E| peaks at |x|=R/sqrt(2), value 2k*abs(Q)/(3sqrt(3)*R^2). E(0)=0,V(0)=kQ/R.'),
('Arc center','Sweep phi RADIANS; lambda=Q/(R*phi). Magnitude E=2k*abs(Q)*sin(phi/2)/(R^2*phi). For Q>0 points AWAY from arc midpoint. Semicircle E=2k*abs(Q)/(pi*R^2); full circle E=0. V=kQ/R.'),
('Gauss results','Phi_closed=Qenc/eps0. Sphere: Er=Qenc/(4*pi*eps0*r^2). Infinite line: Er=lambda/(2*pi*eps0*r). Insulating sheet E=sigma/(2eps0); conductor Eout=sigma/eps0. Uniform sphere inside Er=kQr/R^3.'),
('Energy results','DeltaU=q*DeltaV=-Wfield. Kf=Ki-q*DeltaV. Slow Wext=DeltaU. Pair U=kq1q2/r. Uniform DeltaV=-E*d*cos(theta). Ex=-dV/dx. Equal-V line spacing: |E|~abs(DeltaV)/normal spacing.')]),
('Practice / common traps',[
('Practice first','Try before advancing: +4nC at x=0 and +1nC at x=.30m. Find E=0 point. Then find E at x=.15m. Positive +2uC moves slowly 40V to -10V: find DeltaU and work by field.'),
('Answers','E=0 at x=.20m from +4nC. At .15m E~+1198 N/C. DeltaV=-50V, DeltaU=-1e-4 J, Wfield=+1e-4 J, slow Wext=-1e-4 J. Zero-field location nearer smaller source.'),
('Check Gauss','Closed surface encloses +5nC and -2nC; +10nC external. Net flux=(3e-9)/eps0~338.8 N*m^2/C. External charge irrelevant to NET flux. Without enclosed charges net flux zero but E may be nonzero.'),
('High-value traps','Radians in integrals; arc degree prompts convert internally. Angle for flux is to normal. Project dE before integrating. Ring center vs rod endpoint are different. V scalars add signed; E vectors add components. Do not count pair energy twice.'),
('Final readiness','Derive rod/arc/ring from dq and bounds. Derive sphere/line/sheet from Gaussian surface and Qenc. Explain why E=0 differs from V=0 and zero flux. Show external-work assumptions. Redo missed homework without the guide.'),
('Assigned Gauss homework','Canvas HW8: p677 questions 1,3,5; p679 problems 1,5,13,29,35,39,49,52. Use your assigned textbook edition. Exact exam questions and calculator/reference policy were not verified.')])]
def show():
 while True:
  i=menu('EXAM 2 STUDY CARDS',[g[0] for g in GROUPS])
  if i<0:return
  cards(GROUPS[i][0],GROUPS[i][1])
