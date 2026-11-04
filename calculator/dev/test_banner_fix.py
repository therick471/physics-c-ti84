import sys,types,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Exam2_Evo/TRANSFER'))
import EFGUI as U
class Layout(unittest.TestCase):
 def test_banner_and_bounds(self):
  calls=[];d=types.ModuleType('ti_draw')
  for name in ['clear','set_color','fill_rect','draw_text','draw_line','fill_circle','show_draw']:
   setattr(d,name,lambda *a,k=name:calls.append((k,a)))
  with patch.dict(sys.modules,{'ti_draw':d}):
   for count in [1,2,3,4]:
    for index in range(count):
     calls.clear();U.frame('Two line heading for testing',['Row '+str(i) for i in range(count)],0,1,(index,1))
     text=[a for k,a in calls if k=='draw_text']
     for x,y,t in text:
      if t:self.assertGreaterEqual(y-U.TEXT_ASCENT,U.SAFE_TOP)
      self.assertLessEqual(y,209);self.assertLessEqual(x+len(t)*10,320)
     boxes=[a for k,a in calls if k=='fill_rect' and a[0]==4];x,y,w,h=boxes[0]
     baseline=U.BODY_Y+index*U.LINE_STEP
     self.assertGreaterEqual(baseline-18,y);self.assertLess(baseline,y+h)
    self.assertLess(U.TITLE_Y+18,U.BODY_Y-18)
    self.assertLess(U.BODY_Y+(U.ROWS-1)*U.LINE_STEP,186-18)
   for kind in [0,1]:
    calls.clear();U.sketch(kind)
    for k,a in calls:
     if k=='draw_text':self.assertGreaterEqual(a[1]-18,U.SAFE_TOP);self.assertLessEqual(a[1],209)
 def test_page_navigation_preserves_text(self):
  import E2NOTES as N
  for title,steps in N.GROUPS:
   seen=[]
   def frame(t,lines,p,total,**kw):
    self.assertLessEqual(len(lines),4);seen.extend(lines)
   with patch.object(U,'frame',side_effect=frame),patch.object(U,'event',return_value='next'):U.cards(title,steps)
   self.assertEqual(''.join(''.join(seen).split()),''.join(''.join(b for h,b in steps).split()))
if __name__=='__main__':unittest.main(verbosity=2)
