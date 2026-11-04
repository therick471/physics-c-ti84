from APCORE import menu,number,info,result
from EFMODEL import field,ring_distances,inverse_distance
def inverse(kind):
 if kind==4:info('Arc inverse','Use the numeric evaluator or E&M equation reference for charge/radius. Choose the fixed parameter before varying arc sweep.');return
 which=menu('Solve backward',['Source Q (line: lambda)','Distance x from E'])
 if which<0:return
 d=number('R m' if kind in(0,3)else 'Full L m','+')
 target=number('Signed E N/C')
 if which==0:
  x=number('x m','+' if kind==2 else 's')
  unit=field(kind,1,d,x)[0]
  if unit==0:raise ValueError('At ring center E=0 for every Q')
  result('Source',[('lambda C/m' if kind==3 else 'Q C',target/unit)])
 else:
  q=number('lambda C/m' if kind==3 else 'Q C')
  roots=ring_distances(q,d,target)if kind==0 else[inverse_distance(kind,q,d,target)]
  result('Positive-side x',[('x m',r)for r in roots],'Ring can give TWO distances. E=0 has x=0; infinity is a limit, not another finite root.')
