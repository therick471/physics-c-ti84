from math import sqrt, sin, cos, log, pi
K=8.9875517923e9
NAMES=['Ring: on its axis','Rod: perpendicular bisector','Rod: beyond an end','Infinite straight line','Arc: field at center']

def field(kind,q,d,x,phi=pi):
    # d=R for ring/arc, full L for rod, reference R for infinite line.
    if d<=0: raise ValueError('Size must be positive')
    if kind==0:
        h=sqrt(d*d+x*x)
        return K*q*x/(h*h*h),K*q/h
    if kind==1:
        if x==0: raise ValueError('Ideal rod singular at x=0')
        a=d/2
        h=sqrt(x*x+a*a)
        return K*q/(x*h),K*q/a*log((h+a)/abs(x))
    if kind==2:
        if x<=0: raise ValueError('x is distance beyond end; x>0')
        return K*q/(x*(x+d)),K*q/d*log(1+d/x)
    if kind==3:
        if x==0: raise ValueError('Ideal line singular at x=0')
        return 2*K*q/x,-2*K*q*log(abs(x)/d)
    if not 0<phi<=2*pi: raise ValueError('Arc angle: 0<phi<=360 deg')
    e=0.0 if abs(phi-2*pi)<1e-12 else 2*K*q*sin(phi/2)/(d*d*phi)
    return e,K*q/d

def ring_distances(q,r,target):
    from APNUM import bisect
    if r<=0: raise ValueError('R>0')
    if q==0: raise ValueError('Zero Q: E=0 at every x')
    if target==0: return [0.0]
    if target*q<0: raise ValueError('No positive-x solution with these signs')
    peak=r/sqrt(2)
    top=abs(field(0,q,r,peak)[0])
    y=abs(target)
    if y>top*(1+1e-12): raise ValueError('Target exceeds maximum |E|')
    if abs(y-top)<=1e-12*top: return [peak]
    f=lambda x:abs(field(0,q,r,x)[0])-y
    hi=max(r,sqrt(K*abs(q)/y))*2
    return [bisect(f,0,peak),bisect(f,peak,hi)]

def inverse_distance(kind,q,d,target):
    if target==0 or q==0: raise ValueError('Use limits for E=0; zero charge is degenerate')
    if q/target<=0: raise ValueError('Positive distance requires E and source same sign')
    z=K*q/target
    if kind==1:
        a=d/2
        return sqrt(2*z*z/(sqrt(a**4+4*z*z)+a*a))
    if kind==2: return 2*z/(sqrt(d*d+4*z)+d)
    if kind==3: return 2*z
    raise ValueError('Use ring two-root solver')

def arc_components(q,r,phi,mid):
    e,v=field(4,q,r,0,phi)
    return -e*cos(mid),-e*sin(mid),v

def two_ring_ratio(r1,r2,a,b):
    if min(r1,r2,a,b)<=0: raise ValueError('Positive radii and distances')
    # P is between rings. Fields oppose only for same-sign charges.
    return (b/a)*((r1*r1+a*a)/(r2*r2+b*b))**1.5
