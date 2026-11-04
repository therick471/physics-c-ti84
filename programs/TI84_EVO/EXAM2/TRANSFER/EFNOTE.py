from APMEM import release
from EFMODEL import NAMES
from EFGUI import cards
def guide(kind):
 name='EFN'+str(kind)
 mod=__import__(name)
 steps=[]
 for line in mod.DATA.split('\n'):
  split=line.find('|')
  steps.append((line[:split],line[split+1:]))
 cards(NAMES[kind],steps)
 steps=None
 mod=None
 release([name])
