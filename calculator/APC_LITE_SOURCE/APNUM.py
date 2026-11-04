from math import sqrt

def finite(x):
    return isinstance(x, (int, float)) and x == x and (abs(x) < 1e+300)

def quadratic(a, b, c):
    if a == 0:
        if b == 0:
            raise ValueError('Underdetermined' if c == 0 else 'No solution')
        return [-c / b]
    d = b * b - 4 * a * c
    if d < 0:
        raise ValueError('No real roots')
    if d == 0:
        return [-b / (2 * a)]
    q = -0.5 * (b + (sqrt(d) if b >= 0 else -sqrt(d)))
    roots = [q / a, c / q]
    roots.sort()
    return roots

def bisect(f, a, b, rtol=1e-09, atol=0.0):
    if a >= b:
        raise ValueError('Need low < high')
    fa, fb = (f(a), f(b))
    if not finite(fa) or not finite(fb):
        raise ValueError('Bad endpoints')
    if fa == 0:
        return a
    if fb == 0:
        return b
    if (fa > 0) == (fb > 0):
        raise ValueError('Bracket must change sign')
    for n in range(100):
        m = a + (b - a) / 2
        fm = f(m)
        if not finite(fm):
            raise ValueError('Function undefined')
        if fm == 0:
            return m
        if b - a <= max(atol, rtol * max(abs(a), abs(b), 1e-300)):
            return m
        if (fa > 0) != (fm > 0):
            b = m
        else:
            a, fa = (m, fm)
    raise ValueError('No convergence; narrower bracket')

def integrate(f, a, b, n=80):
    if n < 2 or n % 2:
        raise ValueError('Even interval count required')
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * f(a + i * h)
    return total * h / 3

def derivative(f, x, h):
    if h <= 0:
        raise ValueError('h must be positive')
    return (f(x - 2 * h) - 8 * f(x - h) + 8 * f(x + h) - f(x + 2 * h)) / (12 * h)

def linear(a, b):
    n = len(b)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    scales = [max([abs(v) for v in row]) for row in a]
    if min(scales) == 0:
        raise ValueError('Singular system')
    for k in range(n):
        pivot = k
        for i in range(k + 1, n):
            if abs(m[i][k]) / scales[i] > abs(m[pivot][k]) / scales[pivot]:
                pivot = i
        if abs(m[pivot][k]) / scales[pivot] < 1e-12:
            raise ValueError('Singular/ill-conditioned')
        m[k], m[pivot] = (m[pivot], m[k])
        scales[k], scales[pivot] = (scales[pivot], scales[k])
        for i in range(k + 1, n):
            factor = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= factor * m[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        v = m[i][n]
        for j in range(i + 1, n):
            v -= m[i][j] * x[j]
        x[i] = v / m[i][i]
    return x
