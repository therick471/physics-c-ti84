from APCORE import calc, checked_sides, menu, head, info, number, result, Cancel, error
from APNUM import quadratic, bisect

def valid_geometry(entry, vals):
    title = entry[0]
    if title in ('Uniform sphere inside', 'Sphere inside potential', 'Solid wire inside B'):
        if vals['r'] > vals['R']:
            return False
    if title in ('Spherical capacitor', 'Coaxial capacitor') and vals['r'] >= vals['R']:
        return False
    if title in ('Rod axis field', 'Rod axis potential') and vals['x'] <= 0:
        return False
    if title == 'Disk axis field' and vals['x'] < 0:
        return False
    if title in ('Parallel plate C', 'Physical pendulum') and vals['d'] <= 0:
        return False
    if title == 'SHM speed-position' and abs(vals['x']) > vals['amp']:
        return False
    if title == 'Charge quantization' and abs(vals['nc'] - round(vals['nc'])) > 1e-07:
        return False
    if title in ('Charged orbit radius', 'Velocity selector') and vals['v'] < 0:
        return False
    return True

def solve_formula(entry, target, vals):
    eq, specs, inverses = entry[1:4]
    lhs, rhs = eq.split('=')
    roots = []
    candidates = []
    if len(entry) > 5 and entry[5][target]:
        coefficients = [calc(c, vals) for c in entry[5][target]]
        if len(coefficients) == 2:
            coefficients = [0.0] + coefficients
        try:
            candidates = quadratic(coefficients[0], coefficients[1], coefficients[2])
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
            if domain == '+' and x <= 0 or (domain == '0' and x < 0):
                continue
            test = dict(vals)
            test[specs[target][0]] = x
            if not valid_geometry(entry, test):
                continue
            if not checked_sides(lhs, rhs, test):
                continue
            if not any((abs(x - v) <= 1e-08 * max(abs(x), abs(v), 1e-300) for v in roots)):
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
                if domain == '+' and x <= 0 or (domain == '0' and x < 0):
                    raise ValueError('Root outside physical domain')
                if not valid_geometry(entry, vals):
                    raise ValueError('Root outside stated geometry')
                if not checked_sides(lhs, rhs, vals, 1e-06):
                    raise ValueError('Residual failed; possible pole')
                roots = [x]
            if not roots:
                raise ValueError('No valid real solution. Check degeneracy, signs and domain.')
            result(title, [(specs[target][0] + ' ' + specs[target][2], x) for x in roots], 'Choose the branch that fits the situation. ' + note)
        except Cancel:
            pass
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            error(e)
