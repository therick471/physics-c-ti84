from APCORE import menu,number,info
from EFINPUT import parameters
from EFMODEL import field,NAMES
def plot(kind):
 if kind==4:info('Arc plot','Use custom f(x)=sin(x/2) for fixed density or sin(x/2)/(x/2) for fixed charge; x is sweep in radians, 0<x<=2*pi.');return
 q,d,phi=parameters(kind)
 which=menu('Vertical axis',['Signed E','Magnitude |E|','Potential V'])
 if which<0:return
 lo,hi=number('LOW x'),number('HIGH x')
 from APGRAPH import draw,samples
 def f(x):
  e,v=field(kind,q,d,x)
  return e if which==0 else(abs(e)if which==1 else v)
 seg=[]
 if kind in(1,3)and lo<0<hi:
  gap=max(abs(lo),abs(hi))*1e-6
  seg=samples(f,lo,-gap,20)+samples(f,gap,hi,20)
 else:seg=samples(f,lo,hi,40)
 draw(['Ring axis','Rod bisector','Rod beyond end','Infinite line'][kind],[('field',seg)],'x m','V' if which==2 else 'E N/C')
