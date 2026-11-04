from APCORE import menu, info, head, number, result, CONST, LAST, Cancel, error, fmt
from APMEM import release
UNITS = ['1 Kinematics', '2 Forces / dynamics', '3 Work / energy / power', '4 Linear momentum', '5 Torque / rotation', '6 Rotation energy / L', '7 Oscillations', '8 Charge / fields / Gauss', '9 Electric potential', '10 Conductors / capacitors', '11 Electric circuits', '12 Magnetic fields', '13 Induction / RL / LC']

def unit_ui(unit):
    name = 'APU' + ('0' if unit < 10 else '') + str(unit)
    mod = __import__(name)
    from APDATA import titles, entry
    from APFORM import formula_ui
    while True:
        i = menu(UNITS[unit - 1], titles(mod.DATA))
        if i < 0:
            break
        f = entry(mod.DATA, i)
        while True:
            j = menu(f[0], ['Solve an unknown', 'Graph this relation', 'Equation / variables'])
            if j < 0:
                break
            try:
                if j == 0:
                    formula_ui(f)
                elif j == 1:
                    graph = None
                    try:
                        graph = __import__('APGRAPH')
                        graph.plot_formula(f)
                    finally:
                        graph = None
                        release(['APGRAPH'])
                else:
                    info(f[0], f[1] + '\n' + '\n'.join((s[0] + ' = ' + s[1] + ' [' + s[2] + ']' for s in f[2])) + '\n' + f[4])
            except Cancel:
                pass
            except (ValueError, ZeroDivisionError, OverflowError) as e:
                error(e)
        f = None
    mod = None

def main():
    while True:
        i = menu('PHYSICS C', ['Mechanics: units 1-7', 'E&M: units 8-13', 'Multi-step solvers', 'Math / lab tools', 'Graphs', 'Constants / g', 'Last answer', 'Help / input syntax'])
        if i < 0:
            return
        if i < 2:
            offset = 0 if i == 0 else 7
            while True:
                j = menu('Mechanics' if i == 0 else 'E&M', UNITS[:7] if i == 0 else UNITS[7:])
                if j < 0:
                    break
                try:
                    unit_ui(offset + j + 1)
                except MemoryError:
                    info('Memory', 'Restart the Python shell, then run APC. Record the failing unit if this repeats.')
                release(['APU' + ('0' if offset + j + 1 < 10 else '') + str(offset + j + 1), 'APDATA', 'APFORM', 'APNUM', 'APGRAPH'])
        elif i in (2, 3, 4):
            name = ['APTOOLS', 'APMATH', 'APGRAPH'][i - 2]
            mod = None
            try:
                mod = __import__(name)
                mod.main()
            except ImportError:
                info('Optional tools', 'Transfer the optional tool files from the release to use this menu.')
            except MemoryError:
                info('Memory', 'Restart the Python shell and run APC again.')
            finally:
                mod = None
                release([name, 'APMECH', 'APEM', 'APLAB', 'APFORM', 'APNUM'])
        elif i == 5:
            info('Constants', '\n'.join((n + '=' + fmt(CONST[n]) for n in CONST)))
            try:
                CONST['g'] = number('g m/s^2', '+', CONST['g'])
            except Cancel:
                pass
        elif i == 6:
            info('Last answer', 'ans=' + fmt(LAST[0]))
        else:
            info('Help', '0 Back; 8 previous; 9 next. Select 1..5 then ENTER. Use SI units and radians. q cancels inputs. ENTER reuses a displayed value. ans reuses the last result. Inputs: 2.5e-6, pi/4, sqrt(2), ke*qe. Use * explicitly and ^ for powers. All 160 equations remain. Equation assumptions are shown. Full concept notes and variable definitions are in the computer reference files. Graphs sample 40 points: use narrow windows. Numerical targets require a continuous sign-changing bracket. Restart the Python shell before APCHECK or after MemoryError.')
main()
