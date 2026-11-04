from math import sqrt, sin, pi

def check(a, b):
    if abs(a - b) > 1e-07 * max(abs(b), 1e-290):
        raise ValueError('Wrong result')

def main():
    print('APCHECK START v3')
    stage = 'math'
    try:
        check(sqrt(4), 2)
        check(sin(pi / 2), 1)
        stage = 'expressions'
        from APCORE import calc
        check(calc('-2^2'), -4)
        check(calc('2^3^2'), 512)
        check(calc('sin(pi/2)+2.5e-6'), 1.0000025)
        stage = 'quadratic / root'
        from APNUM import quadratic, bisect
        roots = quadratic(1, -3, 2)
        check(roots[0], 1)
        check(roots[1], 2)
        check(bisect(lambda x: x * x - 2, 0, 2), sqrt(2))
        print('SELF CHECK PASS')
        print('8 numeric checks passed.')
        print('Restart shell, then run APC.')
    except MemoryError:
        print('SELF CHECK MEMORY ERROR')
        print('Restart Python shell and retry.')
    except Exception as e:
        print('SELF CHECK FAILED')
        print('Stage: ' + stage)
        print(str(e))
    input('ENTER to finish ')
main()
