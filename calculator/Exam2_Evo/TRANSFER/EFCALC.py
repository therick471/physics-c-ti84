from math import pi
from APCORE import menu,number,result,fmt,LAST
from EFNOTE import guide
from EFINPUT import parameters
from EFMODEL import field,arc_components
from EFGUI import cards
def calculate(kind):
 q,d,phi=parameters(kind)
 x=0 if kind==4 else number('x m','+' if kind==2 else 's')
 e,v=field(kind,q,d,x,phi)
 pairs=[('lambda C/m' if kind==3 else 'Q C',q),('E N/C',e),('|E| N/C',abs(e)),('V volts',v)]
 if kind!=3:pairs.insert(1,('lambda C/m',q/(2*pi*d if kind==0 else(d*phi if kind==4 else d))))
 if kind==4:
  mid=number('Arc midpoint angle deg','s',180)*pi/180
  ex,ey,v=arc_components(q,d,phi,mid)
  pairs=[('Ex N/C',ex),('Ey N/C',ey),('|E| N/C',abs(e)),('V volts',v)]
 LAST[0]=abs(e)if kind==4 else e
 cards('Solution',[('Substitute SI values','\n'.join(n+' = '+fmt(v)for n,v in pairs)),('Direction / units','E is signed along the positive observation axis; negative Q reverses it. For an arc, Ex/Ey use the entered midpoint angle. F=q_test*E; U=q_test*V. N/C=V/m. V(infinity)=0 for finite distributions. Infinite line uses V(R)=0.')])
 next_action=menu('Continue',['Full start-to-finish guide','Force on test charge'])
 if next_action<0:return
 if next_action==0:guide(kind)
 else:
  test=number('Test charge C')
  if kind==4:result('Test charge',[('Fx N',test*ex),('Fy N',test*ey),('U J',test*v)])
  else:result('Test charge',[('F N',test*e),('U J',test*v)])
