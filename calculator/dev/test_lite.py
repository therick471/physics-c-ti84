"""Test the plain release, including TI's import-style startup."""
import sys, importlib, types, io, contextlib, runpy, unittest, os
os.environ["APC_RUNTIME"]="APC_LITE"
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'APC_LITE'))
import APCORE as C, APNUM as N, APFORM as F, APDATA as D
# Adapt the existing independent physics fixtures to the split runtime.
for name in ['quadratic','bisect','integrate','derivative','linear']:
    setattr(C,name,getattr(N,name))
C.solve_formula=F.solve_formula
T=importlib.import_module('APTOOLS')
for group in ['APMECH','APEM','APLAB']:
    mod=importlib.import_module(group)
    for name in dir(mod):
        if not name.startswith('_'): setattr(T,name,getattr(mod,name))
for u in range(1,14):
    mod=importlib.import_module('APU'+str(u).zfill(2))
    # Test-only materialization. The calculator parses one selected row.
    mod.F=[D.entry(mod.DATA,i) for i in range(len(D.titles(mod.DATA)))]
# Legacy tests import this module, but its new launcher runs immediately.
stub=types.ModuleType('APCHECK')
sys.modules['APCHECK']=stub
import test_toolkit as original

def smoke(self):
    out=io.StringIO()
    with patch('builtins.input',return_value=''),contextlib.redirect_stdout(out):
        runpy.run_path(str(ROOT/'APC_LITE/APCHECK.py'),run_name='APCHECK')
    self.assertIn('APCHECK START',out.getvalue())
    self.assertIn('SELF CHECK PASS',out.getvalue())
    self.assertIn('8 numeric checks passed.',out.getvalue())
original.ToolkitTests.test_on_device_smoke_suite=smoke
def menu_flow(self):
    out=io.StringIO()
    with patch('builtins.input',side_effect=['1','1','0','0','9','0']), contextlib.redirect_stdout(out):
        runpy.run_path(str(ROOT/'APC_LITE/APC.py'),run_name='APC')
    self.assertIn('Kinematics',out.getvalue())
    self.assertNotIn('APU01',sys.modules)
original.ToolkitTests.test_main_menu_flows=menu_flow
# Default graph size is intentionally reduced; explicit sample tests unchanged.
oldplot=original.ToolkitTests.test_plot_api_contract
# Replace its assertion about the previous default sample count.
source=Path(original.__file__).read_text()
a=source.index('    def test_plot_api_contract')
b=source.index('\n    def ',a+8)
code=source[a:b].replace('len(lines[0][0]),80','len(lines[0][0]),40')
ns={}
exec('class Adapted:\n'+code,original.__dict__,ns)
original.ToolkitTests.test_plot_api_contract=ns['Adapted'].test_plot_api_contract

def catalog_setup(self):
    for u in range(1,14):
        mod=importlib.import_module('APU'+str(u).zfill(2))
        mod.F=[D.entry(mod.DATA,i) for i in range(len(D.titles(mod.DATA)))]
original.CatalogTests.setUp=catalog_setup

class LiteTests(unittest.TestCase):
    def test_character_checks_without_string_predicate_methods(self):
        class LimitedString(str):
            def __getattribute__(self,name):
                if name in ('isalnum','isdigit','isalpha'):
                    raise AttributeError('str object has no attribute '+name)
                return super().__getattribute__(name)
            def replace(self,*args):
                return LimitedString(super().replace(*args))
            def __getitem__(self,index):
                return LimitedString(super().__getitem__(index))
        with self.assertRaises(AttributeError): LimitedString('x2').isalnum()
        for expr,expected in [('sin(pi/2)+2.5e-6',1.0000025),('eps0/eps0',1),('2^3^2',512),('alpha2+1',3)]:
            self.assertAlmostEqual(C.calc(LimitedString(expr),{'alpha2':2}),expected)
    def test_import_launches_menu(self):
        out=io.StringIO()
        with patch('builtins.input',return_value='0'),contextlib.redirect_stdout(out):
            importlib.import_module('APC')
        self.assertIn('PHYSICS C',out.getvalue())
        sys.modules.pop('APC',None)
    def test_full_menu_solver_flow(self):
        # Main -> Mechanics -> Unit 2 -> Newton -> Solve -> F -> m=2,a=3.
        out=io.StringIO()
        with patch('builtins.input',side_effect=['1','2','1','1','1','2','3','','0','0','0','0','0']),contextlib.redirect_stdout(out):
            runpy.run_path(str(ROOT/'APC_LITE/APC.py'),run_name='APC')
        self.assertIn('F N = 6',out.getvalue())
        self.assertNotIn('Check inputs',out.getvalue())
        self.assertNotIn('APU02',sys.modules)
    def test_unit_data_matches_catalog(self):
        import json
        refs=json.loads((ROOT/'dev/catalog.json').read_text())
        for u in range(1,14):
            mod=importlib.import_module('APU'+str(u).zfill(2))
            entries=[e for unit,e in refs if unit==u]
            self.assertEqual(D.titles(mod.DATA),[e[0] for e in entries])
            for i,ref in enumerate(entries):
                actual=D.entry(mod.DATA,i)
                self.assertEqual(actual[0],ref[0])
                self.assertEqual(actual[1],ref[1])
                self.assertEqual(actual[4],ref[4])
                self.assertEqual(actual[5],ref[5])
                self.assertEqual([(s[0],s[2],s[3]) for s in actual[2]],[(s[0],s[2],s[3]) for s in ref[2]])
    def test_all_units_release_imports(self):
        # Visit all 13 units through a single session; unit imports must be evicted.
        answers=[]
        clean_points=[]
        for u in range(1,14):
            local=u-1 if u<=7 else u-8
            answers.append('1' if u<=7 else '2')
            if local>=5: answers.append('9')
            answers.append(str(local%5+1))
            answers.append('0')
            clean_points.append(len(answers))
            answers.append('0')
        answers.append('0')
        count=[0]
        def reply(prompt):
            if count[0] in clean_points:
                self.assertFalse(any(n.startswith('APU') for n in sys.modules))
                self.assertNotIn('APFORM',sys.modules)
                self.assertNotIn('APDATA',sys.modules)
            answer=answers[count[0]]
            count[0]+=1
            return answer
        # Remove test-only preloaded catalogs before evaluating lifecycle behavior.
        for name in list(sys.modules):
            if name.startswith('APU'): del sys.modules[name]
        with patch('builtins.input',side_effect=reply),contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(str(ROOT/'APC_LITE/APC.py'),run_name='APC')
        self.assertEqual(count[0],len(answers))
    def test_evaluation_releases_temporary_values(self):
        self.assertEqual(C.calc('x+x',{'x':1e-12}),2e-12)
        self.assertFalse(any(n.startswith('_v') for n in vars(C)))
        with self.assertRaises(ZeroDivisionError): C.calc('x/0',{'x':1})
        self.assertFalse(any(n.startswith('_v') for n in vars(C)))
    def test_plain_no_decoder(self):
        import ast
        for path in (ROOT/'APC_LITE').glob('*.py'):
            code=path.read_text()
            tree=ast.parse(code)
            self.assertLessEqual(len(path.stem),8)
            self.assertLess(len(code),20000)
            for node in ast.walk(tree):
                if isinstance(node,(ast.List,ast.Tuple)): self.assertLessEqual(len(node.elts),100)
                self.assertNotIsInstance(node,(ast.AsyncFunctionDef,ast.JoinedStr,ast.NamedExpr))
                if isinstance(node,ast.Attribute):
                    self.assertNotIn(node.attr,('isalnum','isdigit','isalpha'))
            self.assertNotIn('APLOAD',code)
            self.assertNotIn('exec(',code)
            if path.stem in ['APC','APCHECK']:
                self.assertTrue(code.rstrip().endswith('main()'))
                self.assertNotIn('__main__',code)

if __name__=='__main__':
    suite=unittest.TestSuite()
    for cls in [original.ToolkitTests,original.CatalogTests,LiteTests]:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())
