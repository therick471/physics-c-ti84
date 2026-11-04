from math import pi, sqrt
from APCORE import menu, head, info, number, result, fmt, Cancel, error
from APMEM import release
from EFMODEL import NAMES, K, field, ring_distances, inverse_distance, arc_components
from EFGUI import cards, GRAPHICS

def parameters(kind):
    head(NAMES[kind])
    d=number('R m' if kind in (0,4) else ('Full rod L m' if kind in (1,2) else 'Reference R m'),'+')
    phi=pi
    if kind==4: phi=number('Arc sweep degrees','+')*pi/180
    if kind==3: q=number('lambda C/m')
    else:
        choice=menu('Given charge',['Total Q coulombs','Linear density lambda C/m'])
        if choice<0: raise Cancel()
        q=number('Q coulombs' if choice==0 else 'lambda C/m')
        if choice==1: q*=2*pi*d if kind==0 else (d*phi if kind==4 else d)
    return q,d,phi

def guide(kind):
    name='EFN'+str(kind)
    mod=__import__(name)
    steps=[]
    for line in mod.DATA.split('\n'):
        split=line.find('|')
        steps.append((line[:split],line[split+1:]))
    cards(NAMES[kind],steps)
    steps=None
    mod=None
    release([name])

def calculate(kind):
    q,d,phi=parameters(kind)
    x=0 if kind==4 else number('x m','+' if kind==2 else 's')
    e,v=field(kind,q,d,x,phi)
    pairs=[('lambda C/m' if kind==3 else 'Q C',q),('E N/C',e),('|E| N/C',abs(e)),('V volts',v)]
    if kind!=3: pairs.insert(1,('lambda C/m',q/(2*pi*d if kind==0 else (d*phi if kind==4 else d))))
    if kind==4:
        mid=number('Arc midpoint angle deg','s',180)*pi/180
        ex,ey,v=arc_components(q,d,phi,mid)
        pairs=[('Ex N/C',ex),('Ey N/C',ey),('|E| N/C',abs(e)),('V volts',v)]
    LAST[0]=abs(e) if kind==4 else e
    cards('Solution',[('Substitute SI values','\n'.join(n+' = '+fmt(v) for n,v in pairs)),('Direction / units','E is signed along the positive observation axis; negative Q reverses it. For an arc, Ex/Ey use the entered midpoint angle. F=q_test*E; U=q_test*V. N/C=V/m. V(infinity)=0 for finite distributions. Infinite line uses V(R)=0.')])
    next_action=menu('Continue',['Full start-to-finish guide','Force on test charge'])
    if next_action<0:return
    if next_action==0: guide(kind)
    else:
        test=number('Test charge C')
        if kind==4: result('Test charge',[('Fx N',test*ex),('Fy N',test*ey),('U J',test*v)])
        else: result('Test charge',[('F N',test*e),('U J',test*v)])

def extrema(kind):
    q,d,phi=parameters(kind)
    if q==0:
        cards('Extrema',[('Zero source','E and V are zero wherever the model is defined. Extrema are not unique.')]); return
    if kind==0:
        xp=d/sqrt(2)
        peak=abs(field(0,q,d,xp)[0])
        text='x_peak=R/sqrt(2)='+fmt(xp)+' m. Max |E|='+fmt(peak)+' N/C. Emax=2*k*abs(Q)/(3*sqrt(3)*R^2). Both +x_peak and -x_peak maximize |E|. For Q>0 signed E has max at +x_peak, min at -x_peak; Q<0 swaps them. Min |E|=0 at x=0; infinity is a limit, not a finite root.'
    elif kind in (1,2,3): text='On x>0, |E| decreases strictly from infinity to 0. There is no finite global maximum or attained minimum. At infinity the infimum is zero. Fix Q (or lambda) and size when comparing x. Limits and derivatives are in the full guide.'
    else: text='Vary phi at FIXED lambda: |E|=2*k*abs(lambda)*sin(phi/2)/R. Maximum at phi=pi (180 deg); full ring phi=2*pi gives zero. At FIXED Q: |E|=k*abs(Q)/R^2 *sin(phi/2)/(phi/2), decreases for 0<phi<=2*pi. Its supremum k*abs(Q)/R^2 is approached as phi->0; no finite positive-phi maximum. Do not mix fixed-Q and fixed-lambda comparisons.'
    cards('Extrema',[('Maxima / minima',text),('At x=R (ring), L (rod)','E(size)='+fmt(field(kind,q,d,d,phi)[0])+' N/C; V(size)='+fmt(field(kind,q,d,d,phi)[1])+' V.' if kind!=4 else 'Arc-center model has no observation x. Use ring-axis mode for axial x limits. Here R is the arc radius, not distance from its center.')])

def inverse(kind):
    if kind==4: info('Arc inverse','Use the numeric evaluator or E&M equation reference for charge/radius. Choose the fixed parameter before varying arc sweep.'); return
    which=menu('Solve backward',['Source Q (line: lambda)','Distance x from E'])
    if which<0: return
    d=number('R m' if kind in (0,3) else 'Full L m','+')
    target=number('Signed E N/C')
    if which==0:
        x=number('x m','+' if kind==2 else 's')
        unit=field(kind,1,d,x)[0]
        if unit==0: raise ValueError('At ring center E=0 for every Q')
        result('Source',[('lambda C/m' if kind==3 else 'Q C',target/unit)])
    else:
        q=number('lambda C/m' if kind==3 else 'Q C')
        roots=ring_distances(q,d,target) if kind==0 else [inverse_distance(kind,q,d,target)]
        result('Positive-side x', [('x m',r) for r in roots], 'Ring can give TWO distances. E=0 has x=0; infinity is a limit, not another finite root.')

def plot(kind):
    if kind==4: info('Arc plot','Use custom f(x)=sin(x/2) for fixed density or sin(x/2)/(x/2) for fixed charge; x is sweep in radians, 0<x<=2*pi.'); return
    q,d,phi=parameters(kind)
    which=menu('Vertical axis',['Signed E','Magnitude |E|','Potential V'])
    if which<0: return
    lo,hi=number('LOW x'),number('HIGH x')
    from APGRAPH import draw, samples
    def f(x):
        e,v=field(kind,q,d,x)
        return e if which==0 else (abs(e) if which==1 else v)
    # Split at singular x=0, including when sampling would otherwise miss it.
    seg=[]
    if kind in (1,3) and lo<0<hi:
        gap=max(abs(lo),abs(hi))*1e-6
        seg=samples(f,lo,-gap,20)+samples(f,gap,hi,20)
    else: seg=samples(f,lo,hi,40)
    draw(['Ring axis','Rod bisector','Rod beyond end','Infinite line'][kind],[('field',seg)],'x m','V' if which==2 else 'E N/C')

def main():
    while True:
        i=menu('E-FIELD STUDIO',['Ring: on its axis','Rod: perpendicular bisector','Rod: beyond an end','Infinite straight line','Arc: center / sectors','Two rings / point charges','Custom calculus / limits','Display: graphic/text'])
        if i<0: return
        try:
            if i<5:
                while True:
                    j=menu(NAMES[i],['Calculate E, V and force','Full derivation + limits','Maxima / minima','Graph E(x) or V(x)','Solve for source or x','Geometry sketch'])
                    if j<0: break
                    if j==0: calculate(i)
                    elif j==1: guide(i)
                    elif j==2: extrema(i)
                    elif j==3: plot(i)
                    elif j==4: inverse(i)
                    else:
                        if i in (0,1):
                            from EFGUI import sketch
                            sketch(i)
                        else: guide(i)
            elif i in (5,6):
                from EFTOOLS import main as tools
                tools(i==6)
                tools=None
            else:
                GRAPHICS[0]=not GRAPHICS[0]
                info('Display','Graphical cards ON. CLEAR closes a card; ENTER advances; 8 previous; 0 exit.' if GRAPHICS[0] else 'Text cards ON.')
        except Cancel: pass
        except (ValueError,ZeroDivisionError,OverflowError) as e: error(e)
        except MemoryError: info('Memory','Restart Python, then run EFIELD directly.')
        release(['APGRAPH','EFTOOLS'])
