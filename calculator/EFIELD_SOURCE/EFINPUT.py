from math import pi
from APCORE import head,number,menu,Cancel
from EFMODEL import NAMES
def parameters(kind):
    head(NAMES[kind])
    d=number('R m' if kind in (0,4) else ('Full rod L m' if kind in (1,2) else 'Reference R m'),'+')
    phi=pi
    if kind==4: phi=number('Arc sweep degrees','+')*pi/180
    if kind==3: q=number('lambda C/m')
    else:
        choice=menu('Given charge',['Total Q coulombs','Linear density lambda C/m'])
        if choice<0: raise Cancel()
        q=number('Q coulombs' if choice==0 else 'lambda C/m')
        if choice==1: q*=2*pi*d if kind==0 else (d*phi if kind==4 else d)
    return q,d,phi
