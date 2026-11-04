from APCORE import menu, info, Cancel, error
from APMEM import release
NAMES = ['Vectors: dot / cross', 'Projectile: full flight', 'Collision: elastic / stick', 'COM / total momentum', 'Atwood + massive pulley', 'SHM from initial state', 'Charges: E / V / force', 'Sphere: inside / outside', 'Equivalent R or C', 'DC circuit: multiple cells', 'RC charge / discharge', 'RL rise / decay', 'Rolling incline', 'Lab linear regression', 'Motional emf / drag']

def main():
    while True:
        i = menu('Multi-step tools', NAMES)
        if i < 0:
            return
        name = 'APMECH' if i < 6 or i == 12 else 'APLAB' if i == 13 else 'APEM'
        mod = None
        try:
            mod = __import__(name)
            mod.run_tool(i)
        except Cancel:
            pass
        except ImportError:
            info('Optional tools', 'Transfer the missing optional tool group from the release.')
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            error(e)
        finally:
            mod = None
            release([name, 'APNUM'])
