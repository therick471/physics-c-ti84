"""Check packaged provenance, current install dependencies, syntax and ZIP integrity."""
from pathlib import Path
import ast, hashlib, json, re, zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
manifest=json.loads((ROOT/'source-manifest.json').read_text())
for f in manifest['files']:
    p=ROOT/f['path'];assert p.is_file(),p
    assert sha(p.read_bytes())==f['sha256'],p
for p in (ROOT/'downloads').glob('*.zip'):
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None,p
        for name in z.namelist():
            assert not any(x in {'.DS_Store','__MACOSX','__pycache__'} or x.startswith('._') for x in Path(name).parts),(p,name)
            assert not name.endswith('.pyc'),(p,name)
allowed={'math','sys','gc','ti_system','ti_draw','ti_plotlib'}
profiles=[('calculator/Exam2_Evo/TRANSFER',40),('calculator/AP_Physics_C_Evo_Fixed/TRANSFER_FIRST',22),('Share_AP_Physics_C_EM/TI84_EVO/TRANSFER',34),('Share_AP_Physics_C_EM/TI84_PLUS_CE_PYTHON/TRANSFER',34)]
for path,count in profiles:
    folder=ROOT/path;files=list(folder.glob('*.py'));assert len(files)==count,(path,len(files))
    names={p.stem for p in files}|allowed
    if count==22:names|={'APTOOLS','APMECH','APEM','APLAB'}
    for p in files:
        assert re.fullmatch('[A-Z][A-Z0-9]{0,7}',p.stem),p
        tree=ast.parse(p.read_text('ascii'))
        for node in ast.walk(tree):
            deps=[n.name for n in node.names] if isinstance(node,ast.Import) else ([node.module] if isinstance(node,ast.ImportFrom) else [])
            for dep in deps:assert dep in names,(p,dep)
with zipfile.ZipFile(ROOT/'downloads/Exam2_Evo.zip') as z:
    for p in (ROOT/'calculator/Exam2_Evo/TRANSFER').glob('*.py'):
        member='Exam2_Evo/TRANSFER/'+p.name
        assert z.read(member)==p.read_bytes(),member
for p in ROOT.rglob('*.md'):
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if '://' in target or target.startswith('#'):continue
        target=target.split('#')[0]
        if target:assert (p.parent/target).exists(),(p,target)
print('PASS: source hashes, ZIP integrity, complete installs, imports, ASCII names/syntax, Exam 2 ZIP/source parity, Markdown links')
print(str(len(manifest['files']))+' original files indexed')
