import sys,math,unittest,ast,io,contextlib,runpy,importlib
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]/'Exam2_Evo/TRANSFER'
sys.path.insert(0,str(ROOT))
import E2PHYS as P
import EFGUI as U
import E2CALC as C
class Exam(unittest.TestCase):
 def near(self,a,b):self.assertAlmostEqual(a/b,1,places=7) if b else self.assertEqual(a,0)
 def test_spheres(self):
  for q in [2e-9,-3e-8,0]:
   for r in [0,.1,1,2,10]:
    e,v,enc=P.sphere(q,1,r,0)
    self.near(enc,q*min(r,1)**3)
    if r:self.near(e,P.K*enc/r**2)
    if 0<r<1:
     h=1e-5;dv=(P.sphere(q,1,r+h,0)[1]-P.sphere(q,1,r-h,0)[1])/(2*h)
     self.assertAlmostEqual(e,-dv,places=5)
   self.near(P.sphere(q,1,.5,1)[0],0)
   self.near(P.sphere(q,1,.5,1)[1],P.K*q)
 def test_nonuniform_quadrature(self):
  for n in [0,1,2,6]:
   for r in [0,.3,1,3]:
    e,q=P.power_sphere(2e-9,n,1,r);a=min(r,1);steps=4000;dx=a/steps
    numeric=sum(4*math.pi*2e-9*((i+.5)*dx)**(n+2)*dx for i in range(steps))
    self.assertLess(abs(q-numeric),1e-13)
    if r:self.near(e,P.K*q/r**2)
 def test_cylinder(self):
  self.near(P.cylinder(1,2,0),0)
  self.near(P.cylinder(1,2,2),1/P.EP)
  self.near(P.cylinder(1,2,4),.5/P.EP)
 def test_cancellation(self):
  for a,b in [(4,1),(1,4),(4,-1),(1,-4),(-4,-1)]:
   x=P.zero_field(a,b,3);ex,_,_=P.point_sum([(a,0,0),(b,3,0)],x,0)
   self.assertLess(abs(ex),1e-4)
  self.assertIsNone(P.zero_field(1,-1,3))
 def test_energy_assembly_flux(self):
  self.near(P.assembly([(1,0,0),(1,1,0),(-1,.5,math.sqrt(3)/2)]),-P.K)
  du,w,k,v=P.energy(-P.CONST['qe'],200,P.CONST['me'],0)
  self.near(k,200*P.CONST['qe']);self.near(.5*P.CONST['me']*v*v,k)
  self.near(P.flat_flux(20,3,60),30);self.near(P.uniform(20,3,180),60)
 def test_bad_inputs(self):
  for fn,args in [(P.sphere,(1,0,1,0)),(P.cylinder,(1,1,-1)),(P.zero_field,(0,1,1)),(P.energy,(1,5,1,0)),(P.power_sphere,(1,-1,1,1)),(P.assembly,([(1,0,0),(2,0,0)],)),(P.point_sum,([(1,0,0)],0,0))]:
   with self.assertRaises(ValueError):fn(*args)
 def test_all_new_solver_paths(self):
  cases=[('gauss',0,[2e-9,1,.5],[]),('gauss',1,[2e-9,1,.5],[]),('gauss',2,[2e-9,1,.5],[]),('gauss',3,[2e-9,.5],[]),('gauss',4,[2e-9],[0]),('gauss',4,[2e-9],[1]),('gauss',4,[2e-9],[2]),('gauss',5,[2e-9,1,.5],[1]),('gauss',6,[3e-9],[]),('gauss',7,[20,3,60],[]),('work',0,[-1e-9,200,1,0],[]),('work',1,[20,3,180,1e-9],[]),('work',2,[1,0,0,1,1,0],[2]),('work',3,[4e-9,1e-9,.3],[]),('work',3,[1,-1,1],[]),('work',4,[8e-9,-2e-9],[2])]
  for name,i,nums,ints in cases:
   seen=[]
   with patch.object(C,'number',side_effect=nums),patch.object(C,'integer',side_effect=ints),patch.object(C,'menu',side_effect=ints),patch.object(C,'info'),patch.object(C,'result',side_effect=lambda *args:seen.append(args)):
    getattr(C,name)(i)
   if not(name=='work' and i==3 and nums[0]==1):self.assertTrue(seen,(name,i))
 def test_cards_fit_and_all_text_survives(self):
  import E2NOTES as N
  for title,steps in N.GROUPS:
   self.assertLessEqual(len(U.wrap_at(title)),2)
   seen=[]
   def frame(t,lines,p,n,**kw):
    self.assertLessEqual(len(lines),5);self.assertTrue(all(len(x)<=28 for x in lines));seen.extend(lines)
   with patch.object(U,'frame',side_effect=frame),patch.object(U,'event',return_value='next'):U.cards(title,steps)
   self.assertEqual(''.join(''.join(seen).split()),''.join(''.join(b for h,b in steps).split()))
 def test_launcher_routing(self):
  import E2APP as A
  with patch.object(A,'menu',side_effect=[1,-1,-1]),patch.object(A,'release'):A.main()
  with patch('APCORE.menu',side_effect=[0,-1]),patch.object(A,'main') as main,patch('APMEM.release'):
   runpy.run_path(str(ROOT/'APC.py'),run_name='__main__');main.assert_called_once()
 def test_device_check(self):
  import E2CHECK
  with patch('APCORE.info') as msg:E2CHECK.run();self.assertIn('PASS',msg.call_args[0][1])
 def test_sources(self):
  for f in ROOT.glob('*.py'):
   ast.parse(f.read_text());self.assertLess(len(f.read_bytes()),16000);f.read_text().encode('ascii')
if __name__=='__main__':unittest.main(verbosity=2)
