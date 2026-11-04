from APCORE import menu,info,Cancel,error
from APMEM import release
def action(group):
 labels=['Uniform solid sphere','Shell / conductor sphere','Uniform infinite cylinder','Infinite line','Sheets / conductor face','Nonuniform sphere rho=ar^n','Closed flux from charge','Flat uniform flux'] if group==0 else ['Work and final speed','Uniform field voltage/work','Charge assembly energy','Zero-field point on line','Identical spheres contact']
 while True:
  i=menu('GAUSS / FLUX' if group==0 else 'ENERGY / CHARGE',labels)
  if i<0:return
  mod=None
  try:
   mod=__import__('E2CALC')
   if group==0:mod.gauss(i)
   else:mod.work(i)
  except ImportError:info('Change CE topic','This feature is included in another topic. Open CE_GUIDE.md on your computer: FIELD_STUDIO for field solvers, FIELD_GUIDES for derivations, FINAL_FORMULAS for all final equations. Quit Python before changing the installed topic.')
  except Cancel:pass
  except(ValueError,ZeroDivisionError,OverflowError)as e:error(e)
  finally:
   mod=None;release(['E2CALC','E2PHYS'])
def main():
 while True:
  i=menu('EXAM 2 / ELECTROSTATICS',['Study / formulas / concepts','Gauss law / flux solvers','Work / energy / charge','Point charges E V and force','Rod / arc / ring studio','Exam 2 self-check'])
  if i<0:return
  mod=None
  try:
   if i==0:
    mod=__import__('E2NOTES');mod.show()
   elif i in(1,2):action(i-1)
   elif i==3:
    mod=__import__('E2CALC');mod.points()
   elif i==4:
    mod=__import__('EFAPP');mod.main()
   else:
    mod=__import__('E2CHECK');mod.run()
  except ImportError:info('Change CE topic','This feature is included in another topic. Open CE_GUIDE.md on your computer: FIELD_STUDIO for field solvers, FIELD_GUIDES for derivations, FINAL_FORMULAS for all final equations. Quit Python before changing the installed topic.')
  except Cancel:pass
  except(ValueError,ZeroDivisionError,OverflowError)as e:error(e)
  except MemoryError:info('Memory','Restart Python and run EXAM2 directly.')
  finally:
   mod=None;release(['E2NOTES','E2CALC','E2PHYS','E2CHECK','EFAPP'])
