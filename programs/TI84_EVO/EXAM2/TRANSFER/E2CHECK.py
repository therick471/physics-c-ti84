def run():
 from math import pi
 import E2PHYS as p
 from APCORE import info
 def near(a,b):
  if abs(a-b)>1e-8*max(abs(b),1e-25):raise ValueError('Self-check mismatch')
 near(p.zero_field(4e-9,1e-9,.3),.2)
 near(p.zero_field(4e-9,-1e-9,.3),.6)
 near(p.sphere(2e-9,2,1,0)[0],p.K*2e-9/8)
 near(p.sphere(2e-9,2,0,1)[1],p.K*1e-9)
 near(p.cylinder(2e-9,2,4),2e-9/(2*p.EP))
 near(p.power_sphere(2e-9,1,2,1)[1],pi*2e-9)
 near(p.assembly([(1,0,0),(1,1,0),(-1,.5,3**.5/2)]),-p.K)
 near(p.energy(2e-6,-50,1,0)[0],-1e-4)
 near(p.flat_flux(2,3,60),3)
 near(p.uniform(20,3,0),-60)
 ex,ey,v=p.point_sum([(2e-9,-.3,0),(-2e-9,.3,0)],0,0)
 near(ex,2*p.K*2e-9/.09);near(ey,0);near(v,0)
 info('EXAM 2 CHECK','PASS: Exam 2 physics checks. This does not test every key, graph or device memory condition. Launch EXAM2 for the new hub.')
