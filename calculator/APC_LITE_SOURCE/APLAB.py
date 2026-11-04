from math import sqrt, sin, cos, atan2, exp, pi
from APCORE import CONST, number, integer, menu, head, info, result, Cancel, error
from APNUM import quadratic, linear

def regress(xs, ys):
    n = len(xs)
    if n < 2 or len(ys) != n:
        raise ValueError('Need at least 2 paired points')
    xm, ym = (sum(xs) / n, sum(ys) / n)
    sxx = sum([(x - xm) ** 2 for x in xs])
    if sxx == 0:
        raise ValueError('x values all equal')
    slope = sum([(xs[i] - xm) * (ys[i] - ym) for i in range(n)]) / sxx
    intercept = ym - slope * xm
    ssres = sum([(ys[i] - slope * xs[i] - intercept) ** 2 for i in range(n)])
    sst = sum([(y - ym) ** 2 for y in ys])
    r2 = 1 - ssres / sst if sst else 1.0 if ssres == 0 else 0.0
    return (slope, intercept, r2)

def vector_ui():
    head('Vectors 3D')
    a = [number('A' + k) for k in ('x', 'y', 'z')]
    b = [number('B' + k) for k in ('x', 'y', 'z')]
    dot = sum([a[i] * b[i] for i in range(3)])
    cross = [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
    result('Vectors', [('|A|', sqrt(sum([v * v for v in a]))), ('|B|', sqrt(sum([v * v for v in b]))), ('A dot B', dot), ('cross x', cross[0]), ('cross y', cross[1]), ('cross z', cross[2])])

def data_ui():
    head('Linear fit y = m*x + b')
    n = integer('Point count', 2, 20)
    xs, ys = ([], [])
    for i in range(n):
        print('Point ' + str(i + 1))
        xs.append(number('x'))
        ys.append(number('y'))
    m, b, r2 = regress(xs, ys)
    result('Linear fit', [('slope', m), ('intercept', b), ('R^2', r2)], 'Units of slope are y-unit/x-unit. Linearize first if the physical model requires it.')

def run_tool(which):
    if which == 13:
        data_ui()
    if which == 0:
        vector_ui()
