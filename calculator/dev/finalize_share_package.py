"""Seal the share folder only after regression and profile checks succeed."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import zipfile

CALC=Path(__file__).resolve().parents[1]
ROOT=CALC.parent/'Share_AP_Physics_C_EM'
ZIP=CALC.parent/'Share_AP_Physics_C_EM.zip'
profiles=['TI84_EVO','TI84_PLUS_CE_PYTHON']

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    logs={'shared_solver_tests.txt':CALC/'dev/efield-v2-test-results.txt',
          'model_profile_tests.txt':CALC/'dev/share-package-test-results.txt'}
    counts={}
    for name,path in logs.items():
        text=path.read_text()
        assert text.rstrip().endswith('OK'),str(path)+' did not pass'
        count=re.search(r'Ran (\d+) tests',text)
        assert count
        counts[name]=int(count.group(1))
        shutil.copyfile(path,ROOT/'CHECKS'/name)
    validation=f'''VALIDATION — 2026-11-02

{counts['shared_solver_tests.txt']} shared regression test groups passed.
{counts['model_profile_tests.txt']} package/model-profile test groups passed, exercising both profiles.
Full logs are in CHECKS/. These are desktop tests, not calculator emulation.

The shared regression suite covers independent ring/rod numerical integration,
signs and limits, potential derivatives, extrema, inverse solves, arc components,
two-ring cancellation, menu routes, guide pagination, final-formula accuracy and
display coverage of every one of the 84 E&M catalog entries.

The package/profile checks cover complete 34-file installs, legal calculator
names, ASCII syntax, import dependencies, agreement of solver sources with the
tested release, Evo get_key(1), CE wait_key(), model-specific key maps, ignored
no-key events, keyboard calibration and a real menu selection using simulated
TI APIs, full ring calculation navigation, graphing API calls and highlight
alignment under each model's text-coordinate convention.

EVO PROFILE
Uses the Evo program's existing key support and measured 18-pixel text ascent.
Physical Evo transfer, working navigation and corrected highlight alignment were
confirmed during development. This share package preserves that GUI/solver code;
only the keyboard-calibration screen wording is made model-neutral. The latest
final-formula files were transferred during development; that section's routes
and equations were regression-tested on desktop.

PLUS CE PYTHON PROFILE
Uses the documented CE wait_key() codes and a zero text-ascent correction,
consistent with TI's upper-left text-coordinate API. It has the same solver,
formula and guide files as the Evo profile. Its API behavior was checked with
simulated TI modules; NO PHYSICAL CE PYTHON CALCULATOR WAS AVAILABLE. Actual CE
Python heap limits, display/font behavior and hardware keys must be checked on
the recipient's calculator using EFCHK and EFKEY before relying on it.

WHAT THE INCLUDED DEVICE CHECKS MEAN
EFCHK: 12 numerical physics checks + 2 wrap/menu-page checks. It does not test
physical key presses or prove that every graph renders correctly.
EFKEY: learns six physical keys and asks for a DOWN/ENTER menu test. It prints
PASS: hardware navigation only when the expected second item is selected.
APCHECK: 8 arithmetic, expression, quadratic and root checks.

The files are plain Python. No packed-source decoder is used. No desktop
Python packages or development environment are required by the recipient.
General custom-function limit/extremum sampling is numerical evidence, not a
symbolic proof. Calculator storage and Python runtime heap are different.
'''
    (ROOT/'VALIDATION.txt').write_text(validation)
    manifest={'package':'AP Physics C E&M / E-Field Studio',
              'release_date':'2026-11-02','edition':'E&M only; no Mechanics units',
              'profile_rule':'Install every .py from exactly one model TRANSFER folder.',
              'desktop_test_groups':counts,'profiles':{}}
    for profile in profiles:
        folder=ROOT/profile/'TRANSFER';files=sorted(folder.glob('*.py'))
        assert len(files)==34
        manifest['profiles'][profile]={
            'program_count':len(files),'source_bytes':sum(p.stat().st_size for p in files),
            'hardware_status':'Earlier Evo navigation/alignment verified' if profile=='TI84_EVO' else 'Not physically tested; simulated TI API checks passed',
            'files':[{'name':p.name,'bytes':p.stat().st_size,'sha256':digest(p)} for p in files]}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
    for p in files:
        assert '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='.DS_Store'
    sums=''.join(digest(p)+'  '+str(p.relative_to(ROOT))+'\n' for p in files)
    (ROOT/'SHA256SUMS.txt').write_text(sums)
    files.append(ROOT/'SHA256SUMS.txt')
    with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):z.write(p,str(p.relative_to(ROOT.parent)))
    with zipfile.ZipFile(ZIP) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
        for p in files:assert z.read(str(p.relative_to(ROOT.parent)))==p.read_bytes()
        assert len([n for n in z.namelist() if n.endswith('.py')])==68
    for line in sums.splitlines():
        expected,name=line.split('  ',1)
        assert digest(ROOT/name)==expected
    print('Ready:',ROOT)
    print('ZIP:',ZIP)
    print('ZIP size:',ZIP.stat().st_size,'bytes; files:',len(files))
    print('Tests:',sum(counts.values()),'groups passed; all hashes and ZIP contents verified')
    print('SHA256 ZIP:',digest(ZIP))

if __name__=='__main__':main()
