from math import sqrt,sin,cos,tan,asin,acos,atan,exp,log,pi
CONST={'pi':pi,'e':exp(1),'g':9.8,'G':6.6743e-11,'ke':8987551792.3,'eps0':8.8541878128e-12,'mu0':1.25663706212e-06,'qe':1.602176634e-19,'me':9.1093837139e-31,'mp':1.67262192595e-27,'c0':299792458.0}
ln=log
FUN='sqrt sin cos tan asin acos atan exp ln log abs'.split()
LAST=[0.0]
WIDTH=28
class Cancel(Exception):
 pass
def finite(x):
 return isinstance(x,(int,float))and x==x and(abs(x)<1e+300)
def calc(text,values=None):
 values={}if values is None else values
 s=text.replace(' ','').replace('**','^')
 out=''
 bindings=[]
 i=0
 while i<len(s):
  c=s[i]
  j=i+1
  if c in '0123456789' or c=='.':
   while j<len(s)and(s[j]in '0123456789' or s[j]=='.'):
    j+=1
   if j<len(s)and s[j]in 'eE':
    j+=1
    if j<len(s)and s[j]in '+-':
     j+=1
    while j<len(s)and s[j]in '0123456789':
     j+=1
   token=s[i:j]
   float(token)
   out+=token
  elif c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
   while j<len(s)and s[j]in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789':
    j+=1
   name=s[i:j]
   if j<len(s)and s[j]=='(':
    if name not in FUN:
     raise ValueError('Unknown function')
    out+=name
   else:
    if name in values:
     value=values[name]
    elif name=='ans':
     value=LAST[0]
    elif name in CONST:
     value=CONST[name]
    else:
     raise ValueError('Unknown name: '+name)
    out+='_v'+str(len(bindings))
    bindings.append(value)
  elif c in '+-*/^()':
   out+='**' if c=='^' else c
  else:
   raise ValueError('Use arithmetic syntax')
  i=j
 scope=globals()
 for k in range(len(bindings)):
  scope['_v'+str(k)]=bindings[k]
 try:
  v=eval(out)
 except(SyntaxError,NameError,TypeError):
  raise ValueError('Invalid expression')
 finally:
  for k in range(len(bindings)):
   del scope['_v'+str(k)]
 if not finite(v):
  raise ValueError('Invalid or non-real result')
 return v
def magnitude(s,vals):
 depth=0
 start=0
 total=0.0
 for i in range(len(s)):
  c=s[i]
  if c=='(':
   depth+=1
  elif c==')':
   depth-=1
  elif c in '+-' and depth==0 and(i>start)and(s[i-1]not in '+-*/^eE'):
   total+=abs(calc(s[start:i],vals))
   start=i
 return total+abs(calc(s[start:],vals))
def checked_sides(lhs,rhs,vals,tolerance=1e-07):
 l,r=(calc(lhs,vals),calc(rhs,vals))
 scale=max(magnitude(lhs,vals),magnitude(rhs,vals),abs(l),abs(r),1e-300)
 return abs(l-r)<=tolerance*scale
try:
 from ti_system import disp_clr
except ImportError:
 def disp_clr():
  print('\n'*2)
def wrap(text):
 out=[]
 for para in str(text).split('\n'):
  line=''
  for word in para.split(' '):
   while len(word)>WIDTH:
    if line:
     out.append(line)
     line=''
    out.append(word[:WIDTH])
    word=word[WIDTH:]
   if len(line)+len(word)+1>WIDTH:
    out.append(line)
    line=''
   line=(line+' '+word).strip()
  out.append(line)
 return out
def head(title):
 disp_clr()
 print(('APC | '+title)[:WIDTH])
 print('='*WIDTH)
def info(title,text):
 from EFGUI import read
 read(title,text)
def menu(title,items):
 from EFGUI import choose
 return choose(title,items)
def number(label,domain='s',default=None):
 while True:
  disp_clr()
  for line in wrap(label):
   print(line)
  print('SI units | q cancels')
  if default is not None:
   print('ENTER keeps '+fmt(default))
  s=input('> ').strip()
  if s.lower()in('q','b'):
   raise Cancel()
  try:
   x=default if s=='' and default is not None else calc(s)
   if domain=='+' and x<=0:
    raise ValueError('Must be > 0')
   if domain=='0' and x<0:
    raise ValueError('Must be >= 0')
   return x
  except(ValueError,ZeroDivisionError,OverflowError)as e:
   info('Check input',str(e))
def integer(label,lo,hi):
 while True:
  x=number(label)
  if x==int(x)and lo<=x<=hi:
   return int(x)
  print('Integer '+str(lo)+'..'+str(hi))
def fmt(x):
 return '{:.7g}'.format(x)
def result(title,pairs,note=''):
 lines=[]
 for name,v in pairs:
  if not finite(v):
   raise ValueError('Non-real or overflow result')
  LAST[0]=v
  lines.append(name+' = '+fmt(v))
 info(title,'\n'.join(lines)+('\n'+note if note else ''))
def error(e):
 info('Check inputs',str(e)+'\nUse SI units. q cancels.')
