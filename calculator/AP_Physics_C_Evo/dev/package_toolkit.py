"""Minify and losslessly pack TI sources, keeping readable originals.

Codec uses ASCII LZ77 back references and a tiny standard-Python decoder.
No calculator compression library or external dependency is needed.
"""
import ast, io, tokenize, collections, zipfile, json, zlib, base64
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'APC_EVO'
TARGET=ROOT/'APC_INSTALL'

LZ_LOADER='''# Lossless ASCII source decoder. Readable originals are in the release.
def decode(s):
 out=''
 i=0
 while i<len(s):
  if s[i]!='~':
   j=s.find('~',i)
   if j<0:j=len(s)
   out+=s[i:j]
   i=j
  elif s[i:i+2]=='~~':
   out+='~'
   i+=2
  else:
   j=s.find('~',i+1)
   a,b=s[i+1:j].split(',')
   distance,length=int(a),int(b)
   if distance<1 or distance>len(out):raise ValueError('Bad packed source')
   piece=out[-distance:]
   while len(piece)<length:piece+=piece
   out+=piece[:length]
   i=j+1
 return out
'''

def minify(source):
    parts=[]; depth=0; start=True; previous=None
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        kind,text=token.type,token.string
        if kind==tokenize.INDENT:
            depth+=1
            continue
        if kind==tokenize.DEDENT:
            depth-=1
            continue
        if kind in (tokenize.COMMENT,tokenize.NL,tokenize.ENDMARKER,tokenize.ENCODING):
            continue
        if kind==tokenize.NEWLINE:
            parts.append('\n');start=True;previous=None
            continue
        if start:
            parts.append(' '*depth);start=False
        if previous in (tokenize.NAME,tokenize.NUMBER,tokenize.STRING) and kind in (tokenize.NAME,tokenize.NUMBER,tokenize.STRING):
            parts.append(' ')
        parts.append(text);previous=kind
    result=''.join(parts)
    ast.parse(result)
    return result

def pack(source):
    # Greedy matches; limit search history and overlap lengths for build speed.
    index=collections.defaultdict(collections.deque)
    out=[]; i=0
    while i<len(source):
        best=0; distance=0
        key=source[i:i+3]
        for j in reversed(index[key]):
            if i-j>8192:break
            length=0
            while length<512 and i+length<len(source) and source[j+length]==source[i+length]:
                length+=1
            if length>best:
                best,distance=length,i-j
        token='~'+str(distance)+','+str(best)+'~'
        count=best if best>len(token) else 1
        if count>1:
            out.append(token)
        else:
            out.append('~~' if source[i]=='~' else source[i])
        for pos in range(i,i+count):
            q=index[source[pos:pos+3]]
            q.append(pos)
            if len(q)>30:q.popleft()
        i+=count
    return ''.join(out)

def main():
    TARGET.mkdir(exist_ok=True)
    for old in TARGET.glob('*.py'):old.unlink()
    loader=(ROOT/'dev'/'inflate_runtime.py').read_text('ascii')
    (TARGET/'APLOAD.py').write_text(minify(loader),encoding='ascii')
    ns={}
    exec(loader,ns)
    sizes={}
    for p in sorted(SOURCE.glob('*.py')):
        original=p.read_text('ascii')
        if p.stem.startswith('APU'):
            # Polynomial coefficients already encode these inverses exactly.
            # Keep branch count; omit redundant expression strings in release.
            entries=ast.literal_eval(ast.parse(original).body[0].value)
            slim=[]
            for entry in entries:
                title,eq,specs,inverses,note,polys=entry
                inverses=[['@']*len(inverses[i]) if polys[i] else inverses[i] for i in range(len(inverses))]
                slim.append((title,eq,specs,inverses,note,polys))
            original='F='+repr(slim)+'\n'
        compact=minify(original)
        compressor=zlib.compressobj(9,zlib.DEFLATED,-15)
        encoded=base64.b85encode(compressor.compress(compact.encode('ascii'))+compressor.flush()).decode('ascii')
        assert ns['decode'](encoded)==compact
        wrapper='from APLOAD import decode\nexec(decode('+repr(encoded)+'))\n'
        ast.parse(wrapper)
        (TARGET/p.name).write_text(wrapper,encoding='ascii')
        sizes[p.name]={'original':len(original),'minified':len(compact),'install':len(wrapper)}
    total=sum(p.stat().st_size for p in TARGET.glob('*.py'))
    (ROOT/'dev'/'package_sizes.json').write_text(json.dumps({'total':total,'files':sizes},indent=2))
    print('Install source total:',total,'bytes; files:',len(list(TARGET.glob('*.py'))))

if __name__=='__main__':main()
