from APCORE import menu,info,Cancel,error
from APMEM import release
from EFMODEL import NAMES
from EFGUI import GRAPHICS
def main():
 graphics=GRAPHICS[0]
 modules=['EFCALC','EFNOTE','EFEXT','EFPLOT','EFINV','EFGUI','EFFINAL']
 actions=['calculate','guide','extrema','plot','inverse','sketch','show']
 while True:
  i=menu('E-FIELD STUDIO v2',NAMES+['Final formulas','Two rings / point charges','Custom calculus / limits','Display: graphic/text'])
  if i<0:return
  try:
   if i<5:
    while True:
     j=menu(NAMES[i],['Calculate E, V and force','Full derivation + limits','Maxima / minima','Graph E(x) or V(x)','Solve for source or x','Geometry sketch','Final formulas'])
     if j<0:break
     if j==5 and i not in(0,1):j=1
     mod=None
     gui=None
     try:
      gui=__import__('EFGUI')
      gui.GRAPHICS[0]=graphics
      mod=__import__(modules[j])
      getattr(mod,actions[j])(i)
      graphics=gui.GRAPHICS[0]
     finally:
      mod=None
      gui=None
      release([n for n in modules if n!='EFGUI']+['EFINPUT','EFMODEL','APGRAPH','APNUM'])
   elif i==5:
    mod=__import__('EFFINAL')
    try:mod.show()
    finally:
     mod=None
     release(['EFFINAL','APDATA'])
   elif i in(6,7):
    mod=__import__('EFTOOLS')
    try:mod.main(i==7)
    finally:
     mod=None
     release(['EFTOOLS','EFMODEL','APGRAPH','APNUM'])
   else:
    graphics=not graphics
    GRAPHICS[0]=graphics
    info('Display','Arrow keys move. ENTER selects or advances. CLEAR returns. 8/9 change pages. Full labels wrap across rows.')
  except Cancel:pass
  except(ValueError,ZeroDivisionError,OverflowError)as e:error(e)
  except MemoryError:info('Memory','Restart Python; run EFIELD directly.')
