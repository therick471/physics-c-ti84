from EFGUI import KEYMAP,raw_key,choose
from APCORE import disp_clr
def main():
 keys=[('UP','up'),('DOWN','down'),('LEFT','prev'),('RIGHT','next'),('ENTER','enter'),('CLEAR','back')]
 bindings={}
 for label,action in keys:
  while True:
   disp_clr()
   print('KEY SETUP  v3')
   print('Press and RELEASE '+label)
   print('Use the calculator keypad.')
   code=raw_key()
   if code not in bindings:break
   print('Same code twice. Try again.')
  bindings[code]=action
 KEYMAP.clear();KEYMAP.update(bindings)
 disp_clr()
 print('Keys learned:')
 for code in bindings:print(str(code)+' = '+bindings[code])
 input('ENTER to test ')
 result=choose('TEST: DOWN then ENTER',['First item','Select this item'])
 if result!=1:
  disp_clr();print('Test incomplete. Run EFKEY again.');return
 disp_clr();print('PASS: hardware navigation')
 print('Bindings apply this session.')
 input('ENTER opens APC ')
 __import__('APC')
main()
