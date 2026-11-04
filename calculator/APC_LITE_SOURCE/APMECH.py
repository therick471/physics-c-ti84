from math import sqrt, sin, cos, atan2, exp, pi
from APCORE import CONST, number, integer, menu, head, info, result, Cancel, error
from APNUM import quadratic, linear

def projectile(v, angle, y0, yf, g):
    if v < 0 or g <= 0:
        raise ValueError('Need speed>=0 and g>0')
    vx, vy = (v * cos(angle), v * sin(angle))
    times = [t for t in quadratic(-g / 2, vy, y0 - yf) if t >= 0]
    if not times:
        raise ValueError('Landing height never reached at t>=0')
    t = max(times)
    peak_t = min(t, max(0.0, vy / g))
    vyf = vy - g * t
    return [('flight s', t), ('dx m', vx * t), ('vx m/s', vx), ('vy final m/s', vyf), ('speed final m/s', sqrt(vx * vx + vyf * vyf)), ('peak y m', y0 + vy * peak_t - g * peak_t * peak_t / 2)]

def collision(m1, m2, u1, u2, e):
    if m1 <= 0 or m2 <= 0 or e < 0 or (e > 1):
        raise ValueError('Masses>0; restitution 0..1')
    p = m1 * u1 + m2 * u2
    v1 = (p - m2 * e * (u1 - u2)) / (m1 + m2)
    v2 = (p + m1 * e * (u1 - u2)) / (m1 + m2)
    ki, kf = ((m1 * u1 * u1 + m2 * u2 * u2) / 2, (m1 * v1 * v1 + m2 * v2 * v2) / 2)
    return [('v1 m/s', v1), ('v2 m/s', v2), ('p kg*m/s', p), ('Ki J', ki), ('Kf J', kf), ('K lost J', ki - kf)]

def atwood(m1, m2, inertia, radius, g):
    if min(m1, m2, radius, g) <= 0 or inertia < 0:
        raise ValueError('Positive m,r,g; I>=0')
    a = (m2 - m1) * g / (m1 + m2 + inertia / (radius * radius))
    return [('a m/s^2', a), ('T1 N', m1 * (g + a)), ('T2 N', m2 * (g - a)), ('alpha rad/s^2', a / radius)]

def shm(m, ks, x0, v0, t):
    if m <= 0 or ks <= 0:
        raise ValueError('Need m,k>0')
    w = sqrt(ks / m)
    a = sqrt(x0 * x0 + (v0 / w) ** 2)
    phase = atan2(-v0 / w, x0) if a else 0.0
    x = x0 * cos(w * t) + v0 / w * sin(w * t)
    v = -x0 * w * sin(w * t) + v0 * cos(w * t)
    return [('omega rad/s', w), ('period s', 2 * pi / w), ('amp m', a), ('phase rad', phase), ('x m', x), ('v m/s', v), ('a m/s^2', -w * w * x), ('K J', m * v * v / 2), ('U J', ks * x * x / 2), ('E J', ks * a * a / 2)]

def vector_ui():
    head('Vectors 3D')
    a = [number('A' + k) for k in ('x', 'y', 'z')]
    b = [number('B' + k) for k in ('x', 'y', 'z')]
    dot = sum([a[i] * b[i] for i in range(3)])
    cross = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    result('Vectors', [('|A|', sqrt(sum([v * v for v in a]))), ('|B|', sqrt(sum([v * v for v in b]))), ('A dot B', dot), ('cross x', cross[0]), ('cross y', cross[1]), ('cross z', cross[2])])

def com_ui():
    head('COM / total momentum')
    n = integer('Number of masses', 1, 12)
    mass, mx, my, px, py = (0.0, 0.0, 0.0, 0.0, 0.0)
    for i in range(n):
        head('Mass ' + str(i + 1))
        m = number('m kg', '+')
        x, y = (number('x m'), number('y m'))
        vx, vy = (number('vx m/s'), number('vy m/s'))
        mass += m
        mx += m * x
        my += m * y
        px += m * vx
        py += m * vy
    result('COM', [('M kg', mass), ('COM x m', mx / mass), ('COM y m', my / mass), ('px kg*m/s', px), ('py kg*m/s', py), ('COM vx m/s', px / mass), ('COM vy m/s', py / mass)])

def run_tool(which):
    if which == 0:
        vector_ui()
    if which == 1:
        head('Projectile | angles rad')
        result('Projectile', projectile(number('speed m/s', '0'), number('launch angle rad'), number('launch y m'), number('landing y m'), number('g m/s^2', '+', CONST['g'])), 'No air resistance; last nonnegative crossing used.')
    if which == 2:
        head('Collision 1D')
        result('Collision', collision(number('m1 kg', '+'), number('m2 kg', '+'), number('u1 m/s'), number('u2 m/s'), number('e (0 stick,1 elastic)', '0')), 'Assumes an actual impact and negligible external impulse.')
    if which == 3:
        com_ui()
    if which == 4:
        head('Atwood + pulley')
        result('Atwood', atwood(number('m1 kg', '+'), number('m2 kg', '+'), number('Pulley I kg*m^2', '0'), number('Pulley radius m', '+'), number('g m/s^2', '+', CONST['g'])), 'a positive: m2 down, m1 up. No slip; massless string; frictionless axle.')
    if which == 5:
        head('SHM initial state')
        result('SHM', shm(number('m kg', '+'), number('spring k N/m', '+'), number('initial x m'), number('initial v m/s'), number('time s', '0')), 'x from equilibrium. No damping; phase for x=A*cos(w*t+phase).')
    if which == 12:
        head('Rolling down incline')
        beta = number('I/(m*r^2)', '0')
        th = number('Incline rad')
        h = number('Vertical drop m', '0')
        g = number('g m/s^2', '+', CONST['g'])
        result('Rolling', [('a m/s^2', g * sin(th) / (1 + beta)), ('v final m/s', sqrt(2 * g * h / (1 + beta))), ('Krot / Ktotal', beta / (1 + beta))], 'Starts at rest; rolls without slipping. beta: hoop 1, disk .5, solid sphere .4, spherical shell 2/3.')
