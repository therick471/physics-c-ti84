from math import sqrt,atan2,pi
from APCORE import menu,number,integer,result,fmt,info,CONST
from EFGUI import cards
import E2PHYS as P
def sources():
 rows=[]
 for i in range(integer('Charge count',1,15)):
  info('Source '+str(i+1),'Signed Q in C; coordinates in m.')
  rows.append((number('Q C'),number('Source x m'),number('Source y m')))
 return rows
def points():
 s=sources();x=number('Target x m');y=number('Target y m')
 ex,ey,v=P.point_sum(s,x,y);q=number('Test charge C (0 allowed)')
 pairs=[('Ex N/C',ex),('Ey N/C',ey),('|E| N/C',sqrt(ex*ex+ey*ey)),('V volts',v),('Fx N',q*ex),('Fy N',q*ey),('U test J',q*v)]
 if ex!=0 or ey!=0:pairs.insert(3,('E angle deg',atan2(ey,ex)*180/pi))
 result('Point-charge solution',pairs,'Angle CCW from +x. F=qE. U is test-charge energy, not assembly energy. Target must not coincide with a source.')
def gauss(i):
 if i in(0,1):
  q=number('Total Q C');R=number('Sphere R m','+');r=number('Distance r from CENTER m','0')
  e,v,enc=P.sphere(q,R,r,i)
  result('Spherical symmetry',[('Er N/C',e),('V volts',v),('Qenc C',enc)],'Uniform solid INSULATOR.' if i==0 else 'Thin uniform shell / spherical conductor. At r=R field uses OUTSIDE limit. V(infinity)=0.')
 elif i==2:
  rho=number('Volume rho C/m^3');R=number('Cylinder R m','+');r=number('Radial r m','0')
  result('Infinite cylinder',[('Er N/C',P.cylinder(rho,R,r))],'Uniform solid insulating cylinder; negligible end effects.')
 elif i==3:
  lam=number('lambda C/m');r=number('Radial r m','+')
  result('Infinite line',[('Er N/C',lam/(2*pi*P.EP*r))],'E*2*pi*r*ell=lambda*ell/eps0.')
 elif i==4:
  j=menu('Planar model',['Isolated insulating sheet','Just outside conductor','Opposite parallel sheets'])
  if j<0:return
  sig=number('Signed sigma C/m^2')
  result('Planar field',[('E N/C',sig/((2 if j==0 else 1)*P.EP))],['Signed outward on either side.','Signed outward normal.','sigma belongs to FIRST sheet. Axis points from first sheet toward second; field outside is zero.'][j])
 elif i==5:
  alpha=number('alpha for rho=alpha*r^n');n=integer('Power n (integer >=0)',0,12);R=number('Sphere R m','+');r=number('Observation r m','0')
  e,enc=P.power_sphere(alpha,n,R,r)
  result('Nonuniform sphere',[('Er N/C',e),('Qenc C',enc)],'Qenc=4*pi*alpha*min(r,R)^(n+3)/(n+3). E=Qenc/(4*pi*eps0*r^2).')
 elif i==6:
  q=number('Net enclosed charge C')
  result('Closed surface',[('Net flux N*m^2/C',q/P.EP)],'External charges affect E but add zero NET flux.')
 else:
  e=number('E signed N/C');a=number('Area m^2','0');th=number('Angle to NORMAL deg')
  result('Flat uniform flux',[('Flux N*m^2/C',P.flat_flux(e,a,th))],'Use angle to normal, not plane. Closed surfaces use outward normal.')
def work(i):
 if i==0:
  q=number('Test charge C');dv=number('Vfinal - Vinitial volts');m=number('Mass kg','+');vi=number('Initial speed m/s','0',0)
  du,w,k,v=P.energy(q,dv,m,vi)
  result('Electric work only',[('Delta U J',du),('W field J',w),('K final J',k),('Speed final m/s',v)],'DeltaK=-q*DeltaV. Nonrelativistic; fixed source field; no other work. Slow external work=DeltaU.')
 elif i==1:
  e=number('Field magnitude N/C','0');d=number('Displacement magnitude m','0');th=number('Angle E to displacement deg');q=number('Test charge C')
  dv=P.uniform(e,d,th)
  result('Uniform field',[('Delta V volts',dv),('Delta U J',q*dv),('W field J',-q*dv)],'DeltaV=-E*d*cos(theta). For slow motion Wexternal=DeltaU.')
 elif i==2:result('Assembly energy',[('Total U J',P.assembly(sources()))],'Each distinct pair counted once. Zero energy at infinite separation. Fixed sources; excludes self-energy.')
 elif i==3:
  q1=number('Q1 at x=0 C');q2=number('Q2 at x=d C');d=number('Separation d m','+');x=P.zero_field(q1,q2,d)
  if x is None:info('No finite zero','Equal opposite nonzero charges have no finite zero-field point on the line.')
  else:result('Zero field on line',[('x from Q1 m',x)],'Q1 at 0; Q2 at +d. Like charges: between. Unlike: outside smaller-charge side. This solves E=0, not V=0.')
 else:
  n=integer('Identical sphere count',2,10);q=0.0
  for k in range(n):q+=number('Initial Q'+str(k+1)+' C')
  result('Contact charge sharing',[('Final each Q C',q/n),('Total Q C',q)],'Identical isolated conductors brought to mutual equilibrium then separated. Unequal spheres need equal potential, not equal Q.')
