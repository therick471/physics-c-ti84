"""Build compact TI-Python catalogs. SymPy is build-only, never on device."""
from pathlib import Path
import sympy as S
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'APC_EVO'
# name: label, SI unit, domain ('s' signed, '+' >0, '0' >=0)
V = {}
def vars_group(names, label, unit, domain='s'):
    for name in names.split(','):
        V[name] = (name, label, unit, domain)
vars_group('v,u,v1,v2,vf,v0,vr', 'velocity', 'm/s')
vars_group('a', 'acceleration', 'm/s^2')
vars_group('t,T,tau', 'time', 's', '0')
vars_group('x,x0,dx,d,h,y', 'position/displacement', 'm')
vars_group('r,R,l,Ls', 'length/radius', 'm', '+')
vars_group('m,m1,m2,M', 'mass', 'kg', '+')
vars_group('F,N,F1,F2', 'force', 'N')
vars_group('mu', 'friction coeff', '1', '0')
vars_group('th,ph,theta,theta0,dtheta', 'angle', 'rad')
vars_group('b', 'linear drag coeff', 'kg/s', '+')
vars_group('ks', 'spring constant', 'N/m', '+')
vars_group('W,K,U,E,U0,Ki,Kf,Ui,Uf', 'energy/work', 'J')
vars_group('K,Ki,Kf', 'kinetic energy', 'J', '0')
vars_group('N', 'normal force', 'N', '0')
vars_group('P', 'power', 'W')
vars_group('p,J', 'momentum/impulse', 'kg*m/s')
vars_group('w,w0,wf', 'angular velocity', 'rad/s')
vars_group('alpha', 'angular accel', 'rad/s^2')
vars_group('I,I1,I2', 'moment of inertia', 'kg*m^2', '+')
vars_group('tor', 'torque', 'N*m')
vars_group('ang', 'angular momentum', 'kg*m^2/s')
vars_group('f', 'frequency', 'Hz', '+')
vars_group('amp', 'amplitude', 'm', '0')
vars_group('kap', 'torsion constant', 'N*m/rad', '+')
vars_group('q,q1,q2,Q,Q0', 'charge', 'C')
vars_group('Ef', 'electric field', 'N/C')
vars_group('flux', 'electric flux', 'N*m^2/C')
vars_group('A', 'area', 'm^2', '+')
vars_group('lam', 'line charge density', 'C/m')
vars_group('sig', 'surface charge density', 'C/m^2')
vars_group('rhoq', 'volume charge density', 'C/m^3')
vars_group('V,V0,Vb,dV,emf', 'voltage', 'V')
vars_group('C,C1,C2', 'capacitance', 'F', '+')
vars_group('kd', 'dielectric constant', '1', '+')
vars_group('ue,ub', 'energy density', 'J/m^3', '0')
vars_group('cur,cur0', 'current', 'A')
vars_group('res,res1,res2,ri', 'resistance', 'ohm', '+')
vars_group('rhoe', 'resistivity', 'ohm*m', '+')
vars_group('n', 'carrier density', '1/m^3', '+')
vars_group('vd', 'drift speed', 'm/s', '0')
vars_group('B', 'magnetic field', 'T')
vars_group('Nm', 'turn count', '1', '+')
vars_group('nt', 'turns per length', '1/m', '+')
vars_group('mom', 'magnetic moment', 'A*m^2')
vars_group('fluxB,dflux', 'magnetic flux', 'Wb')
vars_group('ind', 'inductance', 'H', '+')
vars_group('nc', 'signed charge count', '1')
vars_group('jcur', 'current density', 'A/m^2')

# Unit | name | equation | variables | assumptions | numeric-only targets
ROWS = r'''
1|Velocity update|v=u+a*t|v,u,a,t|Constant acceleration; signed 1D.|
1|Displacement|dx=u*t+a*t^2/2|dx,u,a,t|Constant acceleration; keep physical time branch.|
1|Speed-distance|v^2=u^2+2*a*dx|v,u,a,dx|Constant acceleration; both velocity signs may fit.|
1|Average velocity|dx=(u+v)*t/2|dx,u,v,t|Constant acceleration only.|
1|Relative velocity|vr=v1-v2|vr,v1,v2|Same axis; velocity of 1 as seen from 2.|
1|Horizontal component|v=u*cos(th)|v,u,th|Angles radians. Angle solved by numeric bracket.|th
1|Vertical component|v=u*sin(th)|v,u,th|Angles radians. Angle solved by numeric bracket.|th
1|Projectile range|R=v0^2*sin(2*th)/g|R,v0,th|Same launch/landing height; no air; g=9.8.|th
1|Projectile peak|h=v0^2*sin(th)^2/(2*g)|h,v0,th|Height above launch; no air; rising launch.|th
2|Newton second law|F=m*a|F,m,a|F is NET force along selected axis.|
2|Kinetic friction|F=mu*N|F,mu,N|Magnitude; direction opposes slipping.|
2|Static friction limit|F=mu*N|F,mu,N|MAXIMUM static friction, not actual friction.|
2|Spring force|F=-ks*x|F,ks,x|x measured from spring equilibrium.|
2|Gravity force|F=G*M*m/r^2|F,M,m,r|Magnitude; point masses or external spheres.|
2|Circular acceleration|a=v^2/r|a,v,r|Radial magnitude; inward direction.|
2|Centripetal net force|F=m*v^2/r|F,m,v,r|NET radial force; not an additional force.|
2|Incline gravity|F=m*g*sin(th)|F,m,th|Component downhill; g=9.8.|th
2|Incline normal|N=m*g*cos(th)|N,m,th|No other perpendicular forces; g=9.8.|th
2|Ideal banked turn|v^2=r*g*tan(th)|v,r,th|No friction; angle from horizontal.|th
2|Linear drag terminal|v=m*g/b|v,m,b|Downward terminal speed; drag=-b*v.|
2|Fall with linear drag|v=m*g/b*(1-exp(-b*t/m))|v,m,b,t|Starts at rest; positive downward; g=9.8.|m,b
2|Orbital speed|v^2=G*M/r|v,M,r|Circular orbit; r from source center.|
2|Orbit period|T^2=4*pi^2*r^3/(G*M)|T,r,M|Circular orbit; negligible orbiting mass.|
3|Kinetic energy|K=m*v^2/2|K,m,v|K>=0; velocity sign cannot follow from K alone.|
3|Constant-force work|W=F*d*cos(th)|W,F,d,th|th between force and displacement; radians.|th
3|Work-energy|W=Kf-Ki|W,Kf,Ki|W is total net work.|
3|Height potential|U=m*g*h|U,m,h|Near Earth; chosen zero; g=9.8.|
3|Spring energy|U=ks*x^2/2|U,ks,x|x from unstretched length; energy>=0.|
3|Gravity potential|U=-G*M*m/r|U,M,m,r|Zero at infinity; point/spherical source.|
3|Energy balance|Kf+Uf=Ki+Ui+W|Kf,Uf,Ki,Ui,W|W is external/nonconservative work.|
3|Average power|P=W/t|P,W,t|t>0; work over this interval.|
3|Instant force power|P=F*v*cos(th)|P,F,v,th|th between vectors; radians.|th
3|Escape speed|v^2=2*G*M/r|v,M,r|Neglect drag; zero final speed at infinity.|
3|Circular orbit energy|E=-G*M*m/(2*r)|E,M,m,r|Total K+U for circular orbit.|
4|Linear momentum|p=m*v|p,m,v|Signed 1D component.|
4|Constant-force impulse|J=F*t|J,F,t|F constant or average NET force.|
4|Impulse change|J=m*(v-u)|J,m,v,u|Constant mass; net external impulse.|
4|Stick collision|m1*v1+m2*v2=(m1+m2)*vf|m1,v1,m2,v2,vf|Perfectly inelastic; isolated 1D system.|
4|Momentum balance|m1*u+m2*v=m1*v1+m2*v2|m1,u,m2,v,v1,v2|Signed 1D; negligible external impulse.|
4|Center of mass 2|x=(m1*x0+m2*dx)/(m1+m2)|x,m1,x0,m2,dx|x0 and dx are the two positions.|
5|Angular velocity|w=w0+alpha*t|w,w0,alpha,t|Constant angular acceleration.|
5|Angular displacement|dtheta=w0*t+alpha*t^2/2|dtheta,w0,alpha,t|Constant angular acceleration; radians.|
5|Angular speed-angle|w^2=w0^2+2*alpha*dtheta|w,w0,alpha,dtheta|Constant angular acceleration.|
5|Arc length|dx=r*dtheta|dx,r,dtheta|Angles radians.|
5|Tangential speed|v=r*w|v,r,w|Signed tangential component.|
5|Tangential acceleration|a=r*alpha|a,r,alpha|Signed tangential acceleration.|
5|Rotational dynamics|tor=I*alpha|tor,I,alpha|NET torque about fixed axis.|
5|Force torque|tor=r*F*sin(th)|tor,r,F,th|th between r and F; radians.|th
5|Parallel axis|I=I1+m*d^2|I,I1,m,d|I1 about parallel axis through COM.|
5|Point mass inertia|I=m*r^2|I,m,r|r perpendicular distance to axis.|
5|Disk cylinder inertia|I=m*R^2/2|I,m,R|Uniform solid disk/cylinder; symmetry axis.|
5|Hoop inertia|I=m*R^2|I,m,R|Thin hoop; central symmetry axis.|
5|Solid sphere inertia|I=2*m*R^2/5|I,m,R|Uniform solid sphere through center.|
5|Shell sphere inertia|I=2*m*R^2/3|I,m,R|Thin spherical shell through center.|
5|Rod center inertia|I=m*l^2/12|I,m,l|Uniform thin rod; perpendicular center axis.|
5|Rod end inertia|I=m*l^2/3|I,m,l|Uniform thin rod; perpendicular end axis.|
6|Rotational energy|K=I*w^2/2|K,I,w|Fixed-axis rotation.|
6|Angular momentum|ang=I*w|ang,I,w|Fixed axis, rigid-body component.|
6|Angular impulse|ang=tor*t|ang,tor,t|ang here means CHANGE in angular momentum.|
6|Spin conservation|I1*w0=I2*wf|I1,w0,I2,wf|Zero net external torque.|
6|Rotation work|W=tor*dtheta|W,tor,dtheta|Constant torque; radians.|
6|Rotation power|P=tor*w|P,tor,w|Same-axis components.|
6|Rolling total energy|K=m*v^2/2+I*v^2/(2*r^2)|K,m,v,I,r|Rolling without slipping; I through COM.|
6|Rolling incline accel|a=g*sin(th)/(1+I/(m*r^2))|a,th,I,m,r|Rolling without slipping; enough static friction.|th
6|Particle angular mom|ang=m*v*r*sin(th)|ang,m,v,r,th|th between r and v; about chosen origin.|th
7|Spring period|T=2*pi*sqrt(m/ks)|T,m,ks|Ideal mass-spring; no damping.|
7|Pendulum period|T=2*pi*sqrt(l/g)|T,l|Small angle; point bob; g=9.8.|
7|Physical pendulum|T=2*pi*sqrt(I/(m*g*d))|T,I,m,d|Small angle; d pivot-to-COM positive.|
7|Torsion period|T=2*pi*sqrt(I/kap)|T,I,kap|Linear restoring torque=-kap*angle.|
7|Frequency period|f=1/T|f,T|Positive frequency and period.|
7|Angular frequency|w=2*pi*f|w,f|w here is positive oscillation frequency.|
7|Spring frequency|w^2=ks/m|w,ks,m|Choose positive angular frequency.|
7|SHM acceleration|a=-w^2*x|a,w,x|x from equilibrium; positive frequency.|
7|SHM energy|E=ks*amp^2/2|E,ks,amp|Total mass-spring energy; amp>=0.|
7|SHM speed-position|v^2=w^2*(amp^2-x^2)|v,w,amp,x|abs(x)<=amp; choose sign from motion.|
7|SHM position|x=amp*cos(w*t+ph)|x,amp,w,t,ph|Undamped sinusoid; phase in radians.|w,t,ph
8|Coulomb magnitude|F=ke*abs(q1*q2)/r^2|F,q1,q2,r|Magnitude; use signs to decide attract/repel.|q1,q2
8|Point charge field|Ef=ke*q/r^2|Ef,q,r|Signed outward radial component.|
8|Electric force|F=q*Ef|F,q,Ef|Same-axis signed components.|
8|Uniform electric flux|flux=Ef*A*cos(th)|flux,Ef,A,th|th between E and outward area normal.|th
8|Gauss law|flux=q/eps0|flux,q|q is enclosed NET charge; closed surface.|
8|Infinite line field|Ef=lam/(2*pi*eps0*r)|Ef,lam,r|Signed radial; infinite uniform line.|
8|Infinite sheet field|Ef=sig/(2*eps0)|Ef,sig|Nonconducting infinite isolated sheet; one side.|
8|Conductor surface|Ef=sig/eps0|Ef,sig|Just outside electrostatic conductor; outward.|
8|Uniform sphere inside|Ef=ke*Q*r/R^3|Ef,Q,r,R|Only 0<r<=R; uniform volume charge.|
8|Uniform cylinder inside|Ef=rhoq*r/(2*eps0)|Ef,rhoq,r|Infinite uniform volume cylinder; r inside.|
8|Ring axis field|Ef=ke*Q*x/(x^2+R^2)^(3/2)|Ef,Q,x,R|Uniform ring; x along axis from center.|x
8|Disk axis field|Ef=sig/(2*eps0)*(1-x/sqrt(x^2+R^2))|Ef,sig,x,R|Uniform disk; x>=0 on positive axis.|x,R
8|Charge quantization|Q=nc*qe|Q,nc|nc is signed integer count of elementary charges.|
8|Uniform sphere charge|Q=rhoq*4*pi*R^3/3|Q,rhoq,R|Uniform volume charge density.|
9|Point potential|V=ke*q/r|V,q,r|Zero potential at infinity.|
9|Charge potential energy|U=ke*q1*q2/r|U,q1,q2,r|Signed pair energy; zero at infinity.|
9|Potential energy change|U=q*dV|U,q,dV|U here means CHANGE in potential energy.|
9|Uniform field voltage|dV=-Ef*d|dV,Ef,d|d along chosen field axis; uniform field.|
9|Electric work|W=-q*dV|W,q,dV|Work done by electric force.|
9|Ring axis potential|V=ke*Q/sqrt(x^2+R^2)|V,Q,x,R|Uniform ring; zero at infinity.|
9|Sphere inside potential|V=ke*Q*(3-r^2/R^2)/(2*R)|V,Q,r,R|Uniform solid sphere; r<=R; V infinity=0.|R
9|Shell inside potential|V=ke*Q/R|V,Q,R|Thin charged sphere/conductor; inside.|
9|Line potential diff|dV=-lam*ln(R/r)/(2*pi*eps0)|dV,lam,R,r|Infinite line; dV=V(R)-V(r).|
9|Electric kinetic energy|Kf-Ki=-q*dV|Kf,Ki,q,dV|Only electric force does work.|
9|Rod axis field|Ef=ke*lam*(1/x-1/(x+l))|Ef,lam,x,l|Uniform rod; target x>0 beyond near end.|
9|Rod axis potential|V=ke*lam*ln((x+l)/x)|V,lam,x,l|Uniform rod; target x>0 beyond near end.|
10|Capacitance definition|Q=C*V|Q,C,V|V across capacitor; signed plate charge.|
10|Parallel plate C|C=kd*eps0*A/d|C,kd,A,d|Full dielectric fill; d>0; neglect fringing.|
10|Capacitor energy CV|U=C*V^2/2|U,C,V|Stored energy>=0.|
10|Capacitor energy Q|U=Q^2/(2*C)|U,Q,C|Stored energy>=0.|
10|Capacitor energy QV|U=Q*V/2|U,Q,V|Consistent signs for Q and V.|
10|Capacitors parallel 2|C=C1+C2|C,C1,C2|Same potential difference.|
10|Capacitors series 2|1/C=1/C1+1/C2|C,C1,C2|Same charge magnitude; ideal initially uncharged.|
10|Electric energy density|ue=kd*eps0*Ef^2/2|ue,kd,Ef|Linear dielectric; kd=1 in vacuum.|
10|Spherical conductor C|C=4*pi*eps0*R|C,R|Isolated sphere; potential relative infinity.|
10|Spherical capacitor|C=4*pi*eps0*r*R/(R-r)|C,r,R|Concentric vacuum shells; 0<r<R.|
10|Coaxial capacitor|C=2*pi*eps0*l/ln(R/r)|C,l,R,r|Vacuum cylinders; 0<r<R; ignore ends.|
10|Capacitor charge sharing|V=(C1*V0+C2*Vb)/(C1+C2)|V,C1,V0,C2,Vb|Parallel after disconnecting batteries; charge conserved.|
10|Sphere charge sharing|q=Q*r/(r+R)|q,Q,r,R|Far-separated conducting spheres joined by wire; Q total.|
11|Current charge|Q=cur*t|Q,cur,t|Constant or average current.|
11|Ohm law|V=cur*res|V,cur,res|Ohmic resistor; V is voltage drop.|
11|Resistance geometry|res=rhoe*l/A|res,rhoe,l,A|Uniform cross-section and resistivity.|
11|Drift current|cur=n*qe*A*vd|cur,n,A,vd|Current magnitude; qe is elementary magnitude.|
11|Current density|cur=jcur*A|cur,jcur,A|Uniform current density normal to cross-section.|
11|Resistors series 2|res=res1+res2|res,res1,res2|Same current.|
11|Resistors parallel 2|1/res=1/res1+1/res2|res,res1,res2|Same voltage.|
11|Electrical power IV|P=cur*V|P,cur,V|Passive sign convention.|
11|Electrical power IR|P=cur^2*res|P,cur,res|Resistor dissipated power.|
11|Electrical power VR|P=V^2/res|P,V,res|Resistor dissipated power.|
11|Battery terminal V|V=emf-cur*ri|V,emf,cur,ri|Discharging positive current; internal ri>0.|
11|RC time constant|tau=res*C|tau,res,C|Equivalent R seen by capacitor.|
11|RC voltage charging|V=Vb*(1-exp(-t/(res*C)))|V,Vb,t,res,C|Initially uncharged; constant ideal source.|
11|RC voltage discharge|V=V0*exp(-t/(res*C))|V,V0,t,res,C|Source-free discharge; t>=0.|
11|RC current charging|cur=Vb/res*exp(-t/(res*C))|cur,Vb,res,t,C|Initially uncharged; resistor current.|res
12|Magnetic force qv|F=q*v*B*sin(th)|F,q,v,B,th|Signed scalar factor; direction via q(v cross B).|th
12|Wire magnetic force|F=cur*l*B*sin(th)|F,cur,l,B,th|Uniform B; direction via L cross B.|th
12|Charged orbit radius|r=m*v/(abs(q)*abs(B))|r,m,v,q,B|Speed v>0; v perpendicular B; q,B nonzero.|q,B
12|Cyclotron period|T=2*pi*m/(abs(q)*abs(B))|T,m,q,B|Nonrelativistic; nonzero charge and field.|q,B
12|Long wire field|B=mu0*cur/(2*pi*r)|B,cur,r|Infinite straight wire; sign via right hand rule.|
12|Loop center field|B=mu0*Nm*cur/(2*R)|B,Nm,cur,R|Nm identical circular loops; center.|
12|Solenoid field|B=mu0*nt*cur|B,nt,cur|Long air-core solenoid, interior.|
12|Toroid field|B=mu0*Nm*cur/(2*pi*r)|B,Nm,cur,r|Ideal toroid inside windings.|
12|Wire-wire force|F=mu0*cur*cur0*l/(2*pi*r)|F,cur,cur0,l,r|Parallel long wires; same-direction attracts.|
12|Magnetic moment|mom=Nm*cur*A|mom,Nm,cur,A|Planar loop; normal by right hand rule.|
12|Loop torque|tor=mom*B*sin(th)|tor,mom,B,th|th between moment normal and B.|th
12|Dipole energy|U=-mom*B*cos(th)|U,mom,B,th|th between magnetic moment and B.|th
12|Velocity selector|v=Ef/B|v,Ef,B|Magnitudes for crossed perpendicular E,B; undeflected beam.|
12|Solid wire inside B|B=mu0*cur*r/(2*pi*R^2)|B,cur,r,R|Uniform current density in long solid wire; r<=R.|
12|Arc center field|B=mu0*cur*th/(4*pi*r)|B,cur,th,r|Circular arc subtends th radians; radial leads contribute zero.|
13|Magnetic flux|fluxB=B*A*cos(th)|fluxB,B,A,th|Uniform field; angle to area normal.|th
13|Faraday average emf|emf=-Nm*dflux/t|emf,Nm,dflux,t|dflux per turn; fixed sign convention.|
13|Motional emf|emf=B*l*v|emf,B,l,v|Perpendicular rod, velocity and field.|
13|Self-induced emf|emf=-ind*cur/t|emf,ind,cur,t|cur here is CHANGE in current over t.|
13|Inductor energy|U=ind*cur^2/2|U,ind,cur|Ideal inductor energy>=0.|
13|Solenoid inductance|ind=mu0*Nm^2*A/l|ind,Nm,A,l|Long air-core solenoid; ignore ends.|
13|Magnetic energy density|ub=B^2/(2*mu0)|ub,B|Vacuum.|
13|RL time constant|tau=ind/res|tau,ind,res|Equivalent series resistance.|
13|RL current rise|cur=Vb/res*(1-exp(-res*t/ind))|cur,Vb,res,t,ind|Initially zero current; constant source.|res
13|RL current decay|cur=cur0*exp(-res*t/ind)|cur,cur0,res,t,ind|Source-free series RL circuit.|
13|LC period|T=2*pi*sqrt(ind*C)|T,ind,C|Ideal LC; no resistance.|
13|LC angular frequency|w^2=1/(ind*C)|w,ind,C|Choose positive angular frequency.|
13|LC peak current|cur^2=Q0^2/(ind*C)|cur,Q0,ind,C|Magnitude from total LC energy; choose positive peak.|
13|LC charge vs time|Q=Q0*cos(w*t+ph)|Q,Q0,w,t,ph|Ideal LC; phase radians; current is dQ/dt.|w,t,ph
13|Rotating coil emf|emf=Nm*B*A*w*sin(w*t+ph)|emf,Nm,B,A,w,t,ph|Uniform B; flux=Nm*B*A*cos(w*t+ph).|w,t,ph
'''

def build():
    units = {i: [] for i in range(1, 14)}
    all_entries = []
    for row in ROWS.strip().splitlines():
        unit, title, equation, names, note, skip = row.split('|')
        names = names.split(',')
        symbols = {n: S.Symbol(n, real=True) for n in names}
        locals_ = dict(symbols)
        for c in ['g', 'G', 'ke', 'eps0', 'mu0', 'qe']:
            locals_[c] = S.Symbol(c, positive=True)
        locals_.update({'pi': S.pi, 'abs': S.Abs, 'ln': S.log})
        lhs, rhs = equation.replace('^', '**').split('=')
        expression = S.sympify(lhs, locals=locals_) - S.sympify(rhs, locals=locals_)
        inverse = []
        polys = []
        for n in names:
            try:
                numerator = S.together(expression).as_numer_denom()[0]
                poly = S.Poly(numerator, symbols[n])
                coeff = poly.all_coeffs() if 1 <= poly.degree() <= 2 else []
                polys.append([S.pycode(c).replace('math.', '').replace('log(', 'ln(').replace('**', '^') for c in coeff])
            except S.PolynomialError:
                polys.append([])
            if n in skip.split(','):
                inverse.append([])
                continue
            try:
                solutions = S.solve(expression, symbols[n], check=False)
                out = []
                for sol in solutions:
                    text = S.pycode(sol).replace('math.', '').replace('abs(', 'abs(')
                    # Python code printer's fabs and unsupported piecewise are excluded.
                    if any(t in text for t in [' if ', ' else ', '1j', 'complex', 'nan', 'inf', 'sign(']):
                        continue
                    out.append(text.replace('log(', 'ln(').replace('**', '^'))
                inverse.append(out)
            except NotImplementedError:
                inverse.append([])
        specs = [V[n] for n in names]
        entry = (title, equation, specs, inverse, note, polys)
        units[int(unit)].append(entry)
        all_entries.append((int(unit), entry))
    for unit, entries in units.items():
        path = OUT / ('APU' + str(unit).zfill(2) + '.py')
        path.write_text('# Unit ' + str(unit) + ' generated formula catalog.\nF = ' + repr(entries) + '\n', encoding='ascii')
    (ROOT / 'dev' / 'catalog.json').write_text(json.dumps(all_entries, indent=2))
    print('Built', len(all_entries), 'formulas in 13 unit modules')

if __name__ == '__main__':
    build()
