from APCORE import menu, info, head, number, result, CONST, LAST, Cancel, error, fmt
from APMEM import release
UNITS=['Charge / fields / Gauss','Electric potential','Conductors / capacitors','Electric circuits','Magnetic fields','Induction / RL / LC']
def unit_ui(unit):
    name = 'APU' + ('0' if unit < 10 else '') + str(unit)
    mod = __import__(name)
    from APDATA import titles, entry
    from APFORM import formula_ui
    while True:
        i = menu(UNITS[unit - 8], titles(mod.DATA))
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
        i=menu('PHYSICS C / E&M',['E-FIELD STUDIO','Final formulas','E&M equation reference','Math / calculus tools','Custom graph','Help'])
        if i<0:return
        try:
            if i==0:
                mod=__import__('EFAPP')
                mod.main()
                mod=None
            elif i==1:
                mod=__import__('EFFINAL')
                mod.show()
                mod=None
            elif i==2:
                j=menu('E&M units',UNITS)
                if j>=0: unit_ui(j+8)
            elif i==3:
                mod=__import__('APMATH')
                mod.main()
                mod=None
            elif i==4:
                mod=__import__('APGRAPH')
                mod.main()
                mod=None
            else: info('Quick start','Run EFIELD for the new guided solver, APC for all E&M tools. SI units; angles in radians except arc degree prompts. R is ring radius; L is FULL rod length. 0 Back; 8/9 pages. The printed notes are the source for the five derivation guides.')
        except Cancel:pass
        except (ValueError,ZeroDivisionError,OverflowError) as e:error(e)
        release(['APU08','APU09','APU10','APU11','APU12','APU13','APDATA','APFORM','APGRAPH','APMATH','APNUM','EFAPP','EFMODEL','EFTOOLS','EFINPUT','EFNOTE','EFCALC','EFEXT','EFINV','EFPLOT','EFFINAL']+['EFN'+str(n) for n in range(5)])
main()
