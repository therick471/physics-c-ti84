"""Build an E&M-only toolkit and notes-backed field studio, no packed exec."""
import ast,sys,shutil,json,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from package_toolkit import minify
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'EFIELD_SOURCE'
REL=ROOT/'EField_EM'
OUT=REL/'TRANSFER'
OUT.mkdir(parents=True,exist_ok=True)
for p in (ROOT/'APC_LITE').glob('*.py'):
 if p.stem in ['APTOOLS','APMECH','APEM','APLAB'] or p.stem in ['APU%02d'%i for i in range(1,8)]:continue
 shutil.copyfile(p,OUT/p.name)
notes=[
[
('1 Model and axes','Uniform NONCONDUCTING ring, radius R, signed total Q. Observation P is distance x from its center on the axis; x may be negative. r=sqrt(R^2+x^2). Transverse components cancel in pairs; axial components add.'),
('2 Density and dq','Circumference=2*pi*R. lambda=Q/(2*pi*R). Use azimuth phi around ring: dq=lambda*R*dphi, 0<=phi<=2*pi. Do not integrate the fixed projection angle theta.'),
('3 Project before adding','dE=k*dq/r^2. cos(theta)=x/r. Thus dE_x=k*dq*x/r^3=k*lambda*R*x*dphi/(R^2+x^2)^(3/2). r,x,R remain constant during this integral.'),
('4 Integrate and simplify','E_x=[k*lambda*R*x/(R^2+x^2)^(3/2)]*integral(1 dphi,0,2*pi). E_x=2*pi*k*lambda*R*x/(R^2+x^2)^(3/2)=k*Q*x/(R^2+x^2)^(3/2).'),
('5 Limits at 0 and R','E(0)=0: symmetry, not zero potential. E(x)->0 from either side as x->0. Near center E~k*Q*x/R^3. At x->R from either side: E=k*Q/(2*sqrt(2)*R^2). No singularity at x=R on the axis.'),
('6 Infinity and symmetry','As x->+infinity, E~k*Q/x^2 ->0. As x->-infinity, E~-k*Q/x^2 ->0. E(-x)=-E(x). E has sign Q*x. Far from a finite source it behaves like a point charge.'),
('7 Differentiate','dE/dx=k*Q*(R^2-2*x^2)/(R^2+x^2)^(5/2). Set numerator=0: R^2=2*x^2, x=+/-R/sqrt(2). For Q>0, slope changes + to - at +R/sqrt(2), giving a maximum.'),
('8 Extrema and graph','Emax=2*k*Q/(3*sqrt(3)*R^2) for Q>0, at x=R/sqrt(2). Signed minimum is the negative at -R/sqrt(2); Q<0 swaps them. |E| peaks at both positions and is 0 at x=0. Infinity is not an attained finite root.'),
('9 Potential and force','V=integral(k*dq/r)=k*Q/sqrt(R^2+x^2), V(infinity)=0. V(0)=k*Q/R, V(R)=k*Q/(sqrt(2)*R). E=-dV/dx. For Q>0 V is maximal at center; Q<0 gives a minimum. Force on q_test: F=q_test*E.'),
('10 Curvature and units','E inflections: x=0 and +/-sqrt(3/2)*R for Q nonzero. V inflections: +/-R/sqrt(2). E units N/C=V/m; V units J/C. Negative test charge reverses force, not the source field.')],
[
('1 Geometry / symmetry','Uniform nonconducting straight rod has FULL length L, centered at y=0. P=(x,0), x!=0, lies on its PERPENDICULAR bisector. Rod runs -L/2<=y<=L/2. Equal y and -y charges cancel transverse fields.'),
('2 Charge element','lambda=Q/L; dq=lambda*dy. r=sqrt(x^2+y^2). dE_x=(k*dq/r^2)*(x/r)=k*lambda*x*dy/(x^2+y^2)^(3/2). Keep the projection x/r; do not integrate magnitudes alone.'),
('3 Cartesian integral','E_x=k*lambda*x*integral[dy/(x^2+y^2)^(3/2)], y=-L/2 to L/2. Antiderivative: y/[x^2*sqrt(x^2+y^2)]. Evaluate BOTH endpoints, then multiply by k*lambda*x.'),
('4 Exact answer','E_x=k*lambda*L/[x*sqrt(x^2+(L/2)^2)] = k*Q/[x*sqrt(x^2+(L/2)^2)]. If a=L/2: E=k*Q/[x*sqrt(x^2+a^2)]. Positive Q and x>0 give +x field.'),
('5 Trig substitution','For x>0 let y=x*tan(theta). dy=x*sec(theta)^2*dtheta, r=x*sec(theta). dE_x=(k*lambda/x)*cos(theta)*dtheta. Limits: -theta0 to +theta0, theta0=atan(L/(2*x)).'),
('6 Trig evaluation','E=(k*lambda/x)*[sin(theta)](-theta0 to +theta0)=2*k*lambda*sin(theta0)/x. Since sin(theta0)=(L/2)/sqrt(x^2+(L/2)^2), this equals the Cartesian result.'),
('7 Center and infinity','As x->0+: E~2*k*lambda/x, diverging for nonzero lambda. x->0- reverses sign; E(0) is undefined on the ideal line. For |x|>>L: E~k*Q*sign(x)/x^2 ->0. Do not confuse this rod limit with the ring, whose E(0)=0.'),
('8 R, length and near field','If R denotes HALF rod length, R=L/2: at x->R, E=k*Q/(sqrt(2)*R^2). At x=L: E=2*k*Q/(sqrt(5)*L^2). For x<<L, E~2*k*lambda/x: an infinite-line approximation.'),
('9 Max/min and derivative','For x>0, dE/dx=-k*Q*(2*x^2+(L/2)^2)/[x^2*(x^2+(L/2)^2)^(3/2)]. For Q>0 it is always negative. |E| strictly decreases: no finite maximum, infimum 0 at infinity. No stationary point for Q nonzero.'),
('10 Potential and parameters','V=(2*k*Q/L)*ln[(sqrt(x^2+(L/2)^2)+L/2)/abs(x)]. V(infinity)=0; V diverges as x->0 for Q nonzero. At fixed lambda, L->infinity gives E=2*k*lambda/x. At fixed Q, L->0 gives a point charge. F=q_test*E.')],
[
('1 Geometry','Uniform NONCONDUCTING rod length L. Observation P is beyond one end. x>0 means distance from the NEAREST END, not the center. Source-to-P distances span x to x+L.'),
('2 Set up','lambda=Q/L; dq=lambda*dr. All field elements point along the rod axis, so no projection factor is needed: E=k*lambda*integral(dr/r^2,x,x+L).'),
('3 Integrate','Integral r^-2 dr=-1/r. E=k*lambda*[1/x-1/(x+L)]=k*lambda*L/[x*(x+L)]=k*Q/[x*(x+L)]. Positive Q gives field away from the rod.'),
('4 Limits','x->0+: E~k*lambda/x, unbounded. x->infinity: E~k*Q/x^2 ->0. At x=L: E=k*Q/(2*L^2). This near-end field is half the infinite-bisector near-field value for equal lambda and x.'),
('5 Extrema / potential','dE/dx=-k*Q*(2*x+L)/[x^2*(x+L)^2]. |E| decreases on x>0: no finite maximum or attained minimum. V=(k*Q/L)*ln[(x+L)/x], with V(infinity)=0. F=q_test*E.'),
('6 Parameter limits','At fixed lambda, L->infinity gives semi-infinite-rod E=k*lambda/x. At fixed Q, L->0 gives point-charge E=k*Q/x^2. Never substitute x=0 or place P inside the charged rod.')],
[
('1 Infinite line model','An infinite uniform straight line carries signed lambda C/m; total Q is not finite. P has perpendicular coordinate x!=0. Pair the charges above and below P: transverse fields cancel.'),
('2 Integrate','Use y=x*tan(theta) for x>0: E=(k*lambda/x)*integral cos(theta)dtheta, theta=-pi/2 to pi/2. E=(k*lambda/x)*[1-(-1)]=2*k*lambda/x.'),
('3 Gauss check','Choose a coaxial cylindrical Gaussian surface of radius abs(x), length ell. Flux=E*2*pi*abs(x)*ell. Enclosed charge=lambda*ell. E=lambda/(2*pi*eps0*abs(x)) in the outward radial direction.'),
('4 Limits and extrema','x->0+ is unbounded for nonzero lambda; x->0- has opposite sign. As |x|->infinity E->0. At x=R, E=2*k*lambda/R. |E| strictly decreases for x>0; no finite maximum or attained minimum.'),
('5 Potential reference','A line cannot have V(infinity)=0. Choose V(R)=0. Then V(x)=-2*k*lambda*ln(abs(x)/R). For lambda>0: V->+infinity at 0 and ->-infinity far away. E=-dV/dx. F=q_test*E.')],
[
('1 Arc geometry','Uniform nonconducting arc has radius R and sweep phi in RADIANS, 0<phi<=2*pi. P is its CENTER. Arc length=R*phi; lambda=Q/(R*phi). Arc midpoint angle beta points from P toward the charged arc, measured CCW from +x.'),
('2 Charge and direction','dq=lambda*R*dtheta; dE=k*dq/R^2. The field at the center points AWAY from positive charge: vector dE=-(k*lambda/R)*(cos(theta),sin(theta))*dtheta. Negative charge reverses it.'),
('3 Integrate components','Limits theta1=beta-phi/2, theta2=beta+phi/2. Ex=-(k*lambda/R)*[sin(theta2)-sin(theta1)]. Ey=(k*lambda/R)*[cos(theta2)-cos(theta1)].'),
('4 Symmetric-arc result','|E|=2*k*abs(lambda)*sin(phi/2)/R = [2*k*abs(Q)/(R^2*phi)]*sin(phi/2). For Q>0 vector E points opposite beta; Q<0 points toward beta. A left semicircle has beta=180 deg and positive-Q field to the right.'),
('5 Special cases','Full ring at center (phi=2*pi): E=0. Semicircle: |E|=2*k*abs(Q)/(pi*R^2). Quarter-circle: |E|=2*sqrt(2)*k*abs(Q)/(pi*R^2); each component magnitude is 2*k*abs(Q)/(pi*R^2). Add signed components when combining sectors.'),
('6 Max with fixed lambda','Holding lambda and R fixed: |E| proportional to sin(phi/2). Derivative proportional to cos(phi/2); zero at phi=pi (180 deg), a maximum. E=0 at full-ring sweep 2*pi and approaches 0 as phi->0 since Q=lambda*R*phi also tends to 0.'),
('7 Max with fixed Q','Holding TOTAL Q and R fixed changes lambda as phi varies. |E|=(k*abs(Q)/R^2)*sin(phi/2)/(phi/2), strictly decreases on 0<phi<=2*pi. Supremum k*abs(Q)/R^2 as phi->0; the maximum is NOT at phi=pi under this constraint.'),
('8 Potential / limits','V=k*Q/R for any sweep at the center; V(infinity)=0 for a finite arc. The center model has no axial observation x, so x->0,R,infinity is not its domain. For axial ring limits choose Ring mode. Increasing R at fixed Q makes |E| scale as 1/R^2; at fixed lambda and phi as 1/R.')]
]
for n,steps in enumerate(notes):
 (SRC/('EFN'+str(n)+'.py')).write_text('DATA='+repr('\n'.join(a+'|'+b for a,b in steps))+'\n')
# One consistent UI for E&M, math, numeric results, menus and notes.
base=(ROOT/'APC_LITE_SOURCE/APCORE.py').read_text()
tree=ast.parse(base)
for node in tree.body:
 if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name) and node.targets[0].id=='WIDTH':node.value=ast.Constant(28)
 if isinstance(node,ast.FunctionDef) and node.name=='menu':
  node.body=ast.parse("from EFGUI import choose\nreturn choose(title,items)").body
 if isinstance(node,ast.FunctionDef) and node.name=='info':
  node.body=ast.parse("from EFGUI import read\nread(title,text)").body
 if isinstance(node,ast.FunctionDef) and node.name=='number':
  # Retain numeric validation, but display the entire label and a short input line.
  code=ast.get_source_segment(base,node)
  start=code.index("        prompt = label[:23]")
  end=code.index("        if s.lower()",start)
  code=code[:start]+"        disp_clr()\n        for line in wrap(label): print(line)\n        print('SI units | q cancels')\n        if default is not None: print('ENTER keeps '+fmt(default))\n        s=input('> ').strip()\n"+code[end:]
  code=code.replace("print(str(e)[:WIDTH])","info('Check input',str(e))")
  updated=ast.parse(code).body[0]
  node.body=updated.body
ast.fix_missing_locations(tree)
(SRC/'APCORE.py').write_text(ast.unparse(tree)+'\n')
# E&M-only launcher retains all six E&M unit catalogs.
apc=(ROOT/'APC_LITE_SOURCE/APC.py').read_text()
a=apc.index('UNITS =') if 'UNITS =' in apc else apc.index('UNITS=')
b=apc.index('def unit_ui',a)
apc=apc[:a]+"UNITS=['Charge / fields / Gauss','Electric potential','Conductors / capacitors','Electric circuits','Magnetic fields','Induction / RL / LC']\n"+apc[b:]
apc=apc.replace('UNITS[unit-1]','UNITS[unit-8]').replace('UNITS[unit - 1]','UNITS[unit - 8]')
b=apc.index('def main():')
apc=apc[:b]+'''def main():
    while True:
        i=menu('PHYSICS C / E&M',['E-FIELD STUDIO','Final formulas','E&M equation reference','Math / calculus tools','Custom graph','Help'])
        if i<0:return
        try:
            if i==0:
                mod=__import__('EFAPP')
                mod.main()
                mod=None
            elif i==1:
                mod=__import__('EFFINAL')
                mod.show()
                mod=None
            elif i==2:
                j=menu('E&M units',UNITS)
                if j>=0: unit_ui(j+8)
            elif i==3:
                mod=__import__('APMATH')
                mod.main()
                mod=None
            elif i==4:
                mod=__import__('APGRAPH')
                mod.main()
                mod=None
            else: info('Quick start','Run EFIELD for the new guided solver, APC for all E&M tools. SI units; angles in radians except arc degree prompts. R is ring radius; L is FULL rod length. 0 Back; 8/9 pages. The printed notes are the source for the five derivation guides.')
        except Cancel:pass
        except (ValueError,ZeroDivisionError,OverflowError) as e:error(e)
        release(['APU08','APU09','APU10','APU11','APU12','APU13','APDATA','APFORM','APGRAPH','APMATH','APNUM','EFAPP','EFMODEL','EFTOOLS','EFINPUT','EFNOTE','EFCALC','EFEXT','EFINV','EFPLOT','EFFINAL']+['EFN'+str(n) for n in range(5)])
main()
'''
(SRC/'APC.py').write_text(apc)
# Remove mechanics plot presets; keep field sweeps and custom graphs.
graph=(ROOT/'APC_LITE_SOURCE/APGRAPH.py').read_text()
graph=graph[:graph.index('def main():')]+'''def main():
    s=input('f(x): ').strip()
    if s.lower()=='q':return
    lo,hi=number('LOW x'),number('HIGH x')
    draw('Custom f(x)', [('f',samples(lambda x:calc(s,{'x':x}),lo,hi,40))])
'''
(SRC/'APGRAPH.py').write_text(graph)
# Keep metadata only for E&M equations.
meta=(ROOT/'APC_LITE_SOURCE/APDATA.py').read_text()
tree=ast.parse(meta)
old=ast.literal_eval(tree.body[0].value)
keep={v[0] for u,e in json.loads((ROOT/'dev/catalog.json').read_text()) if u>=8 for v in e[2]}
trim='\n'+'\n'.join(line for line in old.split('\n') if line and line.split('|')[0] in keep)+'\n'
body=meta[meta.index('def row('):]
(SRC/'APDATA.py').write_text('U='+repr(trim)+'\n'+body)
# Split action code so a guide does not load all calculators and graph handlers.
full=(ROOT/'dev/ef_app_full.py').read_text()
funcs={n.name:ast.get_source_segment(full,n) for n in ast.parse(full).body if isinstance(n,ast.FunctionDef)}
headers={
 'EFINPUT':('from math import pi\nfrom APCORE import head,number,menu,Cancel\nfrom EFMODEL import NAMES\n',['parameters']),
 'EFNOTE':('from APMEM import release\nfrom EFMODEL import NAMES\nfrom EFGUI import cards\n',['guide']),
 'EFCALC':('from math import pi\nfrom APCORE import menu,number,result,fmt,LAST\nfrom EFNOTE import guide\nfrom EFINPUT import parameters\nfrom EFMODEL import field,arc_components\nfrom EFGUI import cards\n',['calculate']),
 'EFEXT':('from math import sqrt\nfrom APCORE import fmt\nfrom EFINPUT import parameters\nfrom EFMODEL import field\nfrom EFGUI import cards\n',['extrema']),
 'EFINV':('from APCORE import menu,number,info,result\nfrom EFMODEL import field,ring_distances,inverse_distance\n',['inverse']),
 'EFPLOT':('from APCORE import menu,number,info\nfrom EFINPUT import parameters\nfrom EFMODEL import field,NAMES\n',['plot'])}
for name,(header,names) in headers.items():
 (SRC/(name+'.py')).write_text(header+'\n\n'.join(funcs[n] for n in names)+'\n')
(SRC/'EFAPP.py').write_text("""from APCORE import menu,info,Cancel,error
from APMEM import release
from EFMODEL import NAMES
from EFGUI import GRAPHICS

def main():
    graphics=GRAPHICS[0]
    modules=['EFCALC','EFNOTE','EFEXT','EFPLOT','EFINV','EFGUI','EFFINAL']
    actions=['calculate','guide','extrema','plot','inverse','sketch','show']
    while True:
        i=menu('E-FIELD STUDIO v2',NAMES+['Final formulas','Two rings / point charges','Custom calculus / limits','Display: graphic/text'])
        if i<0:return
        try:
            if i<5:
                while True:
                    j=menu(NAMES[i],['Calculate E, V and force','Full derivation + limits','Maxima / minima','Graph E(x) or V(x)','Solve for source or x','Geometry sketch','Final formulas'])
                    if j<0:break
                    if j==5 and i not in (0,1):j=1
                    mod=None
                    gui=None
                    try:
                        gui=__import__('EFGUI')
                        gui.GRAPHICS[0]=graphics
                        mod=__import__(modules[j])
                        getattr(mod,actions[j])(i)
                        graphics=gui.GRAPHICS[0]
                    finally:
                        mod=None
                        gui=None
                        release([n for n in modules if n!='EFGUI']+['EFINPUT','EFMODEL','APGRAPH','APNUM'])
            elif i==5:
                mod=__import__('EFFINAL')
                try:mod.show()
                finally:
                    mod=None
                    release(['EFFINAL','APDATA'])
            elif i in (6,7):
                mod=__import__('EFTOOLS')
                try:mod.main(i==7)
                finally:
                    mod=None
                    release(['EFTOOLS','EFMODEL','APGRAPH','APNUM'])
            else:
                graphics=not graphics
                GRAPHICS[0]=graphics
                info('Display','Arrow keys move. ENTER selects or advances. CLEAR returns. 8/9 change pages. Full labels wrap across rows.')
        except Cancel:pass
        except (ValueError,ZeroDivisionError,OverflowError) as e:error(e)
        except MemoryError:info('Memory','Restart Python; run EFIELD directly.')
""")
for p in SRC.glob('*.py'):
 text=p.read_text();ast.parse(text)
 (OUT/p.name).write_text(minify(text),encoding='ascii')
print('TOTAL',len(list(OUT.glob('*.py'))),sum(p.stat().st_size for p in OUT.glob('*.py')),'bytes')
