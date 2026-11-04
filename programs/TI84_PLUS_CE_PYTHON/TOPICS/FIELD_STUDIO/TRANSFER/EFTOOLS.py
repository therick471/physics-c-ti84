from math import sqrt,pi
from APCORE import menu,number,integer,info,result,calc,fmt,Cancel,error
from EFMODEL import K,field,arc_components,two_ring_ratio
from EFGUI import cards
def rings(which):
 if which==0:
  r1,r2=number('Ring1 R m','+'),number('Ring2 R m','+')
  a,b=number('P distance to ring1 m','+'),number('P distance to ring2 m','+')
  z=two_ring_ratio(r1,r2,a,b)
  cards('Cancel at P',[('1 Directions','P lies BETWEEN the rings. The fields oppose only if the charges have the SAME sign.'),('2 Set magnitudes equal','k*Q1*a/(R1^2+a^2)^(3/2) = k*Q2*b/(R2^2+b^2)^(3/2).'),('3 Solve charge ratio','Q1/Q2=(b/a)*[(R1^2+a^2)/(R2^2+b^2)]^(3/2) = '+fmt(z)+'. For equal radii, a=R,b=2R: 0.505964426.')])
 else:
  total=0.0;voltage=0.0
  x=number('Observation axis x m')
  for i in range(2):
   q,r,c=number('Ring'+str(i+1)+' Q C'),number('R m','+'),number('Center x m')
   e,v=field(0,q,r,x-c);total+=e;voltage+=v
  result('Two rings',[('Net E N/C',total),('Net V volts',voltage)],'Signed axial fields add. Each ring contributes zero E at its own center. V is scalar.')
def superpose(arcs):
 ex=ey=voltage=0.0
 px,py=(0,0)if arcs else(number('Target x m'),number('Target y m'))
 n=integer('Number of arcs' if arcs else 'Point-charge count',1,20)
 for i in range(n):
  q=number('Source'+str(i+1)+' Q C')
  if arcs:
   r=number('Radius m','+')
   sweep=number('Sweep degrees','+')*pi/180
   mid=number('Arc midpoint deg')*pi/180
   a,b,v=arc_components(q,r,sweep,mid)
  else:
   x,y=number('Source x m'),number('Source y m')
   dx,dy=px-x,py-y;rr=dx*dx+dy*dy
   if rr==0:raise ValueError('Target coincides with charge')
   r=sqrt(rr);a=K*q*dx/(rr*r);b=K*q*dy/(rr*r);v=K*q/r
  ex+=a;ey+=b;voltage+=v
 result('Vector sum',[('Ex N/C',ex),('Ey N/C',ey),('|E| N/C',sqrt(ex*ex+ey*ey)),('V volts',voltage)],'Add signed vector components, not field magnitudes. Arc midpoint is measured from +x to the charged arc, counterclockwise.')
def analysis():
 from APNUM import derivative,bisect
 s=input('f(x), with R,Q allowed: ').strip()
 if s.lower()=='q':raise Cancel()
 r=number('R scale','+')
 q=number('Q parameter')
 def f(x):return calc(s,{'x':x,'R':r,'Q':q})
 mode=menu('Numerical analysis',['Limits near 0, R, infinity','Min/max on finite interval','Derivative at x','Graph f(x)'])
 if mode<0:return
 if mode==0:
  rows=[]
  for a,label in[(0,'0'),(r,'R')]:
   text=''
   for h in[.01*r,.0001*r,.000001*r]:
    for side in[-1,1]:
     try:text+=label+(' - ' if side<0 else ' + ')+fmt(h)+': '+fmt(f(a+side*h))+'\n'
     except(ValueError,ZeroDivisionError,OverflowError):text+='undefined\n'
   rows.append(('Approach '+label,text))
  text=''
  for scale in[10,100,10000]:
   for side in[-1,1]:
    x=side*scale*r
    try:text+='x='+fmt(x)+': '+fmt(f(x))+'\n'
    except(ValueError,ZeroDivisionError,OverflowError):text+='undefined\n'
  rows.append(('Infinity samples',text))
  rows.append(('Interpretation','Samples suggest behavior; they do NOT prove a limit. Compare left/right. Oscillations, poles and very slow growth can fool samples. Use the exact ring/rod guides for rigorous limits.'))
  cards('Limits',rows)
 elif mode==1:
  a,b=number('LOW x'),number('HIGH x')
  if a>=b:raise ValueError('LOW < HIGH')
  h=(b-a)*1e-5
  points=[];prev=None
  for i in range(81):
   x=a+(b-a)*i/80
   try:
    y=f(x);points.append((x,y))
    if a<x<b:
     slope=derivative(f,x,h)
     if prev and prev[1]*slope<0:
      z=bisect(lambda t:derivative(f,t,h),prev[0],x)
      if abs(derivative(f,z,h))<1e-4*max(1,abs(y)/max(h,abs(x))):points.append((z,f(z)))
     prev=(x,slope)
   except(ValueError,ZeroDivisionError,OverflowError):prev=None
  if not points:raise ValueError('No defined samples')
  lo=min(points,key=lambda t:t[1]);hi=max(points,key=lambda t:t[1])
  result('Estimated extrema',[('min x',lo[0]),('min f',lo[1]),('max x',hi[0]),('max f',hi[1])],'81 samples plus derivative-root refinement. Includes endpoints. Not certified global extrema; narrow peaks and cusps can be missed.')
 elif mode==2:
  x=number('x');h=number('positive h','+',r*1e-3)
  result('Derivative',[('df/dx',derivative(f,x,h)),('at half h',derivative(f,x,h/2))])
 else:
  from APGRAPH import draw,samples
  a,b=number('LOW x'),number('HIGH x')
  draw('Custom f(x)',[('f',samples(f,a,b,40))])
def main(custom=False):
 if custom:analysis();return
 i=menu('Superposition',['Two rings: charge ratio','Two rings: net field','Point charges in 2D','Add charged arc sectors'])
 if i<0:return
 if i<2:rings(i)
 else:superpose(i==3)
