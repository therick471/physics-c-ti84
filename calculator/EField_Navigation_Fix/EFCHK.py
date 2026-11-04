from math import sqrt,pi
from EFMODEL import K,field,arc_components,two_ring_ratio,ring_distances,inverse_distance
def check(a,b):
 if abs(a-b)>1e-6*max(abs(b),1e-290):raise ValueError('Numerical mismatch')
def main():
 print('EFIELD CHECK START v2')
 try:
  q=1e-9;r=2.0
  check(field(0,q,r,0)[0],0)
  check(field(0,q,r,r)[0],K*q/(2*sqrt(2)*r*r))
  peak=r/sqrt(2)
  top=2*K*q/(3*sqrt(3)*r*r)
  check(field(0,q,r,peak)[0],top)
  check(field(1,q,2*r,r)[0],K*q/(sqrt(2)*r*r))
  check(field(2,q,r,r)[0],K*q/(2*r*r))
  check(field(3,q,r,r)[0],2*K*q/r)
  check(field(4,q,r,0,2*pi)[0],0)
  check(arc_components(q,r,pi,pi)[0],2*K*q/(pi*r*r))
  check(two_ring_ratio(1,1,1,2),2**2.5/5**1.5)
  roots=ring_distances(q,r,top/2)
  check(field(0,q,r,roots[0])[0],top/2)
  check(field(0,q,r,roots[1])[0],top/2)
  check(inverse_distance(1,q,r,field(1,q,r,.7)[0]),.7)
  from EFGUI import wrap_at,menu_pages
  check(max(len(s)for s in wrap_at('A'*100)),28)
  check(len(menu_pages(['A','B','C','D','E','F'])),2)
  print('PASS: 12 physics + 2 UI')
  print('Restart Python; run EFIELD.')
 except Exception as e:
  print('EFIELD CHECK FAILED')
  print(str(e))
 input('ENTER to finish ')
main()
