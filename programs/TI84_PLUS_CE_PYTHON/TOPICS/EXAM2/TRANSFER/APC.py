from APCORE import menu,info,Cancel,error
from APMEM import release
from APBANK import TOPIC,ROUTES
UNITS=['Kinematics','Forces / dynamics','Work / energy / power','Linear momentum','Torque / rotation','Rotation energy / L','Oscillations','Charge / fields / Gauss','Electric potential','Conductors / capacitors','Electric circuits','Magnetic fields','Induction / RL / LC']
def unit_ui(start,end):
 while True:
  j=menu('APC equations',UNITS[start-1:end])
  if j<0:return
  name='APU%02d'%(start+j);mod=None
  try:
   mod=__import__(name)
   from APDATA import titles,entry
   from APFORM import formula_ui
   while True:
    i=menu(UNITS[start+j-1],titles(mod.DATA))
    if i<0:break
    f=entry(mod.DATA,i)
    while True:
     k=menu(f[0],['Solve an unknown','Graph this relation','Equation / variables'])
     if k<0:break
     try:
      if k==0:formula_ui(f)
      elif k==1:
       graph=__import__('APGRAPH');graph.plot_formula(f);graph=None;release(['APGRAPH'])
      else:info(f[0],f[1]+'\n'+'\n'.join(s[0]+' = '+s[1]+' ['+s[2]+']' for s in f[2])+'\n'+f[4])
     except Cancel:pass
     except(ValueError,ZeroDivisionError,OverflowError)as e:error(e)
  finally:
   mod=None;release([name,'APDATA','APFORM','APNUM','APGRAPH'])
def guides():
 from EFMODEL import NAMES
 while True:
  i=menu('Field derivations',NAMES)
  if i<0:return
  mod=__import__('EFNOTE')
  try:mod.guide(i)
  finally:
   mod=None;release(['EFNOTE']+['EFN'+str(n)for n in range(5)])
def help():
 info('CE topics','All APC content is included in the download. The CE Python workspace is limited, so install one topic at a time. EXAM2: Gauss, energy and study cards. FIELD_STUDIO: calculations, inverses and plots. FIELD_GUIDES: complete derivations. FINAL_FORMULAS: final answers and E&M reference. MECHANICS, EM_REFERENCE: equation solvers. MATH_TOOLS: multi-step solvers, calculus and graphs. See CE_GUIDE.md. Use SI units; follow angle prompts. q cancels numeric input.')
def main():
 while True:
  i=menu('APC / '+TOPIC,[r[0]for r in ROUTES]+['Other topics / help'])
  if i<0:return
  if i==len(ROUTES):help();continue
  label,name,action=ROUTES[i];mod=None
  try:
   if name=='MECH':unit_ui(1,7)
   elif name=='EM':unit_ui(8,13)
   elif name=='GUIDES':guides()
   else:
    mod=__import__(name);getattr(mod,action)()
  except ImportError:help()
  except Cancel:pass
  except(ValueError,ZeroDivisionError,OverflowError)as e:error(e)
  except MemoryError:info('Memory','Quit and restart Python. Keep only the selected CE topic in RAM; archive unrelated Python files. Run APC again.')
  finally:
   mod=None;release([name,'E2APP','E2NOTES','E2CALC','E2PHYS','E2CHECK','EFAPP','EFMODEL','EFTOOLS','EFCALC','EFINPUT','EFINV','EFEXT','EFPLOT','EFFINAL','EFNOTE','APDATA','APFORM','APNUM','APGRAPH','APMATH','APTOOLS','APMECH','APEM','APLAB']+['EFN'+str(n)for n in range(5)])
main()
