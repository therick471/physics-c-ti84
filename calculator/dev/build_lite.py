"""Plain TI-Python release: small imports, selected-row catalogs, TI launchers."""
import ast, json
from pathlib import Path
from package_toolkit import minify
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'APC_EVO'
OUT=ROOT/'APC_LITE_SOURCE'
INSTALL=ROOT/'APC_LITE'
OUT.mkdir(exist_ok=True)
INSTALL.mkdir(exist_ok=True)
class PortableText(ast.NodeTransformer):
    def visit_Call(self,node):
        node=self.generic_visit(node)
        if not isinstance(node.func,ast.Attribute): return node
        method=node.func.attr
        if method in ('isdigit','isalpha','isalnum'):
            alphabet='0123456789' if method=='isdigit' else 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            if method=='isalnum': alphabet+='0123456789'
            return ast.copy_location(ast.Compare(left=node.func.value,ops=[ast.In()],comparators=[ast.Constant(alphabet)]),node)
        return node
def functions(filename):
    text=(SRC/filename).read_text()
    return {n.name:ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def put(name,text):
    tree=ast.parse(text)
    portable=PortableText()
    tree=portable.visit(tree)
    ast.fix_missing_locations(tree)
    text=ast.unparse(tree)+'\n'
    ast.parse(text)
    (OUT/(name+'.py')).write_text(text,encoding='ascii')
    (INSTALL/(name+'.py')).write_text(minify(text),encoding='ascii')
core=functions('APCORE.py')
put('APNUM','from math import sqrt\n\ndef finite(x):\n    return isinstance(x,(int,float)) and x==x and abs(x)<1e300\n\n'+'\n\n'.join(core[n] for n in ['quadratic','bisect','integrate','derivative','linear'])+'\n')
arithmetic='''from math import sqrt, sin, cos, tan, asin, acos, atan, exp, log, pi
CONST={'pi':pi,'e':exp(1),'g':9.8,'G':6.67430e-11,'ke':8.9875517923e9,'eps0':8.8541878128e-12,'mu0':1.25663706212e-6,'qe':1.602176634e-19,'me':9.1093837139e-31,'mp':1.67262192595e-27,'c0':299792458.0}
ln=log
FUN='sqrt sin cos tan asin acos atan exp ln log abs'.split()
LAST=[0.0]
WIDTH=30
class Cancel(Exception):
    pass
def finite(x):
    return isinstance(x,(int,float)) and x==x and abs(x)<1e300
def calc(text,values=None):
    # Substitute approved numeric names; reject attributes and Python statements.
    values={} if values is None else values
    s=text.replace(' ','').replace('**','^')
    out=''
    bindings=[]
    i=0
    while i<len(s):
        c=s[i]
        j=i+1
        if c.isdigit() or c=='.':
            while j<len(s) and (s[j].isdigit() or s[j]=='.'): j+=1
            if j<len(s) and s[j] in 'eE':
                j+=1
                if j<len(s) and s[j] in '+-': j+=1
                while j<len(s) and s[j].isdigit(): j+=1
            token=s[i:j]
            float(token)
            out+=token
        elif c.isalpha():
            while j<len(s) and s[j].isalnum(): j+=1
            name=s[i:j]
            if j<len(s) and s[j]=='(':
                if name not in FUN: raise ValueError('Unknown function')
                out+=name
            else:
                if name in values: value=values[name]
                elif name=='ans': value=LAST[0]
                elif name in CONST: value=CONST[name]
                else: raise ValueError('Unknown name: '+name)
                out+='_v'+str(len(bindings))
                bindings.append(value)
        elif c in '+-*/^()': out+= '**' if c=='^' else c
        else: raise ValueError('Use arithmetic syntax')
        i=j
    scope=globals()
    for k in range(len(bindings)): scope['_v'+str(k)]=bindings[k]
    try:
        v=eval(out)
    except (SyntaxError,NameError,TypeError): raise ValueError('Invalid expression')
    finally:
        for k in range(len(bindings)): del scope['_v'+str(k)]
    if not finite(v): raise ValueError('Invalid or non-real result')
    return v
def magnitude(s,vals):
    # Top-level term magnitudes allow roundoff when terms cancel to zero.
    depth=0
    start=0
    total=0.0
    for i in range(len(s)):
        c=s[i]
        if c=='(': depth+=1
        elif c==')': depth-=1
        elif c in '+-' and depth==0 and i>start and s[i-1] not in '+-*/^eE':
            total+=abs(calc(s[start:i],vals))
            start=i
    return total+abs(calc(s[start:],vals))
def checked_sides(lhs,rhs,vals,tolerance=1e-7):
    l,r=calc(lhs,vals),calc(rhs,vals)
    scale=max(magnitude(lhs,vals),magnitude(rhs,vals),abs(l),abs(r),1e-300)
    return abs(l-r)<=tolerance*scale
try:
    from ti_system import disp_clr
except ImportError:
    def disp_clr(): print('\\n'*2)
'''
ui='\n\n'.join(core[n] for n in ['wrap','head','info','menu','number','integer','fmt','result','error'])
ui=ui.replace("    HISTORY.append((title, '\\n'.join(lines)))\n    if len(HISTORY) > 8:\n        HISTORY.pop(0)\n",'')
put('APCORE',arithmetic+'\n'+ui+'\n')
put('APFORM','from APCORE import calc, checked_sides, menu, head, info, number, result, Cancel, error\nfrom APNUM import quadratic, bisect\n\n'+'\n\n'.join(core[n] for n in ['valid_geometry','solve_formula','formula_ui'])+'\n')
catalog=json.loads((ROOT/'dev/catalog.json').read_text())
units={s[0]:(s[1],s[2]) for u,e in catalog for s in e[2]}
metadata='\n'+'\n'.join(n+'|'+label+'|'+unit for n,(label,unit) in units.items())+'\n'
put('APDATA','U='+repr(metadata)+'''
def row(data,index):
    start=0
    for i in range(index): start=data.find('\\n',start)+1
    end=data.find('\\n',start)
    return data[start:] if end<0 else data[start:end]
def titles(data):
    out=[]
    start=0
    while start<len(data):
        out.append(data[start:data.find('|',start)])
        end=data.find('\\n',start)
        if end<0: break
        start=end+1
    return out
def entry(data,index):
    title,eq,names,domains,note,methods=row(data,index).split('|')
    names=names.split(',')
    specs=[]
    for i,n in enumerate(names):
        start=U.find('\\n'+n+'|')+1
        name,label,unit=U[start:U.find('\\n',start)].split('|')
        specs.append((name,label,unit,domains[i]))
    inverses=[]
    polys=[]
    for m in methods.split(';'):
        parts=m[2:].split(',') if len(m)>2 else []
        polys.append(parts if m[0]=='P' else [])
        inverses.append(['@']*max(1,len(parts)-1) if m[0]=='P' else parts)
    return title,eq,specs,inverses,note,polys
''')
for unit in range(1,14):
    rows=[]
    for u,e in catalog:
        if u!=unit: continue
        title,eq,specs,invs,note,polys=e
        methods=['P:'+','.join(polys[i]) if polys[i] else 'E:'+','.join(invs[i]) for i in range(len(specs))]
        rows.append('|'.join([title,eq,','.join(s[0] for s in specs),''.join(s[3] for s in specs),note,';'.join(methods)]))
    put('APU'+str(unit).zfill(2),'DATA='+repr('\n'.join(rows))+'\n')
t=functions('APTOOLS.py')
tree=ast.parse((SRC/'APTOOLS.py').read_text())
imports='from math import sqrt, sin, cos, atan2, exp, pi\nfrom APCORE import CONST, number, integer, menu, head, info, result, Cancel, error\nfrom APNUM import quadratic, linear\n'
run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run_tool')
branches={}
n=run.body[0]
while isinstance(n,ast.If):
    branches[n.test.comparators[0].value]=n.body
    n=n.orelse[0] if n.orelse else None
groups=[list(range(6))+[12],list(range(6,12))+[14],[13,0]]
for name,indices in zip(['APMECH','APEM','APLAB'],groups):
    body=[ast.If(test=ast.Compare(left=ast.Name(id='which',ctx=ast.Load()),ops=[ast.Eq()],comparators=[ast.Constant(i)]),body=branches[i],orelse=[]) for i in indices]
    fn=ast.FunctionDef(name='run_tool',args=run.args,body=body,decorator_list=[])
    ast.fix_missing_locations(fn)
    fntext=ast.unparse(fn)
    needed=set()
    pending=[fntext]
    while pending:
        code=pending.pop()
        for node in ast.walk(ast.parse(code)):
            if isinstance(node,ast.Name) and node.id in t and node.id!='run_tool' and node.id not in needed:
                needed.add(node.id); pending.append(t[node.id])
    put(name,imports+'\n\n'.join(t[k] for k in t if k in needed)+'\n\n'+fntext+'\n')
names=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and n.targets[0].id=='NAMES')
put('APTOOLS','from APCORE import menu, info, Cancel, error\nfrom APMEM import release\nNAMES='+repr(names)+'''
def main():
    while True:
        i=menu('Multi-step tools',NAMES)
        if i<0: return
        name='APMECH' if i<6 or i==12 else ('APLAB' if i==13 else 'APEM')
        mod=None
        try:
            mod=__import__(name)
            mod.run_tool(i)
        except Cancel: pass
        except ImportError: info('Optional tools','Transfer the missing optional tool group from the release.')
        except (ValueError,ZeroDivisionError,OverflowError) as e: error(e)
        finally:
            mod=None
            release([name,'APNUM'])
''')
put('APMEM','''import sys
import gc
def release(names):
    if hasattr(sys,'modules'):
        for name in names:
            if name in sys.modules: del sys.modules[name]
    gc.collect()
''')
mathtext=(SRC/'APMATH.py').read_text().replace('from APCORE import calc, menu, head, info, number, integer, result, error, Cancel, bisect, integrate, derivative, quadratic, linear','from APCORE import calc, menu, head, info, number, integer, result, error, Cancel\nfrom APNUM import bisect, integrate, derivative, quadratic, linear')
put('APMATH',mathtext)
put('APGRAPH',(ROOT/'dev/lite_graph.py').read_text())
launcher=(SRC/'APC.py').read_text()
launcher=launcher[launcher.index('UNITS ='):launcher.index('def unit_ui')]
put('APC','''# TI Run imports a program: call main unconditionally.
from APCORE import menu, info, head, number, result, CONST, LAST, Cancel, error, fmt
from APMEM import release
'''+launcher+'''
def unit_ui(unit):
    name='APU'+('0' if unit<10 else '')+str(unit)
    mod=__import__(name)
    from APDATA import titles, entry
    from APFORM import formula_ui
    while True:
        i=menu(UNITS[unit-1],titles(mod.DATA))
        if i<0: break
        f=entry(mod.DATA,i)
        while True:
            j=menu(f[0],['Solve an unknown','Graph this relation','Equation / variables'])
            if j<0: break
            try:
                if j==0: formula_ui(f)
                elif j==1:
                    graph=None
                    try:
                        graph=__import__('APGRAPH')
                        graph.plot_formula(f)
                    finally:
                        graph=None
                        release(['APGRAPH'])
                else: info(f[0],f[1]+'\\n'+'\\n'.join(s[0]+' = '+s[1]+' ['+s[2]+']' for s in f[2])+'\\n'+f[4])
            except Cancel: pass
            except (ValueError,ZeroDivisionError,OverflowError) as e: error(e)
        f=None
    mod=None
def main():
    while True:
        i=menu('PHYSICS C',['Mechanics: units 1-7','E&M: units 8-13','Multi-step solvers','Math / lab tools','Graphs','Constants / g','Last answer','Help / input syntax'])
        if i<0: return
        if i<2:
            offset=0 if i==0 else 7
            while True:
                j=menu('Mechanics' if i==0 else 'E&M',UNITS[:7] if i==0 else UNITS[7:])
                if j<0: break
                try: unit_ui(offset+j+1)
                except MemoryError: info('Memory','Restart the Python shell, then run APC. Record the failing unit if this repeats.')
                release(['APU'+('0' if offset+j+1<10 else '')+str(offset+j+1),'APDATA','APFORM','APNUM','APGRAPH'])
        elif i in (2,3,4):
            name=['APTOOLS','APMATH','APGRAPH'][i-2]
            mod=None
            try:
                mod=__import__(name)
                mod.main()
            except ImportError: info('Optional tools','Transfer the optional tool files from the release to use this menu.')
            except MemoryError: info('Memory','Restart the Python shell and run APC again.')
            finally:
                mod=None
                release([name,'APMECH','APEM','APLAB','APFORM','APNUM'])
        elif i==5:
            info('Constants','\\n'.join(n+'='+fmt(CONST[n]) for n in CONST))
            try: CONST['g']=number('g m/s^2','+',CONST['g'])
            except Cancel: pass
        elif i==6: info('Last answer','ans='+fmt(LAST[0]))
        else:
            info('Help','0 Back; 8 previous; 9 next. Select 1..5 then ENTER. Use SI units and radians. q cancels inputs. ENTER reuses a displayed value. ans reuses the last result. Inputs: 2.5e-6, pi/4, sqrt(2), ke*qe. Use * explicitly and ^ for powers. All 160 equations remain. Equation assumptions are shown. Full concept notes and variable definitions are in the computer reference files. Graphs sample 40 points: use narrow windows. Numerical targets require a continuous sign-changing bracket. Restart the Python shell before APCHECK or after MemoryError.')
main()
''')
put('APCHECK','''# Small visible smoke check. TI Run imports this program.
from math import sqrt, sin, pi
def check(a,b):
    if abs(a-b)>1e-7*max(abs(b),1e-290): raise ValueError('Wrong result')
def main():
    print('APCHECK START v3')
    stage='math'
    try:
        check(sqrt(4),2)
        check(sin(pi/2),1)
        stage='expressions'
        from APCORE import calc
        check(calc('-2^2'),-4)
        check(calc('2^3^2'),512)
        check(calc('sin(pi/2)+2.5e-6'),1.0000025)
        stage='quadratic / root'
        from APNUM import quadratic, bisect
        roots=quadratic(1,-3,2)
        check(roots[0],1)
        check(roots[1],2)
        check(bisect(lambda x:x*x-2,0,2),sqrt(2))
        print('SELF CHECK PASS')
        print('8 numeric checks passed.')
        print('Restart shell, then run APC.')
    except MemoryError:
        print('SELF CHECK MEMORY ERROR')
        print('Restart Python shell and retry.')
    except Exception as e:
        print('SELF CHECK FAILED')
        print('Stage: '+stage)
        print(str(e))
    input('ENTER to finish ')
main()
''')
print('Plain install:',sum(p.stat().st_size for p in INSTALL.glob('*.py')),'bytes;',len(list(INSTALL.glob('*.py'))),'files')
