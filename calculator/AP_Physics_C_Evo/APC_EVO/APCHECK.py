# Run this on the calculator after transfer. No testing library required.
from math import pi
from APCORE import calc, quadratic, bisect, integrate, derivative, linear, solve_formula, info
from APTOOLS import projectile, collision, atwood, shm, rc, rl, charges, sphere, equivalent, network, regress

def close(a,b):
    if abs(a-b)>1e-7*max(1,abs(b)):
        raise ValueError('Expected '+str(b)+' got '+str(a))

def checks():
    close(calc('-2^2'),-4)
    close(calc('2^3^2'),512)
    close(calc('sin(pi/2)+2.5e-6'),1.0000025)
    close(quadratic(1,-3,2)[0],1)
    close(quadratic(1,-3,2)[1],2)
    close(bisect(lambda x:x*x-2,0,2),2**.5)
    close(integrate(lambda x:x*x,0,3),9)
    close(derivative(lambda x:x**3,2,.001),12)
    close(linear([[2,1],[1,-1]],[5,1])[0],2)
    close(projectile(14,pi/4,0,0,9.8)[1][1],20)
    close(collision(1,1,3,0,1)[0][1],0)
    close(collision(1,1,3,0,1)[1][1],3)
    close(atwood(1,3,0,.1,9.8)[0][1],4.9)
    close(shm(1,4,1,0,pi/4)[4][1],0)
    close(rc(1000,1e-6,0,10,.001)[1][1],6.3212055883)
    close(rl(10,1,0,10,.1)[1][1],.6321205588)
    close(charges([(1e-9,-1,0),(1e-9,1,0)],0,0)[0],0)
    close(sphere(1e-9,1,0,True)[0],0)
    close(equivalent([100,100],'R','parallel'),50)
    close(equivalent([1e-6,1e-6],'C','series'),.5e-6)
    v,ir,iv=network(2,[(1,2,1000),(2,0,1000)],[(1,0,10)])
    close(v[2],5)
    close(ir[0],.005)
    close(regress([1,2,3],[3,5,7])[0],2)
    import APU01
    f=APU01.F[1]
    roots=solve_formula(f,3,{'dx':10,'u':0,'a':5})
    close(roots[0],2)
    return 24

def main():
    try:
        count=checks()
        info('SELF CHECK PASS',str(count)+' numeric checks passed.\nNext run APC, solve Newton F=ma, navigate pages, and try a graph. Graphs and key handling need a real-device check.')
    except Exception as e:
        info('SELF CHECK FAILED',str(e))

if __name__=='__main__':
    main()
