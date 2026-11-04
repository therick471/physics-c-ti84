# Low-memory plots. 40 samples; no calculator-native Y= editor changes.
from APCORE import menu, head, info, number, calc, error, Cancel, CONST
from math import sin, cos, sqrt, pi

def samples(f,lo,hi,count=40):
    if lo>=hi or count<2 or count>100: raise ValueError('Need low<high; 2..100 points')
    segments=[]
    xs=[]
    ys=[]
    for i in range(count):
        x=lo+(hi-lo)*i/(count-1)
        try:
            y=f(x)
            if y!=y or abs(y)>1e100: raise ValueError('Unbounded')
            xs.append(x)
            ys.append(y)
        except (ValueError,ZeroDivisionError,OverflowError):
            if xs: segments.append((xs,ys))
            xs=[]
            ys=[]
    if xs: segments.append((xs,ys))
    return segments

def draw(title,series,xl='x',yl='y'):
    import ti_plotlib as p
    xmin=xmax=ymin=ymax=None
    for label,segments in series:
        for xs,ys in segments:
            for i in range(len(xs)):
                x,y=xs[i],ys[i]
                if xmin is None: xmin=xmax=x; ymin=ymax=y
                else: xmin=min(xmin,x); xmax=max(xmax,x); ymin=min(ymin,y); ymax=max(ymax,y)
    if xmin is None: raise ValueError('No defined points')
    dx=(xmax-xmin)*.06 if xmax!=xmin else max(1,abs(xmin)*.06)
    dy=(ymax-ymin)*.12 if ymax!=ymin else max(1,abs(ymin)*.12)
    p.cls()
    p.window(xmin-dx,xmax+dx,ymin-dy,ymax+dy)
    p.axes('on')
    p.grid((xmax-xmin+2*dx)/5,(ymax-ymin+2*dy)/5,'dot')
    p.title(title[:25])
    p.labels(xl[:15],yl[:15],11,2)
    p.pen('thin','solid')
    for j in range(len(series)):
        p.color(0,100,220) if j==0 else p.color(220,60,40)
        for xs,ys in series[j][1]:
            if len(xs)>1: p.plot(xs,ys,'')
            else: p.plot(xs[0],ys[0],'o')
    p.show_plot()

def plot_formula(entry):
    from APFORM import solve_formula
    title,eq,specs,invs,note=entry[:5]
    yi=menu('Vertical variable',[s[0]+' '+s[2] for s in specs])
    if yi<0: return
    options=[i for i in range(len(specs)) if i!=yi]
    pick=menu('Horizontal variable',[specs[i][0]+' '+specs[i][2] for i in options])
    if pick<0: return
    xi=options[pick]
    if not invs[yi]:
        info('Choose another axis','Numeric targets cannot be swept. Choose an explicit target or custom f(x).')
        return
    branch=0
    if len(invs[yi])>1:
        branch=menu('Root branch (ascending)',['Root '+str(i+1) for i in range(len(invs[yi]))])
        if branch<0: return
    vals={}
    for i in range(len(specs)):
        if i not in (xi,yi): vals[specs[i][0]]=number(specs[i][0]+' '+specs[i][2],specs[i][3])
    lo,hi=number('LOW x'),number('HIGH x')
    def f(x):
        domain=specs[xi][3]
        if (domain=='+' and x<=0) or (domain=='0' and x<0): raise ValueError('Domain')
        vals[specs[xi][0]]=x
        # Do not retain the previous sample's vertical value in known parameters.
        if specs[yi][0] in vals: del vals[specs[yi][0]]
        roots=solve_formula(entry,yi,vals)
        roots.sort()
        if len(roots)<=branch: raise ValueError('Branch undefined')
        return roots[branch]
    info('Plot note',note+'\n40 samples can miss poles or peaks. Use a narrow window.')
    draw(title,[(specs[yi][0],samples(f,lo,hi))],specs[xi][0]+' '+specs[xi][2],specs[yi][0]+' '+specs[yi][2])

def main():
    while True:
        i=menu('Graphs',['Custom f(x)','Projectile path','Motion x(t)','SHM x(t)','RC voltage','RL current'])
        if i<0: return
        try:
            head('Graph | radians / SI')
            if i==0:
                s=input('f(x): ').strip()
                if s.lower()=='q': raise Cancel()
                lo,hi=number('LOW x'),number('HIGH x')
                f=lambda x:calc(s,{'x':x})
            elif i==1:
                from APNUM import quadratic
                v,th=number('Speed m/s','0'),number('Angle rad')
                y0,yf=number('Launch y m'),number('Landing y m')
                g=CONST['g']
                times=[t for t in quadratic(-g/2,v*sin(th),y0-yf) if t>=0]
                if not times or max(times)==0: raise ValueError('No positive flight time')
                t=max(times)
                xs=[v*cos(th)*t*j/39 for j in range(40)]
                ys=[y0+v*sin(th)*t*j/39-g*(t*j/39)**2/2 for j in range(40)]
                draw('Projectile',[('path',[(xs,ys)])],'x m','y m')
                continue
            elif i==2:
                x0,u,a=number('Initial x m'),number('Initial v m/s'),number('Acceleration m/s^2')
                lo,hi=0,number('End time s','+')
                f=lambda x:x0+u*x+a*x*x/2
            elif i==3:
                amp,w,ph=number('Amplitude m','0'),number('Omega rad/s','+'),number('Phase rad')
                lo,hi=0,number('End time s','+',4*pi/w)
                f=lambda x:amp*cos(w*x+ph)
            else:
                res=number('R ohm','+')
                val=number('C farad' if i==4 else 'L henry','+')
                tau=res*val if i==4 else val/res
                initial,final=number('Initial value'),number('Final value')
                lo,hi=0,number('End time s','+',5*tau)
                f=lambda x:final+(initial-final)*calc('exp(-x/tau)',{'x':x,'tau':tau})
            draw('Physics C', [('f',samples(f,lo,hi))])
        except Cancel: pass
        except ImportError: info('Graph module','ti_plotlib is required. Try on the calculator.')
        except (ValueError,ZeroDivisionError,OverflowError) as e: error(e)
