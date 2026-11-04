LB=[3,4,5,6,7,8,9,10,11,13,15,17,19,23,27,31,35,43,51,59,67,83,99,115,131,163,195,227,258]
LE=[0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,0]
DB=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025,1537,2049,3073,4097,6145,8193,12289,16385,24577]
DE=[0,0,0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13]
class Bits:
 def __init__(self,encoded):
  self.d=bytearray()
  alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
  digits={alphabet[i]:i for i in range(85)}
  for i in range(0,len(encoded),5):
   part=encoded[i:i+5]
   size=len(part)
   part+=alphabet[84]*(5-size)
   value=0
   for ch in part:value=value*85+digits[ch]
   for j in range(size-1):self.d.append((value>>(24-8*j))&255)
  self.p=0
 def read(self,n):
  value=0
  for i in range(n):
   if self.p//8>=len(self.d):raise ValueError('Truncated source')
   value|=((self.d[self.p//8]>>(self.p%8))&1)<<i
   self.p+=1
  return value
def tree(lengths):
 counts={i:0 for i in range(16)}
 for length in lengths.values():
  if length:counts[length]+=1
 code=0
 nextcode={}
 for length in range(1,16):
  code=(code+counts[length-1])<<1
  nextcode[length]=code
 table={}
 for symbol in range(len(lengths)):
  length=lengths[symbol]
  if not length:continue
  c=nextcode[length]
  nextcode[length]+=1
  reverse=0
  for i in range(length):
   reverse=(reverse<<1)|((c>>i)&1)
  table[(length,reverse)]=symbol
 return table
def symbol(bits,table):
 code=0
 for length in range(1,16):
  code|=bits.read(1)<<(length-1)
  key=(length,code)
  if key in table:return table[key]
 raise ValueError('Bad source Huffman code')
def tables(bits,kind):
 if kind==1:
  lengths={}
  for i in range(288):
   lengths[i]=8 if i<144 else(9 if i<256 else(7 if i<280 else 8))
  return tree(lengths),tree({i:5 for i in range(32)})
 if kind!=2:raise ValueError('Bad source block')
 nl,nd,nc=bits.read(5)+257,bits.read(5)+1,bits.read(4)+4
 order=[16,17,18,0,8,7,9,6,10,5,11,4,12,3,13,2,14,1,15]
 cl={i:0 for i in range(19)}
 for i in range(nc):cl[order[i]]=bits.read(3)
 ct=tree(cl)
 lengths={};i=0
 while i<nl+nd:
  value=symbol(bits,ct)
  if value<16:
   lengths[i]=value;i+=1
  else:
   if value==16:
    if i==0:raise ValueError('Bad repeat')
    length=lengths[i-1];count=bits.read(2)+3
   elif value==17:
    length=0;count=bits.read(3)+3
   else:
    length=0;count=bits.read(7)+11
   if i+count>nl+nd:raise ValueError('Too many lengths')
   for j in range(count):lengths[i+j]=length
   i+=count
 return tree({i:lengths[i]for i in range(nl)}),tree({i:lengths[nl+i]for i in range(nd)})
def decode(encoded):
 bits=Bits(encoded)
 out=bytearray()
 final=0
 while not final:
  final,kind=bits.read(1),bits.read(2)
  if kind==0:
   bits.p=((bits.p+7)//8)*8
   length=bits.read(16)
   if bits.read(16)!=(length^65535):raise ValueError('Bad source length')
   for i in range(length):out.append(bits.read(8))
   continue
  lt,dt=tables(bits,kind)
  while True:
   value=symbol(bits,lt)
   if value<256:
    out.append(value)
   elif value==256:
    break
   else:
    idx=value-257
    if idx>=len(LB):raise ValueError('Bad match length')
    length=LB[idx]+bits.read(LE[idx])
    ds=symbol(bits,dt)
    if ds>=len(DB):raise ValueError('Bad match distance')
    distance=DB[ds]+bits.read(DE[ds])
    if distance>len(out):raise ValueError('Bad source distance')
    for i in range(length):out.append(out[-distance])
 return out.decode('ascii')
