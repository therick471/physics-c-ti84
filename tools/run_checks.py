"""Run each existing regression suite in a separate Python process."""
from pathlib import Path
import os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
logs=ROOT/'checks';logs.mkdir(exist_ok=True)
suites=['test_lite.py','test_efield.py','test_share_package.py','test_exam2.py','test_banner_fix.py']
failed=[]
for suite in suites:
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    result=subprocess.run([sys.executable,str(ROOT/'calculator/dev'/suite)],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    text=result.stdout.replace(str(ROOT),'<repository>')
    (logs/(suite[:-3]+'.txt')).write_text(text)
    print(suite+': '+('PASS' if result.returncode==0 else 'FAIL'))
    if result.returncode:failed.append(suite)
result=subprocess.run([sys.executable,str(ROOT/'tools/verify_repository.py')],cwd=ROOT)
sys.exit(bool(failed) or result.returncode)
