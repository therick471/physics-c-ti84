# AP Physics C toolkit. TI-Python + desktop Python; no third-party libraries.
from math import sqrt, sin, cos, tan, asin, acos, atan, atan2, exp, log, pi
try:
    from ti_system import disp_clr
except ImportError:
    def disp_clr():
        print('\n' * 2)

CONST = {'pi': pi, 'e': exp(1), 'g': 9.8, 'G': 6.67430e-11,
         'ke': 8.9875517923e9, 'eps0': 8.8541878128e-12,
         'mu0': 1.25663706212e-6, 'qe': 1.602176634e-19,
         'me': 9.1093837139e-31, 'mp': 1.67262192595e-27,
         'c0': 299792458.0}
FUN = {'sqrt': sqrt, 'sin': sin, 'cos': cos, 'tan': tan,
       'asin': asin, 'acos': acos, 'atan': atan, 'exp': exp,
       'ln': log, 'log': log, 'abs': abs}
LAST = [0.0]
HISTORY = []
WIDTH = 30

class Cancel(Exception):
    pass

def finite(x):
    return isinstance(x, (int, float)) and x == x and abs(x) < 1e300

# A small arithmetic parser avoids eval compatibility/security issues.
# Supports scientific notation, functions, constants, ^ and **.
class Parser:
    def __init__(self, text, values):
        self.s = text.replace(' ', '').replace('**', '^')
        self.i = 0
        self.v = values
    def peek(self):
        if self.i < len(self.s):
            return self.s[self.i]
        return ''
    def sum(self):
        v = self.product()
        magnitude = abs(v)
        while self.peek() in ('+', '-'):
            op = self.peek()
            self.i += 1
            r = self.product()
            magnitude += abs(r)
            v = v + r if op == '+' else v - r
        self.magnitude = magnitude
        return v
    def product(self):
        v = self.unary()
        while self.peek() in ('*', '/'):
            op = self.peek()
            self.i += 1
            r = self.unary()
            v = v * r if op == '*' else v / r
        return v
    def unary(self):
        if self.peek() in ('+', '-'):
            op = self.peek()
            self.i += 1
            v = self.unary()
            return v if op == '+' else -v
        v = self.atom()
        if self.peek() == '^':
            self.i += 1
            v = v ** self.unary()
        return v
    def atom(self):
        ch = self.peek()
        if ch == '(':
            self.i += 1
            v = self.sum()
            if self.peek() != ')':
                raise ValueError('Missing )')
            self.i += 1
            return v
        if ch and (ch.isdigit() or ch == '.'):
            start = self.i
            while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
                self.i += 1
            if self.peek() in ('e', 'E'):
                self.i += 1
                if self.peek() in ('+', '-'):
                    self.i += 1
                while self.peek() and self.peek().isdigit():
                    self.i += 1
            return float(self.s[start:self.i])
        if ch and (ch.isalpha() or ch == '_'):
            start = self.i
            while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
                self.i += 1
            name = self.s[start:self.i]
            if self.peek() == '(':
                if name not in FUN:
                    raise ValueError('Unknown function: ' + name)
                self.i += 1
                v = self.sum()
                if self.peek() != ')':
                    raise ValueError('Missing )')
                self.i += 1
                return FUN[name](v)
            if name in self.v:
                return self.v[name]
            if name == 'ans':
                return LAST[0]
            if name in CONST:
                return CONST[name]
            raise ValueError('Unknown name: ' + name)
        raise ValueError('Use Python math syntax')

def calc(text, values=None):
    p = Parser(text, {} if values is None else values)
    v = p.sum()
    if p.i != len(p.s) or not finite(v):
        raise ValueError('Invalid or non-real result')
    return v

def checked_sides(lhs, rhs, vals, tolerance=1e-7):
    # Sum magnitudes make cancellation to zero a valid residual check.
    p = Parser(lhs, vals)
    l = p.sum()
    lm = p.magnitude
    p = Parser(rhs, vals)
    r = p.sum()
    scale = max(abs(l),abs(r),lm,p.magnitude,1e-300)
    return finite(l) and finite(r) and abs(l-r) <= tolerance*scale

def wrap(text):
    out = []
    for para in str(text).split('\n'):
        line = ''
        for word in para.split(' '):
            while len(word) > WIDTH:
                if line:
                    out.append(line)
                    line = ''
                out.append(word[:WIDTH])
                word = word[WIDTH:]
            if len(line) + len(word) + 1 > WIDTH:
                out.append(line)
                line = ''
            line = (line + ' ' + word).strip()
        out.append(line)
    return out

def head(title):
    disp_clr()
    print(('APC | ' + title)[:WIDTH])
    print('=' * WIDTH)

def info(title, text):
    lines = wrap(text)
    for start in range(0, len(lines), 7):
        head(title)
        for line in lines[start:start + 7]:
            print(line)
        input('ENTER continue ')

def menu(title, items):
    page = 0
    while True:
        head(title + ' ' + str(page + 1))
        start = page * 5
        for j in range(start, min(start + 5, len(items))):
            print(str(j - start + 1) + ' ' + items[j][:27])
        print('0 Back | 8 Prev | 9 Next')
        s = input('Select: ').strip().lower()
        if s in ('0', 'q', 'b'):
            return -1
        if s == '9':
            page = (page + 1) % ((len(items) + 4) // 5)
        elif s == '8':
            page = (page - 1) % ((len(items) + 4) // 5)
        elif s in ('1', '2', '3', '4', '5'):
            j = start + int(s) - 1
            if j < len(items):
                return j

def number(label, domain='s', default=None):
    while True:
        prompt = label[:23]
        if default is not None:
            prompt += ' [' + fmt(default) + ']'
        s = input(prompt + ': ').strip()
        if s.lower() in ('q', 'b'):
            raise Cancel()
        try:
            x = default if s == '' and default is not None else calc(s)
            if domain == '+' and x <= 0:
                raise ValueError('Must be > 0')
            if domain == '0' and x < 0:
                raise ValueError('Must be >= 0')
            return x
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            print(str(e)[:WIDTH])

def integer(label, lo, hi):
    while True:
        x = number(label)
        if x == int(x) and lo <= x <= hi:
            return int(x)
        print('Integer ' + str(lo) + '..' + str(hi))

def fmt(x):
    return '{:.7g}'.format(x)

def result(title, pairs, note=''):
    lines = []
    for name, v in pairs:
        if not finite(v):
            raise ValueError('Non-real or overflow result')
        LAST[0] = v
        lines.append(name + ' = ' + fmt(v))
    HISTORY.append((title, '\n'.join(lines)))
    if len(HISTORY) > 8:
        HISTORY.pop(0)
    info(title, '\n'.join(lines) + ('\n' + note if note else ''))

def error(e):
    info('Check inputs', str(e) + '\nUse SI units. q cancels.')

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
    # Stable evaluation avoids loss of the small root.
    q = -0.5 * (b + (sqrt(d) if b >= 0 else -sqrt(d)))
    roots = [q / a, c / q]
    roots.sort()
    return roots

def bisect(f, a, b, rtol=1e-9, atol=0.0):
    if a >= b:
        raise ValueError('Need low < high')
    fa, fb = f(a), f(b)
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
            a, fa = m, fm
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
    return (f(x - 2*h) - 8*f(x-h) + 8*f(x+h) - f(x+2*h)) / (12*h)

def linear(a, b):
    n = len(b)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    scales = [max([abs(v) for v in row]) for row in a]
    if min(scales) == 0:
        raise ValueError('Singular system')
    for k in range(n):
        pivot = k
        for i in range(k + 1, n):
            if abs(m[i][k])/scales[i] > abs(m[pivot][k])/scales[pivot]:
                pivot = i
        if abs(m[pivot][k])/scales[pivot] < 1e-12:
            raise ValueError('Singular/ill-conditioned')
        m[k], m[pivot] = m[pivot], m[k]
        scales[k], scales[pivot] = scales[pivot], scales[k]
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

def valid_geometry(entry, vals):
    title = entry[0]
    if title in ('Uniform sphere inside','Sphere inside potential','Solid wire inside B'):
        if vals['r'] > vals['R']:
            return False
    if title in ('Spherical capacitor','Coaxial capacitor') and vals['r'] >= vals['R']:
        return False
    if title in ('Rod axis field','Rod axis potential') and vals['x'] <= 0:
        return False
    if title == 'Disk axis field' and vals['x'] < 0:
        return False
    if title in ('Parallel plate C','Physical pendulum') and vals['d'] <= 0:
        return False
    if title == 'SHM speed-position' and abs(vals['x']) > vals['amp']:
        return False
    if title == 'Charge quantization' and abs(vals['nc']-round(vals['nc'])) > 1e-7:
        return False
    if title in ('Charged orbit radius','Velocity selector') and vals['v'] < 0:
        return False
    return True

def solve_formula(entry, target, vals):
    # Entry: title, equation, variables, inverses, assumptions.
    eq, specs, inverses = entry[1:4]
    lhs, rhs = eq.split('=')
    roots = []
    candidates = []
    if len(entry) > 5 and entry[5][target]:
        coefficients = [calc(c, vals) for c in entry[5][target]]
        if len(coefficients) == 2:
            coefficients = [0.0] + coefficients
        try:
            candidates = quadratic(coefficients[0],coefficients[1],coefficients[2])
        except ValueError:
            candidates = []
    else:
        for expression in inverses[target]:
            try:
                candidates.append(calc(expression, vals))
            except (ValueError, ZeroDivisionError, OverflowError):
                pass
    for x in candidates:
        try:
            domain = specs[target][3]
            if (domain == '+' and x <= 0) or (domain == '0' and x < 0):
                continue
            test = dict(vals)
            test[specs[target][0]] = x
            if not valid_geometry(entry,test):
                continue
            if not checked_sides(lhs,rhs,test):
                continue
            if not any(abs(x-v) <= 1e-8 * max(abs(x), abs(v), 1e-300) for v in roots):
                roots.append(x)
        except (ValueError, ZeroDivisionError, OverflowError):
            pass
    return roots

def formula_ui(entry):
    title, equation, specs, inverses, note = entry[:5]
    saved = {}
    while True:
        target = menu(title, [s[0] + ' ' + s[1] for s in specs] + ['Equation / assumptions'])
        if target < 0:
            return
        if target == len(specs):
            info(title, equation.replace('**', '^') + '\n' + note)
            continue
        try:
            head(title)
            print(equation.replace('**', '^'))
            print('SI units | angles rad | q Back')
            vals = {}
            for i in range(len(specs)):
                if i != target:
                    name, label, unit, domain = specs[i]
                    vals[name] = number(name + ' ' + unit, domain, saved.get(name))
            saved.update(vals)
            if inverses[target]:
                roots = solve_formula(entry, target, vals)
            else:
                info('Numeric branch', 'Enter a continuous sign-changing bracket for the unknown. One root per bracket. Avoid poles. Tangent roots may require a different equation.')
                lo = number('LOW ' + specs[target][2])
                hi = number('HIGH ' + specs[target][2])
                lhs, rhs = equation.split('=')
                name = specs[target][0]
                def f(x):
                    vals[name] = x
                    return calc(lhs, vals) - calc(rhs, vals)
                x = bisect(f, lo, hi)
                vals[name] = x
                domain = specs[target][3]
                if (domain == '+' and x <= 0) or (domain == '0' and x < 0):
                    raise ValueError('Root outside physical domain')
                if not valid_geometry(entry,vals):
                    raise ValueError('Root outside stated geometry')
                if not checked_sides(lhs,rhs,vals,1e-6):
                    raise ValueError('Residual failed; possible pole')
                roots = [x]
            if not roots:
                raise ValueError('No valid real solution. Check degeneracy, signs and domain.')
            result(title, [(specs[target][0] + ' ' + specs[target][2], x) for x in roots], 'Choose the branch that fits the situation. ' + note)
        except Cancel:
            pass
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            error(e)
