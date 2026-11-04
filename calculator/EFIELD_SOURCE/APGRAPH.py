from APCORE import menu, head, info, number, calc, error, Cancel, CONST
from math import sin, cos, sqrt, pi

def samples(f, lo, hi, count=40):
    if lo >= hi or count < 2 or count > 100:
        raise ValueError('Need low<high; 2..100 points')
    segments = []
    xs = []
    ys = []
    for i in range(count):
        x = lo + (hi - lo) * i / (count - 1)
        try:
            y = f(x)
            if y != y or abs(y) > 1e+100:
                raise ValueError('Unbounded')
            xs.append(x)
            ys.append(y)
        except (ValueError, ZeroDivisionError, OverflowError):
            if xs:
                segments.append((xs, ys))
            xs = []
            ys = []
    if xs:
        segments.append((xs, ys))
    return segments

def draw(title, series, xl='x', yl='y'):
    import ti_plotlib as p
    xmin = xmax = ymin = ymax = None
    for label, segments in series:
        for xs, ys in segments:
            for i in range(len(xs)):
                x, y = (xs[i], ys[i])
                if xmin is None:
                    xmin = xmax = x
                    ymin = ymax = y
                else:
                    xmin = min(xmin, x)
                    xmax = max(xmax, x)
                    ymin = min(ymin, y)
                    ymax = max(ymax, y)
    if xmin is None:
        raise ValueError('No defined points')
    dx = (xmax - xmin) * 0.06 if xmax != xmin else max(1, abs(xmin) * 0.06)
    dy = (ymax - ymin) * 0.12 if ymax != ymin else max(1, abs(ymin) * 0.12)
    p.cls()
    p.window(xmin - dx, xmax + dx, ymin - dy, ymax + dy)
    p.axes('on')
    p.grid((xmax - xmin + 2 * dx) / 5, (ymax - ymin + 2 * dy) / 5, 'dot')
    p.title(title[:25])
    p.labels(xl[:15], yl[:15], 11, 2)
    p.pen('thin', 'solid')
    for j in range(len(series)):
        p.color(0, 100, 220) if j == 0 else p.color(220, 60, 40)
        for xs, ys in series[j][1]:
            if len(xs) > 1:
                p.plot(xs, ys, '')
            else:
                p.plot(xs[0], ys[0], 'o')
    p.show_plot()

def plot_formula(entry):
    from APFORM import solve_formula
    title, eq, specs, invs, note = entry[:5]
    yi = menu('Vertical variable', [s[0] + ' ' + s[2] for s in specs])
    if yi < 0:
        return
    options = [i for i in range(len(specs)) if i != yi]
    pick = menu('Horizontal variable', [specs[i][0] + ' ' + specs[i][2] for i in options])
    if pick < 0:
        return
    xi = options[pick]
    if not invs[yi]:
        info('Choose another axis', 'Numeric targets cannot be swept. Choose an explicit target or custom f(x).')
        return
    branch = 0
    if len(invs[yi]) > 1:
        branch = menu('Root branch (ascending)', ['Root ' + str(i + 1) for i in range(len(invs[yi]))])
        if branch < 0:
            return
    vals = {}
    for i in range(len(specs)):
        if i not in (xi, yi):
            vals[specs[i][0]] = number(specs[i][0] + ' ' + specs[i][2], specs[i][3])
    lo, hi = (number('LOW x'), number('HIGH x'))

    def f(x):
        domain = specs[xi][3]
        if domain == '+' and x <= 0 or (domain == '0' and x < 0):
            raise ValueError('Domain')
        vals[specs[xi][0]] = x
        if specs[yi][0] in vals:
            del vals[specs[yi][0]]
        roots = solve_formula(entry, yi, vals)
        roots.sort()
        if len(roots) <= branch:
            raise ValueError('Branch undefined')
        return roots[branch]
    info('Plot note', note + '\n40 samples can miss poles or peaks. Use a narrow window.')
    draw(title, [(specs[yi][0], samples(f, lo, hi))], specs[xi][0] + ' ' + specs[xi][2], specs[yi][0] + ' ' + specs[yi][2])

def main():
    s=input('f(x): ').strip()
    if s.lower()=='q':return
    lo,hi=number('LOW x'),number('HIGH x')
    draw('Custom f(x)', [('f',samples(lambda x:calc(s,{'x':x}),lo,hi,40))])
