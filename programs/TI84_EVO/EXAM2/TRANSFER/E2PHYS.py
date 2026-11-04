from math import sqrt,pi,cos
from APCORE import CONST
K=CONST['ke']
EP=CONST['eps0']
def sphere(q,R,r,kind):
 if R<=0 or r<0:raise ValueError('R>0 and r>=0')
 if r<R:
  if kind==0:return K*q*r/R**3,K*q*(3-r*r/R**2)/(2*R),q*(r/R)**3
  return 0.0,K*q/R,0.0
 return K*q/r**2,K*q/r,q
def cylinder(rho,R,r):
 if R<=0 or r<0:raise ValueError('R>0 and r>=0')
 return rho*r/(2*EP) if r<=R else rho*R*R/(2*EP*r)
def power_sphere(alpha,n,R,r):
 if n<0 or n!=int(n):raise ValueError('Use integer n>=0')
 if R<=0 or r<0:raise ValueError('R>0 and r>=0')
 enc=4*pi*alpha*min(r,R)**(n+3)/(n+3)
 return (0.0 if r==0 else K*enc/r**2),enc
def point_sum(sources,x,y):
 ex=ey=v=0.0
 for q,a,b in sources:
  dx=x-a;dy=y-b;rs=dx*dx+dy*dy
  if rs==0:raise ValueError('Point coincides with source')
  r=sqrt(rs);ex+=K*q*dx/(rs*r);ey+=K*q*dy/(rs*r);v+=K*q/r
 return ex,ey,v
def assembly(sources):
 u=0.0
 for i in range(len(sources)):
  q,x,y=sources[i]
  for j in range(i):
   a,b,c=sources[j];r=sqrt((x-b)**2+(y-c)**2)
   if r==0:raise ValueError('Sources coincide')
   u+=K*q*a/r
 return u
def zero_field(q1,q2,d):
 if q1==0 or q2==0 or d<=0:raise ValueError('Nonzero charges, d>0')
 a=sqrt(abs(q1));b=sqrt(abs(q2))
 if q1*q2>0:return d*a/(a+b)
 if a==b:return None
 return d*a/(a-b)
def energy(q,dv,m,vi):
 if m<=0 or vi<0:raise ValueError('m>0; speed>=0')
 du=q*dv;kf=.5*m*vi*vi-du
 if kf<0:raise ValueError('Not reachable with this initial energy')
 return du,-du,kf,sqrt(2*kf/m)
def uniform(e,d,deg):return -e*d*cos(deg*pi/180)
def flat_flux(e,a,deg):
 if a<0:raise ValueError('Area>=0')
 return e*a*cos(deg*pi/180)
