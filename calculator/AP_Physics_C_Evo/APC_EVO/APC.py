# Transfer every .py file in this folder; run APC in the Python app.
from APCORE import menu, info, head, number, result, CONST, HISTORY, Cancel, error, formula_ui, fmt

UNITS = ['1 Kinematics','2 Forces / dynamics','3 Work / energy / power','4 Linear momentum',
         '5 Torque / rotation','6 Rotation energy / L','7 Oscillations','8 Charge / fields / Gauss',
         '9 Electric potential','10 Conductors / capacitors','11 Electric circuits',
         '12 Magnetic fields','13 Induction / RL / LC']

def unit_ui(unit):
    mod = __import__('APU'+('0' if unit<10 else '')+str(unit))
    while True:
        i=menu(UNITS[unit-1],['Concepts / strategy']+[f[0] for f in mod.F])
        if i<0:
            return
        if i==0:
            import APNOTES
            APNOTES.unit(unit)
        else:
            f=mod.F[i-1]
            while True:
                choice=menu(f[0],['Solve an unknown','Graph this relation','Equation / variables'])
                if choice<0:
                    break
                if choice==0:
                    formula_ui(f)
                elif choice==1:
                    import APGRAPH
                    try:
                        APGRAPH.plot_formula(f)
                    except Cancel:
                        pass
                    except (ValueError,ZeroDivisionError,OverflowError) as e:
                        error(e)
                else:
                    labels=[s[0]+' = '+s[1]+' ['+s[2]+']' for s in f[2]]
                    info(f[0],f[1]+'\n'+'\n'.join(labels)+'\n'+f[4])

def constants():
    names=['g','G','ke','eps0','mu0','qe','me','mp','c0','pi']
    units=['m/s^2','N*m^2/kg^2','N*m^2/C^2','F/m','N/A^2','C','kg','kg','m/s','1']
    info('Constants', '\n'.join([names[i]+'='+fmt(CONST[names[i]])+' '+units[i] for i in range(len(names))]))
    if menu('Local gravity',['Change default g'])==0:
        try:
            CONST['g']=number('g m/s^2','+',CONST['g'])
        except Cancel:
            pass

def help_ui():
    info('Start here','1 Choose Mechanics or E&M.\n2 Choose unit and equation.\n3 Select Solve, then the unknown.\n4 Enter the other values in SI.\n0=Back; 8/9=pages. q cancels a numeric prompt. ENTER accepts a displayed previous value. ans reuses last result. Angles are always radians, independent of calculator mode.')
    info('Input syntax','Scientific notation: 2.5e-6. Expressions: pi/3, sqrt(2), 3*10^8, ke*qe. Use * explicitly. sin/cos/tan use radians. Convert degrees with deg*pi/180. Length m; mass kg; time s; C capacitance farads; charge coulombs. Metric: cm*.01, mm*.001, micro*1e-6, nano*1e-9.')
    info('Scope / validation','160 equation solvers, all 13 course units, multi-step tools, numerical calculus and sampled plots. A formula models stated conditions. Numeric branches need continuous sign-changing brackets. Numerical approximations are not symbolic proofs. On-device self-check: run APCHECK. This program does not replace your diagrams or explanations.')

def main():
    while True:
        i=menu('PHYSICS C',['Mechanics: units 1-7','E&M: units 8-13','Multi-step solvers','Math / lab calculations',
                               'Graphs','Lab / reasoning guide','Constants / default g','Recent answers','Help / input syntax'])
        if i<0:
            return
        if i in (0,1):
            offset=0 if i==0 else 7
            items=UNITS[:7] if i==0 else UNITS[7:]
            while True:
                j=menu('Mechanics' if i==0 else 'E&M',items)
                if j<0:
                    break
                unit_ui(offset+j+1)
        elif i==2:
            import APTOOLS
            APTOOLS.main()
        elif i==3:
            import APMATH
            APMATH.main()
        elif i==4:
            import APGRAPH
            APGRAPH.main()
        elif i==5:
            import APNOTES
            APNOTES.lab()
        elif i==6:
            constants()
        elif i==7:
            if HISTORY:
                j=menu('Recent answers',[h[0] for h in HISTORY])
                if j>=0:
                    info(HISTORY[j][0],HISTORY[j][1])
            else:
                info('Recent answers','No answers yet this session.')
        else:
            help_ui()

if __name__=='__main__':
    main()
