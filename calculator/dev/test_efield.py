import sys,math,unittest,io,contextlib,types,importlib,ast
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'EField_EM/TRANSFER'))
import EFMODEL as F
from APNUM import integrate,derivative

class Fields(unittest.TestCase):
 def near(self,a,b): self.assertLessEqual(abs(a-b),2e-7*max(abs(b),1e-285))
 def test_ring_independent_quadrature(self):
  for q,r,x in [(1e-9,.3,.7),(-3e-9,2,-1),(3,.4,0)]:
   lam=q/(2*math.pi*r)
   e=integrate(lambda t:F.K*lam*r*x/(r*r+x*x)**1.5,0,2*math.pi,80)
   self.near(F.field(0,q,r,x)[0],e)
 def test_rod_independent_quadrature(self):
  for q,l,x in [(1e-9,.5,.3),(-3e-9,2,4),(1,.4,-.5)]:
   lam=q/l
   self.near(F.field(1,q,l,x)[0],integrate(lambda y:F.K*lam*x/(x*x+y*y)**1.5,-l/2,l/2,160))
   if x>0:self.near(F.field(2,q,l,x)[0],integrate(lambda t:F.K*lam/t**2,x,x+l,160))
 def test_trig_endpoints_and_half_length(self):
  q,l,x=2e-9,3,.7
  self.near(F.field(1,q,l,x)[0],2*F.K*q/l/x*math.sin(math.atan(l/(2*x))))
  r=l/2
  self.near(F.field(1,q,l,r)[0],F.K*q/(math.sqrt(2)*r*r))
 def test_limits_symmetry_and_point_charge(self):
  q,r=2e-9,.7
  self.assertEqual(F.field(0,q,r,0)[0],0)
  self.near(F.field(0,q,r,r)[0],F.K*q/(2*math.sqrt(2)*r*r))
  self.near(F.field(0,q,r,-r)[0],-F.field(0,q,r,r)[0])
  for k in [0,1,2]:
   x=1e8*r
   self.assertLess(abs(F.field(k,q,r,x)[0]/(F.K*q/x**2)-1),1e-7)
  x=1e-7*r
  self.assertLess(abs(F.field(1,q,r,x)[0]/(2*F.K*(q/r)/x)-1),1e-7)
  self.assertLess(abs(F.field(2,q,r,x)[0]/(F.K*(q/r)/x)-1),2e-7)
 def test_ring_derivative_extrema_potential(self):
  q,r=2e-9,.7
  xp=r/math.sqrt(2);top=2*F.K*q/(3*math.sqrt(3)*r*r)
  self.near(F.field(0,q,r,xp)[0],top)
  self.assertGreater(derivative(lambda x:F.field(0,q,r,x)[0],xp*.9,r*1e-4),0)
  self.assertLess(derivative(lambda x:F.field(0,q,r,x)[0],xp*1.1,r*1e-4),0)
  for kind in range(4):
   x=1.2*r
   self.near(-derivative(lambda y:F.field(kind,q,r,y)[1],x,r*1e-4),F.field(kind,q,r,x)[0])
 def test_ring_two_roots_and_peak(self):
  q,r=3e-9,.2
  peak=r/math.sqrt(2);top=F.field(0,q,r,peak)[0]
  roots=F.ring_distances(q,r,top*.4)
  self.assertEqual(len(roots),2);self.assertLess(roots[0],peak);self.assertGreater(roots[1],peak)
  for x in roots:self.near(F.field(0,q,r,x)[0],top*.4)
  self.near(F.ring_distances(q,r,top)[0],peak)
  self.assertEqual(F.ring_distances(q,r,0),[0])
  for target in [-top,top*2]:
   with self.assertRaises(ValueError):F.ring_distances(q,r,target)
 def test_inverse_distances(self):
  for kind in [1,2,3]:
   for q,d,x in [(2e-9,.5,.7),(-2e-9,.5,1e-5)]:
    self.near(F.inverse_distance(kind,q,d,F.field(kind,q,d,x)[0]),x)
 def test_arc_components_and_constraints(self):
  q,r=2e-9,.4
  self.assertEqual(F.field(4,q,r,0,2*math.pi)[0],0)
  self.near(F.arc_components(q,r,math.pi,math.pi)[0],2*F.K*q/(math.pi*r*r))
  ex,ey,v=F.arc_components(q,r,math.pi/2,math.pi/4)
  self.near(ex,-2*F.K*q/(math.pi*r*r));self.near(ey,ex)
  # At fixed Q smaller sweep has a stronger field; at fixed lambda peak is pi.
  self.assertGreater(F.field(4,q,r,0,.1)[0],F.field(4,q,r,0,math.pi)[0])
  lam=1e-9
  def byphi(phi):return F.field(4,lam*r*phi,r,0,phi)[0]
  self.assertGreater(byphi(math.pi),byphi(math.pi*.9))
  self.assertGreater(byphi(math.pi),byphi(math.pi*1.1))
 def test_two_ring_reference_answer(self):
  z=F.two_ring_ratio(1,1,1,2)
  self.near(z,2**2.5/5**1.5)
  self.assertLess(abs(F.field(0,z,1,1)[0]+F.field(0,1,1,-2)[0]),1e-6)
 def test_domains(self):
  for kind in [1,2,3]:
   with self.assertRaises(ValueError):F.field(kind,1,1,0)
  with self.assertRaises(ValueError):F.field(4,1,1,0,7)
 def test_notes_all_five_cases(self):
  for n in range(5):
   mod=importlib.import_module('EFN'+str(n))
   cards=[s.split('|',1) for s in mod.DATA.split('\n')]
   self.assertTrue(all(len(c)==2 for c in cards));self.assertGreaterEqual(len(cards),5)
  self.assertIn('R/sqrt(2)',importlib.import_module('EFN0').DATA)
  self.assertIn('L/2',importlib.import_module('EFN1').DATA)
  self.assertIn('FIXED',importlib.import_module('EFN4').DATA.upper())
 def test_no_mechanics_and_ti_syntax(self):
  dest=ROOT/'EField_EM/TRANSFER'
  self.assertFalse(any((dest/('APU%02d.py'%i)).exists() for i in range(1,8)))
  for p in dest.glob('*.py'):
   self.assertLessEqual(len(p.stem),8)
   tree=ast.parse(p.read_text('ascii'))
   for node in ast.walk(tree):
    if isinstance(node,ast.Attribute):self.assertNotIn(node.attr,['isalnum','isdigit','isalpha'])
  self.assertNotIn('Mechanics',(dest/'APC.py').read_text())
 def test_import_style_startup(self):
  import runpy
  for name in ['EFIELD','APC']:
   out=io.StringIO()
   with patch('builtins.input',return_value='0'),contextlib.redirect_stdout(out):runpy.run_path(str(ROOT/'EField_EM/TRANSFER'/(name+'.py')),run_name=name)
   self.assertIn('E-FIELD' if name=='EFIELD' else 'E&M',out.getvalue())
 def test_graphics_contract(self):
  import EFGUI
  calls=[];mod=types.ModuleType('ti_draw')
  for n in ['clear','set_color','fill_rect','draw_text','show_draw']:
   setattr(mod,n,lambda *a,k=n:calls.append((k,a)))
  EFGUI.GRAPHICS[0]=True
  with patch.dict(sys.modules,{'ti_draw':mod}),patch.object(EFGUI,'event',return_value='enter'):
   EFGUI.cards('Test',[('1 Geometry','An example field guide card.')])
  self.assertEqual(calls[0][0],'clear');self.assertFalse(any(n=='show_draw' for n,a in calls))
  self.assertTrue(any(n=='fill_rect' for n,a in calls))
 def test_full_ring_calculation_menu(self):
  import EFCALC,EFGUI
  EFGUI.GRAPHICS[0]=False
  # R=1, total Q=1e-9, x=1; exit result cards after viewing first, then back.
  out=io.StringIO()
  with patch('builtins.input',side_effect=['1','1','1e-9','1','','0','0']),contextlib.redirect_stdout(out):EFCALC.calculate(0)
  self.assertIn('E N/C',out.getvalue())

class FinalFormulas(unittest.TestCase):
 def test_model_equations_match_solvers(self):
  import EFFINAL as A
  from APCORE import calc
  for kind,item in enumerate(A.FINAL):
   for q in [1e-9,-2e-9]:
    d=1.7;x=.8;phi=math.pi/2
    values={'k':F.K,'Q':q,'lam':q,'R':d,'L':d,'x':x,'phi':phi}
    e,v=F.field(kind,q,d,x,phi)
    self.assertAlmostEqual(calc(item[2],values),e,places=10)
    self.assertAlmostEqual(calc(item[3],values),v,places=10)
 def test_two_ring_reference_formula(self):
  import EFFINAL as A
  from APCORE import calc
  text=A.EXTRA[0][1][1][1]
  expression=text.split('Q1/Q2=')[1].split('=')[0]
  self.assertAlmostEqual(calc(expression),F.two_ring_ratio(1,1,1,2),places=12)
 def test_all_formula_cards_preserve_complete_text(self):
  import EFFINAL as A,EFGUI as U
  for i in range(len(A.FINAL)+len(A.EXTRA)):
   for title,body in A.pages(i):
    seen=[]
    def paint(title,lines,page,total,**kw):
     self.assertLessEqual(len(lines),5)
     self.assertTrue(all(len(line)<=28 for line in lines));seen.extend(lines)
    with patch.object(U,'frame',side_effect=paint),patch.object(U,'event',return_value='next'):
     U.cards(title,[(title,body)])
    self.assertEqual(''.join(body.split()),''.join(''.join(seen).split()))
 def test_read_only_em_catalog_covers_every_entry(self):
  import EFFINAL as A,APDATA
  expected=[];choices=[]
  for unit in range(8,14):
   data=importlib.import_module('APU%02d'%unit).DATA
   count=len(APDATA.titles(data));choices.append(unit-8)
   for i in range(count):
    row=APDATA.row(data,i).split('|');expected.append((row[0],row[1],row[4]));choices.append(i)
   choices.append(-1)
  choices.append(-1);seen=[]
  with patch.object(A,'menu',side_effect=choices),patch.object(A,'cards',side_effect=lambda title,pages:seen.append((title,pages[0][1],pages[1][1]))),patch('builtins.input',side_effect=AssertionError('Formula browser must not ask for values')):
   A.catalog()
  self.assertEqual(seen,expected)
 def test_each_model_has_final_formula_shortcut(self):
  import EFAPP
  for kind in range(5):
   A=importlib.import_module('EFFINAL');seen=[]
   with patch.object(EFAPP,'menu',side_effect=[kind,6,-1,-1]),patch.object(A,'cards',side_effect=lambda title,pages:seen.append((title,pages))),patch('builtins.input',side_effect=AssertionError('Formula shortcut must not ask for values')):
    EFAPP.main()
   self.assertEqual(seen,[(A.FINAL[kind][0],A.pages(kind))])
 def test_studio_has_standalone_final_formula_section(self):
  import EFAPP
  A=importlib.import_module('EFFINAL')
  with patch.object(EFAPP,'menu',side_effect=[5,-1]) as menu,patch.object(A,'show') as show:
   EFAPP.main()
  show.assert_called_once_with();self.assertEqual(menu.call_args_list[0].args[1][5],'Final formulas')
 def test_apc_has_standalone_final_formula_section(self):
  import APCORE,runpy
  A=importlib.import_module('EFFINAL')
  with patch.object(APCORE,'menu',side_effect=[1,-1]) as menu,patch.object(A,'show') as show:
   runpy.run_path(str(ROOT/'EField_EM/TRANSFER/APC.py'),run_name='APC')
  show.assert_called_once_with();self.assertEqual(menu.call_args_list[0].args[1][1],'Final formulas')

class Navigation(unittest.TestCase):
 def test_evo_highlight_covers_selected_glyphs(self):
  import EFGUI as U
  # A physical Evo capture places glyph tops 18 pixels above draw_text y.
  # Check actual selection frames, including wrapped entries and page changes.
  calls=[];module=types.ModuleType('ti_draw')
  for name in ['clear','set_color','fill_rect','draw_text']:
   setattr(module,name,lambda *args,k=name:calls.append((k,args)))
  keys=iter(['down','down','down','down','down','up','enter'])
  frames=[];real_frame=U.frame
  def record(title,lines,page,total,highlight=None,**kwargs):
   calls.clear();real_frame(title,lines,page,total,highlight,**kwargs)
   boxes=[a for k,a in calls if k=='fill_rect' and a[0]==4]
   self.assertEqual(len(boxes),1)
   x,y,w,h=boxes[0];selected=highlight[0];count=highlight[1]
   body=[a for k,a in calls if k=='draw_text' and a[2] in lines]
   self.assertEqual(len(body),len(lines))
   for row,(_,baseline,label) in enumerate(body):
    top=baseline-18;bottom=baseline-1
    if selected<=row<selected+count:
     self.assertGreaterEqual(top,y);self.assertLess(bottom,y+h)
    else:self.assertTrue(bottom<y or top>=y+h)
   frames.append((page,selected,count))
  saved=U.GRAPHICS[0];U.GRAPHICS[0]=True
  try:
   with patch.dict(sys.modules,{'ti_draw':module}),patch.object(U,'event',side_effect=lambda:next(keys)),patch.object(U,'frame',side_effect=record):
    U.choose('Alignment',['Ring','Rod: perpendicular bisector','Beyond end','Infinite line','Arc','Another model'])
   self.assertTrue(any(count==2 for page,start,count in frames))
   self.assertTrue(any(page==1 for page,start,count in frames))
  finally:U.GRAPHICS[0]=saved
 def test_evo_raw_codes_through_menu(self):
  import EFGUI as U
  module=types.ModuleType('ti_system');values=iter([0,34,34,105])
  module.get_key=lambda wait:next(values)
  with patch.dict(sys.modules,{'ti_system':module}),patch.object(U,'frame'):
   self.assertEqual(U.choose('Evo',['Ring','Rod','Line']),2)
  raw=[25,34,24,26,105,45,92,93,94,82,83,73,74,102]
  self.assertEqual([U.key_action(k) for k in raw],['up','down','prev','next','enter','back','1','2','3','4','5','prev','next','back'])
 def test_evo_get_key_and_unknown_keys(self):
  import EFGUI as U
  module=types.ModuleType('ti_system');values=iter([0,999,None,'',25])
  calls=[]
  module.get_key=lambda wait:(calls.append(wait) or next(values))
  module.wait_key=lambda:self.fail('Evo get_key must be preferred')
  with patch.dict(sys.modules,{'ti_system':module}):self.assertEqual(U.event(),'up')
  self.assertEqual(calls,[1]*5)
 def test_hardware_calibration_overrides_and_launches(self):
  import EFGUI as U,EFAPP,runpy
  # Deliberately use codes unrelated to either default map. The learned map
  # must drive a real menu before opening the studio in the same session.
  values=iter([501,502,503,504,505,506,502,505])
  module=types.ModuleType('ti_system');module.get_key=lambda wait:next(values)
  saved=dict(U.KEYMAP);launched=[]
  try:
   with patch.dict(sys.modules,{'ti_system':module}),patch.object(U,'frame'),patch('builtins.input',return_value=''),patch.object(EFAPP,'main',side_effect=lambda:launched.append(dict(U.KEYMAP))),contextlib.redirect_stdout(io.StringIO()) as output:
    runpy.run_path(str(ROOT/'EField_EM/TRANSFER/EFKEY.py'),run_name='EFKEY')
   self.assertEqual(launched,[{501:'up',502:'down',503:'prev',504:'next',505:'enter',506:'back'}])
   self.assertIn('PASS: hardware navigation',output.getvalue())
  finally:U.KEYMAP.clear();U.KEYMAP.update(saved)
 def test_string_key_events(self):
  import EFGUI as U
  module=types.ModuleType('ti_system');values=iter(['up','down','left','right','enter','esc','1'])
  module.get_key=lambda wait:next(values)
  with patch.dict(sys.modules,{'ti_system':module}):self.assertEqual([U.event() for _ in range(7)],['up','down','prev','next','enter','back','1'])
 def test_key_mapping(self):
  import EFGUI as U
  raw=[14,15,3,4,13,9,243,244,245,246,247,250,251,62]
  module=types.ModuleType('ti_system');values=iter(raw);module.wait_key=lambda:next(values)
  with patch.dict(sys.modules,{'ti_system':module}):
   self.assertEqual([U.event() for _ in raw],['prev','next','up','down','enter','back','1','2','3','4','5','prev','next','back'])
 def test_all_guide_text_visible(self):
  import EFGUI as U
  for n in range(5):
   source=importlib.import_module('EFN'+str(n)).DATA
   for row in source.split('\n'):
    heading,body=row.split('|',1);seen=[]
    def show(title,lines,page,total,**kw):
     self.assertLessEqual(len(lines),5)
     self.assertTrue(all(len(line)<=28 for line in lines))
     seen.extend(lines)
    with patch.object(U,'frame',side_effect=show),patch.object(U,'event',return_value='next'):
     U.cards(heading,[(heading,body)])
    self.assertEqual(''.join(body.split()),''.join(''.join(seen).split()))
 def test_arrow_selection_and_back(self):
  import EFGUI as U
  for keys,expected in [(['down']*7+['enter'],7),(['prev','enter'],5),(['up','enter'],9),(['back'],-1)]:
   with patch.object(U,'frame'),patch.object(U,'event',side_effect=keys):self.assertEqual(U.choose('Test',['Item '+str(i) for i in range(10)]),expected)
  seen=[]
  with patch.object(U,'frame',side_effect=lambda t,l,p,n,**k:seen.append(p)),patch.object(U,'event',side_effect=['next','next','prev','back']):U.cards('Guide',[('Heading','word '*100)])
  self.assertEqual(seen,[0,1,2,1])
 def test_all_six_em_unit_menus(self):
  import runpy
  from APCORE import menu
  with patch('builtins.input',return_value='0'),contextlib.redirect_stdout(io.StringIO()):env=runpy.run_path(str(ROOT/'EField_EM/TRANSFER/APC.py'),run_name='APC')
  fn=env['unit_ui'];seen=[]
  fn.__globals__['menu']=lambda title,items:(seen.append(title) or -1)
  for unit in range(8,14):fn(unit)
  self.assertEqual(seen,['Charge / fields / Gauss','Electric potential','Conductors / capacitors','Electric circuits','Magnetic fields','Induction / RL / LC'])

class Workflow(unittest.TestCase):
 def test_complete_arrow_key_ring_flow(self):
  import EFGUI as U,EFAPP,APCORE as C
  events=iter(['enter','enter','enter','back','back','back','back'])
  frames=[]
  def paint(title,lines,page,total,*args,**kw):frames.append((title,lines))
  with patch.object(U,'event',side_effect=lambda:next(events)),patch.object(U,'frame',side_effect=paint),patch('builtins.input',side_effect=['1','1e-9','1']),contextlib.redirect_stdout(io.StringIO()):EFAPP.main()
  self.assertTrue(any(t=='Substitute SI values' for t,lines in frames))
  self.assertAlmostEqual(C.LAST[0],F.K*1e-9/(2**1.5),places=8)
 def test_all_reference_menu_labels_preserved(self):
  import APDATA,EFGUI as U
  for unit in range(8,14):
   mod=importlib.import_module('APU%02d'%unit)
   labels=APDATA.titles(mod.DATA)
   pages=U.menu_pages(labels)
   shown={i:[] for i in range(len(labels))}
   for page in pages:
    self.assertLessEqual(sum(len(parts) for i,parts in page),5)
    for index,parts in page:
     self.assertTrue(all(len(line)<=26 for line in parts));shown[index]+=parts
   for i,label in enumerate(labels):self.assertEqual(''.join(label.split()),''.join(''.join(shown[i]).split()))

if __name__=='__main__':unittest.main(verbosity=2)
