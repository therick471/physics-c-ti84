from math import sqrt, sin, cos, atan2, exp, pi
from APCORE import CONST, number, integer, menu, head, info, result, Cancel, error
from APNUM import quadratic, linear

def rc(res, cap, initial, final, t):
    if res <= 0 or cap <= 0 or t < 0:
        raise ValueError('Need R,C>0; t>=0')
    tau = res * cap
    v = final + (initial - final) * exp(-t / tau)
    cur = (final - initial) / res * exp(-t / tau)
    return [('tau s', tau), ('Vc V', v), ('I A', cur), ('Q C', cap * v), ('U J', cap * v * v / 2)]

def rl(res, ind, initial, source, t):
    if res <= 0 or ind <= 0 or t < 0:
        raise ValueError('Need R,L>0; t>=0')
    tau = ind / res
    final = source / res
    cur = final + (initial - final) * exp(-t / tau)
    vl = (source - res * initial) * exp(-t / tau)
    return [('tau s', tau), ('I A', cur), ('VL V', vl), ('VR V', res * cur), ('U J', ind * cur * cur / 2)]

def charges(sources, x, y):
    ex, ey, voltage = (0.0, 0.0, 0.0)
    for q, sx, sy in sources:
        dx, dy = (x - sx, y - sy)
        r2 = dx * dx + dy * dy
        if r2 == 0:
            raise ValueError('Target at a point charge')
        r = sqrt(r2)
        ex += CONST['ke'] * q * dx / (r2 * r)
        ey += CONST['ke'] * q * dy / (r2 * r)
        voltage += CONST['ke'] * q / r
    return (ex, ey, voltage)

def sphere(q, radius, r, conducting):
    if radius <= 0 or r < 0:
        raise ValueError('Need R>0; r>=0')
    kq = CONST['ke'] * q
    if r >= radius:
        return (kq / (r * r), kq / r)
    if conducting:
        return (0.0, kq / radius)
    return (kq * r / radius ** 3, kq * (3 - r * r / (radius * radius)) / (2 * radius))

def equivalent(values, kind, connection):
    if not values or min(values) <= 0:
        raise ValueError('Every component must be >0')
    add = kind == 'R' and connection == 'series' or (kind == 'C' and connection == 'parallel')
    return sum(values) if add else 1 / sum([1 / v for v in values])

def network(nodes, resistors, sources):
    n = nodes + len(sources)
    if nodes < 1 or nodes > 6 or len(sources) > 4:
        raise ValueError('1..6 nodes, max 4 sources')
    a = [[0.0] * n for i in range(n)]
    b = [0.0] * n
    for na, nb, res in resistors:
        if min(na, nb) < 0 or max(na, nb) > nodes or na == nb or (res <= 0):
            raise ValueError('Invalid resistor')
        conductance = 1 / res
        for nd in (na, nb):
            if nd:
                a[nd - 1][nd - 1] += conductance
        if na and nb:
            a[na - 1][nb - 1] -= conductance
            a[nb - 1][na - 1] -= conductance
    for j in range(len(sources)):
        na, nb, emf = sources[j]
        if min(na, nb) < 0 or max(na, nb) > nodes or na == nb:
            raise ValueError('Invalid source')
        k = nodes + j
        if na:
            a[na - 1][k] = 1
            a[k][na - 1] = 1
        if nb:
            a[nb - 1][k] = -1
            a[k][nb - 1] = -1
        b[k] = emf
    sol = linear(a, b)
    voltage = [0.0] + sol[:nodes]
    currents = [(voltage[na] - voltage[nb]) / res for na, nb, res in resistors]
    return (voltage, currents, sol[nodes:])

def charges_ui():
    head('Point charges 2D')
    n = integer('Charge count', 1, 12)
    sources = []
    for i in range(n):
        head('Source ' + str(i + 1))
        sources.append((number('q C'), number('x m'), number('y m')))
    while True:
        head('Target point | q Back')
        x, y = (number('x m'), number('y m'))
        testq = number('Test q C (0=field only)')
        ex, ey, v = charges(sources, x, y)
        result('Superposition', [('Ex N/C', ex), ('Ey N/C', ey), ('|E| N/C', sqrt(ex * ex + ey * ey)), ('V volts', v), ('Fx N', testq * ex), ('Fy N', testq * ey), ('U test J', testq * v)])
        if menu('Reuse sources?', ['New target']) < 0:
            return

def network_ui():
    info('DC circuit', 'Resistors and ideal voltage sources only. Label ground 0 and other nodes 1..N. A source enforces Va-Vb=emf. All branch currents positive from a to b. No floating nodes. For capacitors at DC steady state: open. Inductors: wire.')
    head('Circuit sizes')
    n = integer('Non-ground node count', 1, 6)
    nr = integer('Resistor count', 1, 12)
    ns = integer('Voltage source count', 0, 4)
    resistors, sources = ([], [])
    for i in range(nr):
        head('Resistor ' + str(i + 1))
        resistors.append((integer('Node a', 0, n), integer('Node b', 0, n), number('R ohm', '+')))
    for i in range(ns):
        head('Source ' + str(i + 1))
        sources.append((integer('Node a (+)', 0, n), integer('Node b (-)', 0, n), number('emf V')))
    v, ir, iv = network(n, resistors, sources)
    pairs = [('V' + str(i) + ' V', v[i]) for i in range(1, n + 1)]
    pairs += [('R' + str(i + 1) + ' I A', ir[i]) for i in range(nr)]
    pairs += [('Src' + str(i + 1) + ' I A', iv[i]) for i in range(ns)]
    result('DC solution', pairs, 'Negative current means b to a.')

def equivalent_ui():
    kind = menu('Component', ['Resistors ohm', 'Capacitors F'])
    if kind < 0:
        return
    conn = menu('Connection', ['Series', 'Parallel'])
    if conn < 0:
        return
    head('Equivalent')
    n = integer('Component count', 1, 20)
    values = [number(str(i + 1) + ' value', '+') for i in range(n)]
    result('Equivalent', [('Req ohm' if kind == 0 else 'Ceq F', equivalent(values, 'R' if kind == 0 else 'C', 'series' if conn == 0 else 'parallel'))], 'For mixed networks reduce one group, then use ans as an input to the next group.')

def run_tool(which):
    if which == 6:
        charges_ui()
    if which == 7:
        choice = menu('Sphere', ['Uniform solid charge', 'Conductor / thin shell'])
        if choice < 0:
            return
        head('Sphere E and V')
        ef, v = sphere(number('Total Q C'), number('Sphere R m', '+'), number('Target r m', '0'), choice == 1)
        result('Sphere', [('Er N/C', ef), ('V volts', v)], 'V infinity=0. At surface uses outside E; conductor just inside has E=0.')
    if which == 8:
        equivalent_ui()
    if which == 9:
        network_ui()
    if which == 10:
        head('RC step response')
        result('RC', rc(number('R ohm', '+'), number('C farad', '+'), number('initial Vc V'), number('final/source V V'), number('t s', '0')), 'Current positive INTO reference capacitor plate. Final V=0 for discharge.')
    if which == 11:
        head('RL step response')
        result('RL', rl(number('R ohm', '+'), number('L henry', '+'), number('initial current A'), number('source voltage V'), number('t s', '0')), 'Source V=0 for decay; VL referenced in current direction.')
    if which == 14:
        head('Faraday / motional rod')
        b, l, v = (number('B tesla'), number('Rod l m', '+'), number('speed m/s'))
        res = number('Circuit R ohm', '+')
        emf = b * l * v
        result('Moving rod', [('emf magnitude V', abs(emf)), ('I magnitude A', abs(emf / res)), ('Drag magnitude N', abs(b * l * emf / res)), ('Dissipation W', emf * emf / res)], 'Rod, velocity and field perpendicular. Direction from v cross B and Lenz law.')
