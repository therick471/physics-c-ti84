from math import sqrt
from APCORE import fmt
from EFINPUT import parameters
from EFMODEL import field
from EFGUI import cards
def extrema(kind):
 q,d,phi=parameters(kind)
 if q==0:
  cards('Extrema',[('Zero source','E and V are zero wherever the model is defined. Extrema are not unique.')]);return
 if kind==0:
  xp=d/sqrt(2)
  peak=abs(field(0,q,d,xp)[0])
  text='x_peak=R/sqrt(2)='+fmt(xp)+' m. Max |E|='+fmt(peak)+' N/C. Emax=2*k*abs(Q)/(3*sqrt(3)*R^2). Both +x_peak and -x_peak maximize |E|. For Q>0 signed E has max at +x_peak, min at -x_peak; Q<0 swaps them. Min |E|=0 at x=0; infinity is a limit, not a finite root.'
 elif kind in(1,2,3):text='On x>0, |E| decreases strictly from infinity to 0. There is no finite global maximum or attained minimum. At infinity the infimum is zero. Fix Q (or lambda) and size when comparing x. Limits and derivatives are in the full guide.'
 else:text='Vary phi at FIXED lambda: |E|=2*k*abs(lambda)*sin(phi/2)/R. Maximum at phi=pi (180 deg); full ring phi=2*pi gives zero. At FIXED Q: |E|=k*abs(Q)/R^2 *sin(phi/2)/(phi/2), decreases for 0<phi<=2*pi. Its supremum k*abs(Q)/R^2 is approached as phi->0; no finite positive-phi maximum. Do not mix fixed-Q and fixed-lambda comparisons.'
 cards('Extrema',[('Maxima / minima',text),('At x=R (ring), L (rod)','E(size)='+fmt(field(kind,q,d,d,phi)[0])+' N/C; V(size)='+fmt(field(kind,q,d,d,phi)[1])+' V.' if kind!=4 else 'Arc-center model has no observation x. Use ring-axis mode for axial x limits. Here R is the arc radius, not distance from its center.')])
