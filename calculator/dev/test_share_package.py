"""Validate the complete handoff and the two model-specific TI API profiles."""
from pathlib import Path
import ast
import contextlib
import importlib
import io
import runpy
import sys
import types
import unittest
from unittest.mock import patch

CALC=Path(__file__).resolve().parents[1]
ROOT=CALC.parent/'Share_AP_Physics_C_EM'
PROFILES=['TI84_EVO','TI84_PLUS_CE_PYTHON']
PROGRAMS={p.stem for p in (ROOT/PROFILES[0]/'TRANSFER').glob('*.py')}

@contextlib.contextmanager
def runtime(profile):
    previous={n:sys.modules[n] for n in PROGRAMS if n in sys.modules}
    for n in PROGRAMS:sys.modules.pop(n,None)
    old_path=list(sys.path)
    sys.path.insert(0,str(ROOT/profile/'TRANSFER'))
    try:yield
    finally:
        for n in PROGRAMS:sys.modules.pop(n,None)
        sys.modules.update(previous)
        sys.path[:]=old_path

def keyboard(profile,values):
    values=iter(values);mod=types.ModuleType('ti_system')
    if profile=='TI84_EVO':mod.get_key=lambda wait:next(values)
    else:mod.wait_key=lambda:next(values)
    return mod

class SharePackage(unittest.TestCase):
    def test_complete_installations_and_legal_names(self):
        for profile in PROFILES:
            folder=ROOT/profile/'TRANSFER'
            self.assertEqual(len(list(folder.iterdir())),34)
            self.assertEqual({p.stem for p in folder.iterdir()},PROGRAMS)
            for p in folder.iterdir():
                self.assertEqual(p.suffix,'.py');self.assertLessEqual(len(p.stem),8)
                self.assertTrue(p.stem[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
                tree=ast.parse(p.read_text('ascii'))
                for node in ast.walk(tree):
                    if isinstance(node,ast.Attribute):self.assertNotIn(node.attr,['isalnum','isalpha','isdigit'])
            self.assertFalse(any((folder/('APU%02d.py'%i)).exists() for i in range(1,8)))
            self.assertFalse((folder/'APLOAD.py').exists())

    def test_solver_sources_match_verified_release(self):
        for profile in PROFILES:
            for name in PROGRAMS-{'EFGUI','EFKEY'}:
                self.assertEqual((ROOT/profile/'TRANSFER'/(name+'.py')).read_bytes(),
                                 (CALC/'EField_EM/TRANSFER'/(name+'.py')).read_bytes())
        self.assertEqual((ROOT/'TI84_EVO/TRANSFER/EFGUI.py').read_bytes(),
                         (CALC/'EField_EM/TRANSFER/EFGUI.py').read_bytes())

    def test_runtime_import_dependencies_present(self):
        builtin={'math','sys','gc','ti_system','ti_draw','ti_plotlib'}
        for profile in PROFILES:
            for p in (ROOT/profile/'TRANSFER').glob('*.py'):
                for node in ast.walk(ast.parse(p.read_text())):
                    names=[n.name for n in node.names] if isinstance(node,ast.Import) else ([node.module] if isinstance(node,ast.ImportFrom) else [])
                    for name in names:self.assertIn(name,PROGRAMS|builtin)

    def test_ce_key_codes_and_wait_key_api(self):
        with runtime('TI84_PLUS_CE_PYTHON'):
            U=importlib.import_module('EFGUI');self.assertEqual(U.TEXT_ASCENT,0)
            raw=[14,15,3,4,13,9,243,244,245,246,247,250,251,62]
            mod=keyboard('TI84_PLUS_CE_PYTHON',raw)
            mod.get_key=lambda wait:self.fail('CE profile must use documented wait_key')
            with patch.dict(sys.modules,{'ti_system':mod}):
                self.assertEqual([U.event() for _ in raw],['prev','next','up','down','enter','back','1','2','3','4','5','prev','next','back'])

    def test_evo_key_codes_and_get_key_api(self):
        with runtime('TI84_EVO'):
            U=importlib.import_module('EFGUI');self.assertEqual(U.TEXT_ASCENT,18)
            raw=[24,26,25,34,105,45,92,93,94,82,83,73,74,102]
            mod=keyboard('TI84_EVO',raw)
            mod.wait_key=lambda:self.fail('Evo get_key should be preferred')
            with patch.dict(sys.modules,{'ti_system':mod}):
                self.assertEqual([U.event() for _ in raw],['prev','next','up','down','enter','back','1','2','3','4','5','prev','next','back'])

    def test_graphic_highlight_in_each_coordinate_convention(self):
        for profile in PROFILES:
            with runtime(profile):
                U=importlib.import_module('EFGUI');d=types.ModuleType('ti_draw');calls=[]
                for name in ['clear','set_color','fill_rect','draw_text']:
                    setattr(d,name,lambda *args,k=name:calls.append((k,args)))
                for selected,count in [(0,1),(1,2),(4,1)]:
                    calls.clear()
                    with patch.dict(sys.modules,{'ti_draw':d}):
                        U.frame('Model menu',['one','two','three','four','five'],0,1,(selected,count))
                    boxes=[a for k,a in calls if k=='fill_rect' and a[0]==4]
                    self.assertEqual(len(boxes),1)
                    _,y,_,height=boxes[0]
                    ascent=18 if profile=='TI84_EVO' else 0
                    for row in range(5):
                        top=50+23*row-ascent;bottom=top+17
                        if selected<=row<selected+count:
                            self.assertGreaterEqual(top,y);self.assertLess(bottom,y+height)
                        else:self.assertTrue(bottom<y or top>=y+height)
                    self.assertFalse(any(k=='show_draw' for k,args in calls))

    def test_no_key_and_unknown_key_are_ignored(self):
        for profile in PROFILES:
            with runtime(profile):
                U=importlib.import_module('EFGUI')
                mod=keyboard(profile,[0,None,'',999,13 if profile.endswith('PYTHON') else 105])
                with patch.dict(sys.modules,{'ti_system':mod}):self.assertEqual(U.event(),'enter')

    def test_both_self_checks_pass_from_ti_style_import(self):
        for profile in PROFILES:
            for name,expected in [('EFCHK','PASS: 12 physics + 2 UI'),('APCHECK','SELF CHECK PASS')]:
                with runtime(profile),patch('builtins.input',return_value=''),contextlib.redirect_stdout(io.StringIO()) as out:
                    importlib.import_module(name)
                self.assertIn(expected,out.getvalue())
                self.assertNotIn('FAILED',out.getvalue())

    def test_calibration_and_test_menu_in_both_profiles(self):
        for profile in PROFILES:
            with runtime(profile):
                U=importlib.import_module('EFGUI');studio=importlib.import_module('EFAPP');seen=[]
                mod=keyboard(profile,[501,502,503,504,505,506,502,505])
                with patch.dict(sys.modules,{'ti_system':mod}),patch.object(U,'frame'),patch.object(studio,'main',side_effect=lambda:seen.append(dict(U.KEYMAP))),patch('builtins.input',return_value=''),contextlib.redirect_stdout(io.StringIO()) as out:
                    importlib.import_module('EFKEY')
                self.assertEqual(seen,[{501:'up',502:'down',503:'prev',504:'next',505:'enter',506:'back'}])
                self.assertIn('PASS: hardware navigation',out.getvalue())
                self.assertNotIn('EVO KEY SETUP',out.getvalue())

    def test_real_key_reader_through_ring_numeric_workflow(self):
        for profile in PROFILES:
            with runtime(profile):
                U=importlib.import_module('EFGUI');studio=importlib.import_module('EFAPP');C=importlib.import_module('APCORE');frames=[]
                enter,back=(105,45) if profile=='TI84_EVO' else (13,9)
                mod=keyboard(profile,[enter]*3+[back]*4)
                with patch.dict(sys.modules,{'ti_system':mod}),patch.object(U,'frame',side_effect=lambda title,*a,**kw:frames.append(title)),patch('builtins.input',side_effect=['1','1e-9','1']),contextlib.redirect_stdout(io.StringIO()):
                    studio.main()
                self.assertIn('Substitute SI values',frames)
                self.assertAlmostEqual(C.LAST[0],8.9875517923/(2**1.5),places=8)

    def test_graph_api_available_to_each_profile(self):
        for profile in PROFILES:
            with runtime(profile):
                G=importlib.import_module('APGRAPH');F=importlib.import_module('EFMODEL');p=types.ModuleType('ti_plotlib');calls=[]
                for name in ['cls','window','axes','grid','title','labels','pen','color','plot','show_plot']:
                    setattr(p,name,lambda *args,k=name:calls.append((k,args)))
                points=G.samples(lambda x:F.field(0,1e-9,1,x)[0],-3,3,40)
                with patch.dict(sys.modules,{'ti_plotlib':p}):G.draw('Ring axis',[('E',points)])
                self.assertTrue(any(k=='window' for k,a in calls));self.assertTrue(any(k=='plot' for k,a in calls))
                self.assertEqual(calls[-1][0],'show_plot')

    def test_handoff_instructions_are_complete_and_portable(self):
        for name in ['README.txt','README.md','QUICK_REFERENCE.txt','TROUBLESHOOTING.txt','OFFICIAL_LINKS.txt']:
            text=(ROOT/name).read_text()
            self.assertNotIn('/Users/',text);self.assertNotIn('jakerickles',text)
        readme=(ROOT/'README.txt').read_text()
        for item in ['TI84_EVO/TRANSFER','TI84_PLUS_CE_PYTHON/TRANSFER','34','EFCHK','EFKEY','APC','RAM','without Python','physical CE']:
            self.assertIn(item.lower(),readme.lower())
        for profile in PROFILES:self.assertTrue((ROOT/profile/'INSTALL.txt').is_file())

if __name__=='__main__':unittest.main(verbosity=2)
