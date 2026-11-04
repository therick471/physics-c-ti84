from math import sqrt, sin, cos, exp, pi
from APCORE import menu, head, info, number, calc, result, error, Cancel, CONST, valid_geometry, solve_formula

def samples(f, lo, hi, count=80):
    if lo >= hi or count < 2 or count > 100:
        raise ValueError('Need low<high; 2..100 points')
    # Segments prevent drawing straight lines across undefined samples.
    segments, xs, ys = [],[],[]
    for i in range(count):
        x = lo+(hi-lo)*i/(count-1)
        try:
            y = f(x)
            if y != y or abs(y) > 1e100:
                raise ValueError('Unbounded')
            xs.append(x)
            ys.append(y)
        except (ValueError,ZeroDivisionError,OverflowError):
            if xs:
                segments.append((xs,ys))
            xs,ys = [],[]
    if xs:
        segments.append((xs,ys))
    return segments

def draw(title, series, xl='x', yl='y'):
    try:
        import ti_plotlib as plt
    except ImportError:
        info('Graph preview', 'ti_plotlib is available on the calculator. Desktop mode shows sampled values only.')
        for label,segments in series:
            pairs = []
            for xs,ys in segments:
                for i in range(0,len(xs),max(1,len(xs)//5)):
                    pairs.append((label+' x='+str(round(xs[i],4)),ys[i]))
            result(title,pairs[:10])
        return
    xmin,xmax,ymin,ymax = None,None,None,None
    for label,segments in series:
        for xs,ys in segments:
            for i in range(len(xs)):
                x,y = xs[i],ys[i]
                if xmin is None:
                    xmin,xmax,ymin,ymax = x,x,y,y
                else:
                    xmin,xmax = min(xmin,x),max(xmax,x)
                    ymin,ymax = min(ymin,y),max(ymax,y)
    if xmin is None:
        raise ValueError('No defined points in window')
    dx = (xmax-xmin)*.06 if xmax != xmin else max(1,abs(xmin)*.06)
    dy = (ymax-ymin)*.12 if ymax != ymin else max(1,abs(ymin)*.12)
    plt.cls()
    plt.window(xmin-dx,xmax+dx,ymin-dy,ymax+dy)
    plt.axes('on')
    plt.grid((xmax-xmin+2*dx)/5,(ymax-ymin+2*dy)/5,'dot')
    plt.title(title[:25])
    plt.labels(xl[:15],yl[:15],11,2)
    plt.pen('thin','solid')
    colors = [(0,100,220),(220,60,40),(30,160,70)]
    for j in range(len(series)):
        rgb = colors[j%3]
        plt.color(rgb[0],rgb[1],rgb[2])
        for xs,ys in series[j][1]:
            if len(xs)>1:
                plt.plot(xs,ys,'')
            else:
                plt.plot(xs[0],ys[0],'o')
    plt.show_plot()

def plot_formula(entry):
    title,eq,specs,inverses,note = entry[:5]
    yidx = menu('Plot vertical variable',[s[0]+' '+s[2] for s in specs])
    if yidx < 0:
        return
    options = [i for i in range(len(specs)) if i != yidx]
    xpick = menu('Plot horizontal variable',[specs[i][0]+' '+specs[i][2] for i in options])
    if xpick < 0:
        return
    xidx = options[xpick]
    if not inverses[yidx]:
        info('Choose another axis','This vertical variable uses numerical solving. Choose a variable with an explicit inverse, or use custom f(x).')
        return
    branch = 0
    if len(inverses[yidx]) > 1:
        branch = menu('Algebraic branch',['Root '+str(i+1)+' (ascending)' for i in range(len(inverses[yidx]))])
        if branch < 0:
            return
    vals = {}
    head('Fixed parameters')
    for i in range(len(specs)):
        if i not in (xidx,yidx):
            vals[specs[i][0]] = number(specs[i][0]+' '+specs[i][2],specs[i][3])
    lo,hi = number('x axis LOW'),number('x axis HIGH')
    xd,yd = specs[xidx][3],specs[yidx][3]
    def f(x):
        if (xd=='+' and x<=0) or (xd=='0' and x<0):
            raise ValueError('Domain')
        vals[specs[xidx][0]] = x
        roots = solve_formula(entry,yidx,vals)
        roots.sort()
        if len(roots) <= branch:
            raise ValueError('Branch undefined')
        y = roots[branch]
        if (yd=='+' and y<=0) or (yd=='0' and y<0):
            raise ValueError('Domain')
        vals[specs[yidx][0]] = y
        if not valid_geometry(entry,vals):
            raise ValueError('Geometry')
        return y
    info('Plot note',note+'\nSampled graph; poles, narrow peaks and oscillations can be missed. Use a smaller interval to inspect.')
    draw(title,[(specs[yidx][0],samples(f,lo,hi))],specs[xidx][0]+' '+specs[xidx][2],specs[yidx][0]+' '+specs[yidx][2])

def main():
    items = ['Custom f(x) and g(x)','Projectile trajectory','Motion x(t), v(t), a(t)',
             'SHM position / velocity','RC voltage response','RL current response','Electric E(r) or V(r)']
    while True:
        i = menu('Graphs',items)
        if i < 0:
            return
        try:
            head(items[i])
            if i == 0:
                info('Graph syntax','Use explicit *, ^ for powers, radians; x is horizontal variable. Two curves: blue=f, red=g. Sampled graphs may miss poles or rapid changes.')
                s = input('f(x): ').strip()
                if s == 'q':
                    raise Cancel()
                t = input('g(x) or ENTER: ').strip()
                lo,hi = number('LOW x'),number('HIGH x')
                series = [('f',samples(lambda x:calc(s,{'x':x}),lo,hi))]
                if t:
                    series.append(('g',samples(lambda x:calc(t,{'x':x}),lo,hi)))
                draw('Blue f / red g',series)
            elif i == 1:
                from APTOOLS import projectile
                v,angle = number('speed m/s','0'),number('angle rad')
                y0,yf,g = number('launch y m'),number('land y m'),number('g','+',CONST['g'])
                time = projectile(v,angle,y0,yf,g)[0][1]
                xs = [v*cos(angle)*time*j/79 for j in range(80)]
                ys = [y0+v*sin(angle)*time*j/79-g*(time*j/79)**2/2 for j in range(80)]
                draw('Projectile', [('path',[(xs,ys)])],'x m','y m')
            elif i == 2:
                x0,u,a = number('x0 m'),number('v0 m/s'),number('a m/s^2')
                hi = number('End time s','+')
                k = menu('Vertical axis',['Position m','Velocity m/s','Acceleration m/s^2'])
                if k < 0:
                    continue
                funcs = [lambda t:x0+u*t+a*t*t/2,lambda t:u+a*t,lambda t:a]
                draw('Motion',[('motion',samples(funcs[k],0,hi))],'time s',['x m','v m/s','a m/s^2'][k])
            elif i == 3:
                amp,w,ph = number('amp m','0'),number('omega rad/s','+'),number('phase rad')
                hi = number('End time s','+',4*pi/w)
                k = menu('Vertical axis',['Position','Velocity','Acceleration'])
                if k < 0:
                    continue
                funcs = [lambda t:amp*cos(w*t+ph),lambda t:-amp*w*sin(w*t+ph),lambda t:-amp*w*w*cos(w*t+ph)]
                draw('SHM',[('SHM',samples(funcs[k],0,hi))],'time s',['x m','v m/s','a m/s^2'][k])
            elif i in (4,5):
                res = number('R ohm','+')
                val = number('C farad' if i==4 else 'L henry','+')
                tau = res*val if i==4 else val/res
                initial = number('Initial V' if i==4 else 'Initial I A')
                final = number('Final V' if i==4 else 'Final I A')
                hi = number('End time s','+',5*tau)
                draw('RC' if i==4 else 'RL',[('response',samples(lambda t:final+(initial-final)*exp(-t/tau),0,hi))],
                     'time s','Vc V' if i==4 else 'I A')
            elif i == 6:
                from APTOOLS import sphere
                typ = menu('Source',['Point charge','Uniform solid sphere','Conductor / shell'])
                if typ < 0:
                    continue
                q = number('Charge C')
                radius = number('Sphere R m','+') if typ else 1
                axis = menu('Vertical axis',['E radial N/C','V volts'])
                if axis < 0:
                    continue
                lo,hi = number('LOW r m','0'),number('HIGH r m','+')
                def f(r):
                    if typ:
                        return sphere(q,radius,r,typ==2)[axis]
                    return CONST['ke']*q/(r*r if axis==0 else r)
                # A conductor surface is discontinuous; don't connect through it.
                if typ==2 and axis==0 and lo<radius<hi:
                    seg = samples(f,lo,radius*(1-1e-8))+samples(f,radius,hi)
                else:
                    seg = samples(f,lo,hi)
                draw('Radial electrostatics',[('field',seg)],'r m','E N/C' if axis==0 else 'V volts')
        except Cancel:
            pass
        except (ValueError,ZeroDivisionError,OverflowError) as e:
            error(e)
