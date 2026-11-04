"""Desktop verification: physics fixtures, all catalog inverses, UI/plot contracts."""
from pathlib import Path
import sys, unittest, importlib, random, math, ast, io, contextlib, os
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/os.environ.get('APC_RUNTIME','APC_EVO')))
import APCORE as C
import APTOOLS as T
import APGRAPH as P
import APCHECK

class ToolkitTests(unittest.TestCase):
    def near(self,a,b,tol=1e-7):
        self.assertLessEqual(abs(a-b),tol*max(abs(b),1e-290))
    def test_on_device_smoke_suite(self):
        self.assertEqual(APCHECK.checks(),24)
    def test_parser_precedence_domains(self):
        for text,expected in [('1e-9',1e-9),('-2^2',-4),('(-2)^2',4),('2^-3',.125),('2^3^2',512),
                              ('1--2',3),('3*(2+4)/2',9),('sqrt(4)+ln(e)',3),('cos(pi)',-1)]:
            self.near(C.calc(text),expected)
        for text in ['2x','__import__(1)','1/0','sqrt(-1)','(-1)^0.5','2+','sin(pi','nan','1e999']:
            with self.assertRaises((ValueError,ZeroDivisionError,OverflowError)):
                C.calc(text)
    def test_quadratic_stability(self):
        roots=C.quadratic(1,-1e8,1)
        self.near(roots[0],1e-8)
        self.near(roots[1],1e8)
        self.assertEqual(C.quadratic(0,2,-4),[2])
        for args in [(0,0,1),(0,0,0),(1,0,1)]:
            with self.assertRaises(ValueError): C.quadratic(*args)
    def test_calculus_and_small_roots(self):
        self.near(C.bisect(lambda x:x-1e-12,0,2e-12),1e-12)
        self.near(C.integrate(math.sin,0,math.pi,160),2,tol=2e-9)
        self.near(C.integrate(lambda x:x*x,3,0),-9)
        self.near(C.derivative(math.sin,0,.01),1,tol=1e-8)
        with self.assertRaises(ValueError): C.bisect(lambda x:x*x+1,-1,1)
        with self.assertRaises(ValueError): C.integrate(math.sin,0,1,3)
    def test_projectile_nonzero_height_and_directions(self):
        vals=dict(T.projectile(10,0,5,0,10))
        self.near(vals['flight s'],1)
        self.near(vals['dx m'],10)
        self.near(vals['vy final m/s'],-10)
        self.near(vals['peak y m'],5)
        self.assertLess(dict(T.projectile(10,math.pi,5,0,10))['dx m'],0)
        with self.assertRaises(ValueError): T.projectile(1,0,0,100,9.8)
    def test_collision_conservation(self):
        for m1,m2,u1,u2,e in [(2,3,4,-1,1),(2,3,4,-1,0),(1,10,-20,0,.3)]:
            d=dict(T.collision(m1,m2,u1,u2,e))
            self.near(m1*d['v1 m/s']+m2*d['v2 m/s'],m1*u1+m2*u2)
            self.near(d['v2 m/s']-d['v1 m/s'],e*(u1-u2))
            self.assertGreaterEqual(d['K lost J'],-1e-12)
        with self.assertRaises(ValueError): T.collision(1,1,1,0,2)
    def test_pulley_tensions(self):
        d=dict(T.atwood(1,3,.02,.1,10))
        self.near(d['a m/s^2'],10/3)
        self.near(d['T2 N']-d['T1 N'],.02*d['alpha rad/s^2']/.1)
    def test_shm_energy_and_initial_state(self):
        for t in [0,.1,1,10]:
            d=dict(T.shm(2,8,.3,-.4,t))
            self.near(d['K J']+d['U J'],.52)
        d=dict(T.shm(2,8,.3,-.4,0))
        self.near(d['x m'],.3)
        self.near(d['v m/s'],-.4)
    def test_rc_rl_limits(self):
        self.near(dict(T.rc(100,1e-3,4,12,0))['Vc V'],4)
        self.near(dict(T.rc(100,1e-3,4,12,10))['Vc V'],12)
        self.near(dict(T.rc(100,1e-3,4,0,0))['I A'],-.04)
        self.near(dict(T.rl(5,2,3,0,0))['I A'],3)
        self.near(dict(T.rl(5,2,3,0,0))['VL V'],-15)
    def test_superposition_sign_and_singularity(self):
        ex,ey,v=T.charges([(1e-9,-1,0),(-1e-9,1,0)],0,0)
        self.near(ex,2*C.CONST['ke']*1e-9)
        self.assertEqual(ey,0)
        self.assertEqual(v,0)
        with self.assertRaises(ValueError): T.charges([(1,0,0)],0,0)
    def test_sphere_continuity(self):
        ke=C.CONST['ke']
        self.near(T.sphere(1e-9,2,0,False)[1],ke*1e-9*.75)
        self.near(T.sphere(1e-9,2,1,False)[0],ke*1e-9/8)
        self.near(T.sphere(1e-9,2,1,True)[1],ke*1e-9/2)
        self.near(T.sphere(1e-9,2,2,False)[1],T.sphere(1e-9,2,2-1e-9,False)[1])
    def test_mna_multi_battery(self):
        # Two opposing cells: V1=12,V2=5, 7V across a 100 ohm resistor.
        v,ir,iv=T.network(2,[(1,2,100),(2,0,50)],[(1,0,12),(2,0,5)])
        self.near(v[1],12); self.near(v[2],5)
        self.near(ir[0],.07); self.near(ir[1],.1)
        self.near(iv[0],-.07); self.near(iv[1],-.03)
        # Floating voltage source across nodes 1 and 2, both linked to ground.
        v,ir,iv=T.network(2,[(1,0,100),(2,0,100)],[(1,2,10)])
        self.near(v[1],5); self.near(v[2],-5)
        # Power delivered by sources equals resistor heat.
        self.near(sum([(v[a]-v[b])*cur for (a,b,r),cur in zip([(1,0,100),(2,0,100)],ir)]),-10*iv[0])
        with self.assertRaises(ValueError): T.network(2,[(1,2,100)],[])
    def test_linear_scaled_and_singular(self):
        self.near(C.linear([[1e-15,0],[0,1e15]],[2e-15,3e15])[0],2)
        with self.assertRaises(ValueError): C.linear([[1,2],[2,4]],[1,2])
    def test_regression(self):
        m,b,r2=T.regress([1,2,3],[3,5,7])
        self.near(m,2); self.near(b,1); self.near(r2,1)
        with self.assertRaises(ValueError): T.regress([1,1],[2,3])
    def test_graph_sampling_limits(self):
        segments=P.samples(lambda x:1/x,-1,1,81)
        self.assertEqual(len(segments),2)
        self.assertEqual(sum(len(s[0]) for s in segments),80)
        self.assertLess(max(segments[0][0]),0)
        self.assertGreater(min(segments[1][0]),0)
        with self.assertRaises(ValueError): P.samples(lambda x:x,1,0)
    def test_plot_api_contract(self):
        from unittest.mock import patch
        import types
        calls=[]
        fake=types.ModuleType('ti_plotlib')
        for name in ['cls','window','axes','grid','title','labels','pen','color','plot','show_plot']:
            setattr(fake,name,lambda *args,n=name:calls.append((n,args)))
        with patch.dict(sys.modules,{'ti_plotlib':fake}):
            P.draw('Test',[('f',P.samples(lambda x:x*x,-2,2))],'x m','y m')
        self.assertEqual(calls[0][0],'cls')
        self.assertEqual(calls[-1][0],'show_plot')
        lines=[args for name,args in calls if name=='plot']
        self.assertEqual(len(lines[0][0]),80)
        window=next(args for name,args in calls if name=='window')
        self.assertLess(window[0],-2); self.assertGreater(window[1],2)
    def test_main_menu_flows(self):
        from unittest.mock import patch
        import APC
        # Mechanics -> unit 1 -> back to units -> main -> page 2 -> back -> quit.
        with patch('builtins.input',side_effect=['1','1','0','0','9','0']), contextlib.redirect_stdout(io.StringIO()):
            APC.main()
    def test_menu_navigation(self):
        from unittest.mock import patch
        with patch('builtins.input',side_effect=['9','2']), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(C.menu('test',[str(i) for i in range(12)]),6)
        with patch('builtins.input',side_effect=['8','1']), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(C.menu('test',[str(i) for i in range(12)]),10)
        with patch('builtins.input',return_value='0'), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(C.menu('test',['one']),-1)
    def test_numeric_input_cancellation_defaults(self):
        from unittest.mock import patch
        with patch('builtins.input',return_value='q'):
            with self.assertRaises(C.Cancel): C.number('x')
        with patch('builtins.input',return_value=''):
            self.assertEqual(C.number('x',default=3),3)
    def test_ti_source_constraints(self):
        for p in (ROOT/'APC_EVO').glob('*.py'):
            self.assertLessEqual(len(p.stem),8,p.name)
            text=p.read_text('ascii')
            self.assertLess(len(text),20000,p.name)
            tree=ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node,(ast.List,ast.Tuple)):
                    self.assertLessEqual(len(node.elts),100,p.name)
                self.assertNotIsInstance(node,(ast.AsyncFunctionDef,ast.JoinedStr,ast.NamedExpr),p.name)
        for text in ['word '*80,'A'*100,'line\nline']:
            self.assertTrue(all(len(line)<=C.WIDTH for line in C.wrap(text)))
    def test_formula_edge_cases(self):
        f=importlib.import_module('APU01').F[1]
        self.near(C.solve_formula(f,3,{'dx':10,'u':5,'a':0})[0],2)
        roots=C.solve_formula(f,3,{'dx':0,'u':3,'a':-9.8})
        self.assertEqual(len(roots),2)
        self.near(max(roots),6/9.8)
        # Field formula for inside sphere must reject outside geometry.
        f=next(e for e in importlib.import_module('APU08').F if e[0]=='Uniform sphere inside')
        self.assertEqual(C.solve_formula(f,0,{'Q':1e-9,'r':2,'R':1}),[])
        f=next(e for e in importlib.import_module('APU10').F if e[0]=='Parallel plate C')
        self.assertEqual(C.solve_formula(f,0,{'kd':1,'A':1,'d':-1}),[])
        f=next(e for e in importlib.import_module('APU10').F if e[0]=='Capacitor charge sharing')
        self.near(C.solve_formula(f,0,{'C1':2e-6,'V0':10,'C2':3e-6,'Vb':0})[0],4)
        f=next(e for e in importlib.import_module('APU13').F if e[0]=='LC peak current')
        self.near(max(C.solve_formula(f,0,{'Q0':2e-6,'ind':.01,'C':1e-6})),.02)

class CatalogTests(unittest.TestCase):
    def test_every_explicit_inverse(self):
        # Generate consistent states from independent symbolic evaluation,
        # then round-trip each unknown through calculator arithmetic/parser.
        import sympy as S
        import build_catalog as builder
        rng=random.Random(8031)
        tested=set(); bracketed=set(); misses=[]
        for unit in range(1,14):
            entries=importlib.import_module('APU'+str(unit).zfill(2)).F
            for entry in entries:
                title,eq,specs,invs,note=entry[:5]
                names=[v[0] for v in specs]
                loc={n:S.Symbol(n,real=True) for n in names}
                loc.update({n:S.Float(v) for n,v in C.CONST.items()})
                loc.update({'ln':S.log,'abs':S.Abs})
                lhs,rhs=eq.replace('^','**').split('=')
                expr=S.sympify(lhs,locals=loc)-S.sympify(rhs,locals=loc)
                anchor=next(i for i,v in enumerate(invs) if v)
                # Reuse symbolic equation's direct anchor expressions as oracle.
                solutions=S.solve(expr,loc[names[anchor]],check=False)
                for trial in range(14):
                    vals={n:rng.uniform(.2,4) for n in names}
                    for n in ['q','q1','q2','Q','lam','sig','rhoq']:
                        if n in vals: vals[n]*=1e-9
                    for n in ['C','C1','C2']:
                        if n in vals: vals[n]*=1e-6
                    for n in ['t','ph','th']:
                        if n in vals: vals[n]*=.1
                    if title.startswith('RC '):
                        if 't' in vals: vals['t']*=.02
                        if 'res' in vals: vals['res']*=1000
                    # Avoid nonphysical sphere/capacitor geometry in test states.
                    if 'r' in vals and 'R' in vals: vals['r']=vals['R']*.4
                    if 'amp' in vals and 'x' in vals: vals['x']=vals['amp']*.4
                    if 'nc' in vals: vals['nc']=rng.randint(1,12)
                    for sol in solutions:
                        try:
                            x=complex(sol.evalf(subs={loc[k]:v for k,v in vals.items() if k!=names[anchor]}))
                        except (TypeError,ValueError,OverflowError): continue
                        if abs(x.imag)>1e-15 or not math.isfinite(x.real): continue
                        if specs[anchor][3]=='+' and x.real<=0: continue
                        if specs[anchor][3]=='0' and x.real<0: continue
                        vals[names[anchor]]=x.real
                        break
                    else: continue
                    for target,expressions in enumerate(invs):
                        expected=vals[names[target]]
                        known={k:v for k,v in vals.items() if k!=names[target]}
                        if not expressions:
                            def residual(x):
                                known[names[target]]=x
                                return C.calc(lhs.replace('**','^'),known)-C.calc(rhs.replace('**','^'),known)
                            delta=abs(expected)*.03
                            try:
                                got=C.bisect(residual,expected-delta,expected+delta)
                                if abs(got-expected)<=1e-6*max(abs(expected),1e-290):
                                    bracketed.add((unit,title,names[target]))
                            except (ValueError,ZeroDivisionError,OverflowError):
                                pass
                            continue
                        roots=C.solve_formula(entry,target,known)
                        key=(unit,title,names[target])
                        if any(abs(v-expected)<=2e-6*max(abs(expected),1e-290) for v in roots):
                            tested.add(key)
                for i,inv in enumerate(invs):
                    if inv and (unit,title,names[i]) not in tested:
                        misses.append((unit,title,names[i]))
                    if not inv and (unit,title,names[i]) not in bracketed:
                        misses.append((unit,title,names[i],'numeric'))
        self.assertFalse(misses,'Untested/failed inverses: '+str(misses))
        print('\nCatalog:',len(tested),'explicit and',len(bracketed),'bracketed target inverses verified')

if __name__=='__main__':
    unittest.main(verbosity=2)
