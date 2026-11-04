from APCORE import calc, menu, head, info, number, integer, result, error, Cancel, bisect, integrate, derivative, quadratic, linear

def expression(prompt):
    info('Expression syntax', 'Use x, pi, g, ke, eps0, mu0; + - * / ^; sqrt, sin, cos, tan, exp, ln, abs. Angles radians. Example: 3*x^2-2*x. Explicit multiplication: 2*x, not 2x. q cancels.')
    s = input(prompt + ': ').strip()
    if s.lower() == 'q':
        raise Cancel()
    return s

def calculus(which):
    s = expression('f(x)')
    def f(x):
        return calc(s, {'x': x})
    head('Numerical calculus')
    if which == 0:
        x = number('x of derivative')
        h = number('step h','+',1e-3*max(1,abs(x)))
        d1,d2 = derivative(f,x,h),derivative(f,x,h/2)
        result('Derivative',[('df/dx',d2),('step change',abs(d2-d1))], 'Finite-difference estimate. Reduce h carefully; roundoff and cusps can invalidate it.')
    elif which == 1:
        a,b = number('lower x'),number('upper x')
        n = integer('Even intervals (2..160)',2,160)
        if n % 2:
            raise ValueError('Interval count must be even')
        i1,i2 = integrate(f,a,b,n),integrate(f,a,b,n*2)
        result('Integral',[('integral',i2),('refinement change',abs(i2-i1))], 'Composite Simpson estimate, not certified error. Split discontinuities. Integral of v gives displacement; F gives work; I gives charge.')
    elif which == 2:
        a,b = number('LOW x'),number('HIGH x')
        x = bisect(f,a,b)
        residual = f(x)
        scale = max(abs(f(a)),abs(f(b)),1e-300)
        if abs(residual) > 1e-6*scale:
            raise ValueError('Residual failed; avoid poles')
        result('Root',[('x',x),('f(x)',residual)], 'Continuous sign-changing bracket required; finds one root. Even-multiplicity roots need another method.')
    elif which == 3:
        x = number('x')
        result('Evaluate',[('f(x)',f(x))])

def ode_ui():
    info('ODE: y prime=f(x,y)', 'Fourth-order Runge-Kutta with fixed steps. For decay: -y/(R*C), enter numeric R and C values. For dv/dt: g-b*y/m. Use x for time, y for state. Compare different step counts. No automatic error guarantee.')
    s = input('f(x,y): ').strip()
    if s.lower() == 'q':
        raise Cancel()
    x0,y0,x1 = number('initial x'),number('initial y'),number('final x')
    n = integer('Steps 1..200',1,200)
    def f(x,y):
        return calc(s,{'x':x,'y':y})
    def rk(steps):
        h = (x1-x0)/steps
        x,y = x0,y0
        for i in range(steps):
            k1 = f(x,y)
            k2 = f(x+h/2,y+h*k1/2)
            k3 = f(x+h/2,y+h*k2/2)
            k4 = f(x+h,y+h*k3)
            y += h*(k1+2*k2+2*k3+k4)/6
            x = x0+(i+1)*h
        return y
    a,b = rk(n),rk(2*n)
    result('ODE estimate',[('final y',b),('step change',abs(b-a))])

def systems_ui():
    info('Linear equations', 'Enter A coefficients and b for A*x=b. Use for KCL/KVL, equilibrium forces/torques, or other simultaneous equations. Max 6 unknowns. Each equation must be linear.')
    n = integer('Unknowns 1..6',1,6)
    a,b = [],[]
    for i in range(n):
        head('Equation '+str(i+1))
        a.append([number('Coeff x'+str(j+1)) for j in range(n)])
        b.append(number('Right side'))
    result('Linear system',[('x'+str(i+1),v) for i,v in enumerate(linear(a,b))])

def percent_ui():
    head('Percent error / difference')
    choice = menu('Compare',['Error: measured vs true','Difference: two measurements'])
    if choice < 0:
        return
    a,b = number('value 1'),number('value 2')
    denominator = abs(b) if choice == 0 else (abs(a)+abs(b))/2
    if denominator == 0:
        raise ValueError('Reference denominator is zero')
    result('Comparison',[('percent',100*abs(a-b)/denominator)], 'Error uses value 2 as accepted reference. Difference uses average absolute magnitudes.')

def main():
    items = ['Derivative / slope','Integral / area','Root in bracket','Evaluate f(x)',
             'Quadratic: both roots','Linear system Ax=b','ODE: y prime=f(x,y)','Percent error / difference']
    while True:
        i = menu('Math / lab tools',items)
        if i < 0:
            return
        try:
            if i < 4:
                calculus(i)
            elif i == 4:
                head('a*x^2 + b*x + c = 0')
                roots = quadratic(number('a'),number('b'),number('c'))
                result('Quadratic',[('root '+str(j+1),x) for j,x in enumerate(roots)])
            elif i == 5:
                systems_ui()
            elif i == 6:
                ode_ui()
            else:
                percent_ui()
        except Cancel:
            pass
        except (ValueError,ZeroDivisionError,OverflowError) as e:
            error(e)
