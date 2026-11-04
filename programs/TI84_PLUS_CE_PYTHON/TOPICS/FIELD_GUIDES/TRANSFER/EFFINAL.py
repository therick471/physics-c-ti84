from APCORE import menu
from EFGUI import cards
from APMEM import release
FINAL=[('Ring: on its axis','Ex','k*Q*x/(R^2+x^2)^(3/2)','k*Q/sqrt(R^2+x^2)','R>0: ring radius. Q: signed total charge. x: signed distance from CENTER along axis.','x_peak=+/-R/sqrt(2). |E|max=2*k*abs(Q)/(3*sqrt(3)*R^2). E(0)=0. E(R)=k*Q/(2*sqrt(2)*R^2). E(+/-infinity)->0.'),('Rod: perpendicular bisector','Ex','k*Q/(x*sqrt(x^2+(L/2)^2))','(2*k*Q/L)*ln((sqrt(x^2+(L/2)^2)+L/2)/abs(x))','L>0: FULL rod length; lam=Q/L. x!=0: perpendicular coordinate from MIDPOINT. E=2*k*lam*sin(theta0)/x, theta0=atan(L/(2*x)) for x>0.','For nonzero Q: |E| has no finite maximum. x->0: E~2*k*lam/x. abs(x)>>L: E~k*Q*sign(x)/x^2 ->0. At x=L/2: E=2*sqrt(2)*k*Q/L^2.'),('Rod: beyond an end','E','k*Q/(x*(x+L))','(k*Q/L)*ln((x+L)/x)','L>0: FULL length. x>0: distance from NEAR END, measured outward along rod axis. lam=Q/L.','For nonzero Q, |E| decreases for x>0; no finite maximum. x->0+: E~k*lam/x. x->infinity: E~k*Q/x^2 ->0. E(L)=k*Q/(2*L^2).'),('Infinite straight line','Ex','2*k*lam/x','-2*k*lam*ln(abs(x)/R)','lam: signed charge per length C/m. x!=0: perpendicular coordinate. R>0: reference radius with V(R)=0. E=lam/(2*pi*eps0*x).','For nonzero lam: |E| decreases for x>0; no finite maximum. E(R)=2*k*lam/R. abs(x)->infinity: E->0. V(infinity)=0 cannot be chosen for an infinite line.'),('Arc: field at center','E0','2*k*Q*sin(phi/2)/(R^2*phi)','k*Q/R','R>0. phi: sweep in RADIANS, 0<phi<=2*pi. beta: angle from +x TOWARD arc midpoint. lam=Q/(R*phi). Ex=-E0*cos(beta); Ey=-E0*sin(beta).','|E|=abs(E0)=2*k*abs(lam)*sin(phi/2)/R. Semicircle: 2*k*abs(Q)/(pi*R^2). Quarter arc: 2*sqrt(2)*k*abs(Q)/(pi*R^2). Full circle: E=0. Fixed lam: peak at phi=pi. Fixed Q: supremum k*abs(Q)/R^2 as phi->0.')]
EXTRA=[('Two rings: charge ratio',[('Final ratio','Q1/Q2=(b/a)*[(R1^2+a^2)/(R2^2+b^2)]^(3/2).'),('Conditions','P lies BETWEEN rings; a,b>0 are distances from their centers to P. SAME-sign charges cancel. For R1=R2=R, a=R, b=2R: Q1/Q2=2*(2/5)^(3/2)=0.505964426.')]),('Two rings: net field',[('Final field','Ex=sum_i[k*Qi*(x-ci)/(Ri^2+(x-ci)^2)^(3/2)].'),('Final potential','V=sum_i[k*Qi/sqrt(Ri^2+(x-ci)^2)].'),('Variables','ci: signed center coordinate of ring i. Ri>0: radius. Qi: signed charge. x: observation coordinate on common axis. Use i=1,2 for two rings.')]),('Point charges in 2D',[('Final components','Ex=k*sum_i[qi*dxi/ri^3]. Ey=k*sum_i[qi*dyi/ri^3]. |E|=sqrt(Ex^2+Ey^2).'),('Potential / force','V=k*sum_i[qi/ri]. Fx=q_test*Ex; Fy=q_test*Ey.'),('Variables','dxi=x-xi; dyi=y-yi; ri=sqrt(dxi^2+dyi^2)>0. (x,y): target. (xi,yi): source. qi is signed. Add components, not magnitudes.')]),('Sum of arc sectors',[('Final components','Ai=2*k*Qi*sin(phi_i/2)/(Ri^2*phi_i). Ex=-sum_i[Ai*cos(beta_i)]. Ey=-sum_i[Ai*sin(beta_i)]. |E|=sqrt(Ex^2+Ey^2).'),('Final potential','V=sum_i[k*Qi/Ri].'),('Conditions','All arcs share the observation CENTER. Ri>0, signed Qi, 0<phi_i<=2*pi radians. beta_i points toward each arc midpoint. At phi_i=2*pi take Ai=0.')]),('Constants / force',[('Constants','k=1/(4*pi*eps0)=8.9875517923e9 N*m^2/C^2. eps0=8.8541878128e-12 F/m.'),('Force and units','F_vector=q_test*E_vector. E in N/C=V/m; V in volts; Q,q in C; lam in C/m; lengths in m. ln is natural log. Potential zero is at infinity for finite sources.')])]
def pages(kind):
 if kind<5:
  title,label,e,v,variables,other=FINAL[kind]
  return[('Final field',label+'='+e),('Final potential','V='+v),('Variables / conditions',variables),('Other final results',other)]
 return EXTRA[kind-5][1]
def catalog():
 from APDATA import titles,row
 units=['Charge / fields / Gauss','Electric potential','Conductors / capacitors','Electric circuits','Magnetic fields','Induction / RL / LC']
 while True:
  unit=menu('E&M final formulas',units)
  if unit<0:return
  name='APU%02d'%(unit+8);mod=__import__(name)
  try:
   while True:
    i=menu(units[unit],titles(mod.DATA))
    if i<0:break
    title,eq,names,domains,note,methods=row(mod.DATA,i).split('|')
    cards(title,[(title,eq),('Conditions',note)])
  finally:
   mod=None;release([name])
def show(kind=None):
 if kind is not None:cards(FINAL[kind][0],pages(kind));return
 labels=[f[0]for f in FINAL]+[f[0]for f in EXTRA]+['All other E&M equations']
 while True:
  i=menu('FINAL FORMULAS',labels)
  if i<0:return
  if i==len(labels)-1:catalog()
  else:cards(labels[i],pages(i))
