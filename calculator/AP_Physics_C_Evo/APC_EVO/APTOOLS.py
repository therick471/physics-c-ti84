from math import sqrt, sin, cos, atan2, exp, pi
from APCORE import CONST, number, integer, menu, head, info, result, quadratic, linear, Cancel, error

def projectile(v, angle, y0, yf, g):
    if v < 0 or g <= 0:
        raise ValueError('Need speed>=0 and g>0')
    vx, vy = v*cos(angle), v*sin(angle)
    times = [t for t in quadratic(-g/2, vy, y0-yf) if t >= 0]
    if not times:
        raise ValueError('Landing height never reached at t>=0')
    t = max(times)
    peak_t = min(t, max(0.0, vy/g))
    vyf = vy-g*t
    return [('flight s', t), ('dx m', vx*t), ('vx m/s', vx),
            ('vy final m/s', vyf), ('speed final m/s', sqrt(vx*vx+vyf*vyf)),
            ('peak y m', y0+vy*peak_t-g*peak_t*peak_t/2)]

def collision(m1, m2, u1, u2, e):
    if m1 <= 0 or m2 <= 0 or e < 0 or e > 1:
        raise ValueError('Masses>0; restitution 0..1')
    p = m1*u1+m2*u2
    v1 = (p-m2*e*(u1-u2))/(m1+m2)
    v2 = (p+m1*e*(u1-u2))/(m1+m2)
    ki, kf = (m1*u1*u1+m2*u2*u2)/2, (m1*v1*v1+m2*v2*v2)/2
    return [('v1 m/s', v1), ('v2 m/s', v2), ('p kg*m/s', p),
            ('Ki J', ki), ('Kf J', kf), ('K lost J', ki-kf)]

def atwood(m1, m2, inertia, radius, g):
    if min(m1, m2, radius, g) <= 0 or inertia < 0:
        raise ValueError('Positive m,r,g; I>=0')
    a = (m2-m1)*g/(m1+m2+inertia/(radius*radius))
    return [('a m/s^2', a), ('T1 N', m1*(g+a)),
            ('T2 N', m2*(g-a)), ('alpha rad/s^2', a/radius)]

def shm(m, ks, x0, v0, t):
    if m <= 0 or ks <= 0:
        raise ValueError('Need m,k>0')
    w = sqrt(ks/m)
    a = sqrt(x0*x0+(v0/w)**2)
    phase = atan2(-v0/w, x0) if a else 0.0
    x = x0*cos(w*t)+v0/w*sin(w*t)
    v = -x0*w*sin(w*t)+v0*cos(w*t)
    return [('omega rad/s', w), ('period s', 2*pi/w), ('amp m', a),
            ('phase rad', phase), ('x m', x), ('v m/s', v), ('a m/s^2', -w*w*x),
            ('K J', m*v*v/2), ('U J', ks*x*x/2), ('E J', ks*a*a/2)]

def rc(res, cap, initial, final, t):
    if res <= 0 or cap <= 0 or t < 0:
        raise ValueError('Need R,C>0; t>=0')
    tau = res*cap
    v = final+(initial-final)*exp(-t/tau)
    cur = (final-initial)/res*exp(-t/tau)
    return [('tau s', tau), ('Vc V', v), ('I A', cur),
            ('Q C', cap*v), ('U J', cap*v*v/2)]

def rl(res, ind, initial, source, t):
    if res <= 0 or ind <= 0 or t < 0:
        raise ValueError('Need R,L>0; t>=0')
    tau = ind/res
    final = source/res
    cur = final+(initial-final)*exp(-t/tau)
    vl = (source-res*initial)*exp(-t/tau)
    return [('tau s', tau), ('I A', cur), ('VL V', vl),
            ('VR V', res*cur), ('U J', ind*cur*cur/2)]

def charges(sources, x, y):
    ex, ey, voltage = 0.0, 0.0, 0.0
    for q, sx, sy in sources:
        dx, dy = x-sx, y-sy
        r2 = dx*dx+dy*dy
        if r2 == 0:
            raise ValueError('Target at a point charge')
        r = sqrt(r2)
        ex += CONST['ke']*q*dx/(r2*r)
        ey += CONST['ke']*q*dy/(r2*r)
        voltage += CONST['ke']*q/r
    return ex, ey, voltage

def sphere(q, radius, r, conducting):
    if radius <= 0 or r < 0:
        raise ValueError('Need R>0; r>=0')
    kq = CONST['ke']*q
    if r >= radius:
        return kq/(r*r), kq/r
    if conducting:
        return 0.0, kq/radius
    return kq*r/(radius**3), kq*(3-r*r/(radius*radius))/(2*radius)

def equivalent(values, kind, connection):
    if not values or min(values) <= 0:
        raise ValueError('Every component must be >0')
    add = (kind == 'R' and connection == 'series') or (kind == 'C' and connection == 'parallel')
    return sum(values) if add else 1/sum([1/v for v in values])

def network(nodes, resistors, sources):
    # Modified nodal analysis. Ground=0, sources enforce Va-Vb=emf.
    n = nodes+len(sources)
    if nodes < 1 or nodes > 6 or len(sources) > 4:
        raise ValueError('1..6 nodes, max 4 sources')
    a = [[0.0]*n for i in range(n)]
    b = [0.0]*n
    for na, nb, res in resistors:
        if min(na,nb) < 0 or max(na,nb) > nodes or na == nb or res <= 0:
            raise ValueError('Invalid resistor')
        conductance = 1/res
        for nd in (na, nb):
            if nd:
                a[nd-1][nd-1] += conductance
        if na and nb:
            a[na-1][nb-1] -= conductance
            a[nb-1][na-1] -= conductance
    for j in range(len(sources)):
        na, nb, emf = sources[j]
        if min(na,nb) < 0 or max(na,nb) > nodes or na == nb:
            raise ValueError('Invalid source')
        k = nodes+j
        if na:
            a[na-1][k] = 1
            a[k][na-1] = 1
        if nb:
            a[nb-1][k] = -1
            a[k][nb-1] = -1
        b[k] = emf
    sol = linear(a,b)
    voltage = [0.0]+sol[:nodes]
    currents = [(voltage[na]-voltage[nb])/res for na,nb,res in resistors]
    return voltage, currents, sol[nodes:]

def regress(xs, ys):
    n = len(xs)
    if n < 2 or len(ys) != n:
        raise ValueError('Need at least 2 paired points')
    xm, ym = sum(xs)/n, sum(ys)/n
    sxx = sum([(x-xm)**2 for x in xs])
    if sxx == 0:
        raise ValueError('x values all equal')
    slope = sum([(xs[i]-xm)*(ys[i]-ym) for i in range(n)])/sxx
    intercept = ym-slope*xm
    ssres = sum([(ys[i]-slope*xs[i]-intercept)**2 for i in range(n)])
    sst = sum([(y-ym)**2 for y in ys])
    r2 = 1-ssres/sst if sst else (1.0 if ssres == 0 else 0.0)
    return slope, intercept, r2

def vector_ui():
    head('Vectors 3D')
    a = [number('A'+k) for k in ('x','y','z')]
    b = [number('B'+k) for k in ('x','y','z')]
    dot = sum([a[i]*b[i] for i in range(3)])
    cross = [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]
    result('Vectors', [('|A|',sqrt(sum([v*v for v in a]))), ('|B|',sqrt(sum([v*v for v in b]))),
                       ('A dot B',dot), ('cross x',cross[0]), ('cross y',cross[1]), ('cross z',cross[2])])

def com_ui():
    head('COM / total momentum')
    n = integer('Number of masses',1,12)
    mass, mx, my, px, py = 0.0,0.0,0.0,0.0,0.0
    for i in range(n):
        head('Mass '+str(i+1))
        m = number('m kg','+')
        x,y = number('x m'),number('y m')
        vx,vy = number('vx m/s'),number('vy m/s')
        mass += m
        mx += m*x
        my += m*y
        px += m*vx
        py += m*vy
    result('COM', [('M kg',mass),('COM x m',mx/mass),('COM y m',my/mass),
                   ('px kg*m/s',px),('py kg*m/s',py),('COM vx m/s',px/mass),('COM vy m/s',py/mass)])

def charges_ui():
    head('Point charges 2D')
    n = integer('Charge count',1,12)
    sources = []
    for i in range(n):
        head('Source '+str(i+1))
        sources.append((number('q C'),number('x m'),number('y m')))
    while True:
        head('Target point | q Back')
        x,y = number('x m'),number('y m')
        testq = number('Test q C (0=field only)')
        ex,ey,v = charges(sources,x,y)
        result('Superposition', [('Ex N/C',ex),('Ey N/C',ey),('|E| N/C',sqrt(ex*ex+ey*ey)),
                                 ('V volts',v),('Fx N',testq*ex),('Fy N',testq*ey),('U test J',testq*v)])
        if menu('Reuse sources?', ['New target']) < 0:
            return

def network_ui():
    info('DC circuit', 'Resistors and ideal voltage sources only. Label ground 0 and other nodes 1..N. A source enforces Va-Vb=emf. All branch currents positive from a to b. No floating nodes. For capacitors at DC steady state: open. Inductors: wire.')
    head('Circuit sizes')
    n = integer('Non-ground node count',1,6)
    nr = integer('Resistor count',1,12)
    ns = integer('Voltage source count',0,4)
    resistors,sources = [],[]
    for i in range(nr):
        head('Resistor '+str(i+1))
        resistors.append((integer('Node a',0,n),integer('Node b',0,n),number('R ohm','+')))
    for i in range(ns):
        head('Source '+str(i+1))
        sources.append((integer('Node a (+)',0,n),integer('Node b (-)',0,n),number('emf V')))
    v, ir, iv = network(n,resistors,sources)
    pairs = [('V'+str(i)+' V',v[i]) for i in range(1,n+1)]
    pairs += [('R'+str(i+1)+' I A',ir[i]) for i in range(nr)]
    pairs += [('Src'+str(i+1)+' I A',iv[i]) for i in range(ns)]
    result('DC solution',pairs,'Negative current means b to a.')

def equivalent_ui():
    kind = menu('Component', ['Resistors ohm','Capacitors F'])
    if kind < 0:
        return
    conn = menu('Connection',['Series','Parallel'])
    if conn < 0:
        return
    head('Equivalent')
    n = integer('Component count',1,20)
    values = [number(str(i+1)+' value','+') for i in range(n)]
    result('Equivalent', [('Req ohm' if kind == 0 else 'Ceq F', equivalent(values,'R' if kind==0 else 'C','series' if conn==0 else 'parallel'))],
           'For mixed networks reduce one group, then use ans as an input to the next group.')

def data_ui():
    head('Linear fit y = m*x + b')
    n = integer('Point count',2,20)
    xs,ys = [],[]
    for i in range(n):
        print('Point '+str(i+1))
        xs.append(number('x'))
        ys.append(number('y'))
    m,b,r2 = regress(xs,ys)
    result('Linear fit',[('slope',m),('intercept',b),('R^2',r2)],'Units of slope are y-unit/x-unit. Linearize first if the physical model requires it.')

def run_tool(which):
    if which == 0:
        vector_ui()
    elif which == 1:
        head('Projectile | angles rad')
        result('Projectile',projectile(number('speed m/s','0'),number('launch angle rad'),number('launch y m'),number('landing y m'),number('g m/s^2','+',CONST['g'])), 'No air resistance; last nonnegative crossing used.')
    elif which == 2:
        head('Collision 1D')
        result('Collision',collision(number('m1 kg','+'),number('m2 kg','+'),number('u1 m/s'),number('u2 m/s'),number('e (0 stick,1 elastic)','0')), 'Assumes an actual impact and negligible external impulse.')
    elif which == 3:
        com_ui()
    elif which == 4:
        head('Atwood + pulley')
        result('Atwood',atwood(number('m1 kg','+'),number('m2 kg','+'),number('Pulley I kg*m^2','0'),number('Pulley radius m','+'),number('g m/s^2','+',CONST['g'])), 'a positive: m2 down, m1 up. No slip; massless string; frictionless axle.')
    elif which == 5:
        head('SHM initial state')
        result('SHM',shm(number('m kg','+'),number('spring k N/m','+'),number('initial x m'),number('initial v m/s'),number('time s','0')), 'x from equilibrium. No damping; phase for x=A*cos(w*t+phase).')
    elif which == 6:
        charges_ui()
    elif which == 7:
        choice = menu('Sphere',['Uniform solid charge','Conductor / thin shell'])
        if choice < 0:
            return
        head('Sphere E and V')
        ef,v = sphere(number('Total Q C'),number('Sphere R m','+'),number('Target r m','0'),choice==1)
        result('Sphere',[('Er N/C',ef),('V volts',v)], 'V infinity=0. At surface uses outside E; conductor just inside has E=0.')
    elif which == 8:
        equivalent_ui()
    elif which == 9:
        network_ui()
    elif which == 10:
        head('RC step response')
        result('RC',rc(number('R ohm','+'),number('C farad','+'),number('initial Vc V'),number('final/source V V'),number('t s','0')), 'Current positive INTO reference capacitor plate. Final V=0 for discharge.')
    elif which == 11:
        head('RL step response')
        result('RL',rl(number('R ohm','+'),number('L henry','+'),number('initial current A'),number('source voltage V'),number('t s','0')), 'Source V=0 for decay; VL referenced in current direction.')
    elif which == 12:
        head('Rolling down incline')
        beta = number('I/(m*r^2)','0')
        th = number('Incline rad')
        h = number('Vertical drop m','0')
        g = number('g m/s^2','+',CONST['g'])
        result('Rolling',[('a m/s^2',g*sin(th)/(1+beta)),('v final m/s',sqrt(2*g*h/(1+beta))),
                          ('Krot / Ktotal',beta/(1+beta))], 'Starts at rest; rolls without slipping. beta: hoop 1, disk .5, solid sphere .4, spherical shell 2/3.')
    elif which == 13:
        data_ui()
    elif which == 14:
        head('Faraday / motional rod')
        b,l,v = number('B tesla'),number('Rod l m','+'),number('speed m/s')
        res = number('Circuit R ohm','+')
        emf = b*l*v
        result('Moving rod',[('emf magnitude V',abs(emf)),('I magnitude A',abs(emf/res)),
                             ('Drag magnitude N',abs(b*l*emf/res)),('Dissipation W',emf*emf/res)], 'Rod, velocity and field perpendicular. Direction from v cross B and Lenz law.')

NAMES = ['Vectors: dot / cross','Projectile: full flight','Collision: elastic / stick','COM / total momentum',
         'Atwood + massive pulley','SHM from initial state','Charges: E / V / force','Sphere: inside / outside',
         'Equivalent R or C','DC circuit: multiple cells','RC charge / discharge','RL rise / decay',
         'Rolling incline','Lab linear regression','Motional emf / drag']

def main():
    while True:
        i = menu('Multi-step tools',NAMES)
        if i < 0:
            return
        try:
            run_tool(i)
        except Cancel:
            pass
        except (ValueError,ZeroDivisionError,OverflowError) as e:
            error(e)
