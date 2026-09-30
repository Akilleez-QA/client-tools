"""Compile authored declaration/sample contracts only; no linking or execution."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
base = Path(__file__).resolve().parent
out = base / 'evidence-portable-v1'
out.mkdir(exist_ok=False)
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
inputs = [base / p for p in ['ClientMilesStartup.h', 'sample/install_order.h',
          'sample/install_order.cpp', 'tests/portable_contract.cpp', 'check-portable.py']]
inputs += [base.parent / p for p in ['backend-boundary24/ClientMiles.h',
           'reverse-file-seam20/ClientAudioFileCallbacks.h']]
before = {str(p): digest(p) for p in inputs}
compiler = Path(shutil.which('g++')).resolve()
result = {'compiler': str(compiler), 'compiler_sha256': digest(compiler),
          'linked': False, 'executed': False, 'vendor_loaded': False, 'before': before, 'checks': []}
for relative in ['sample/install_order.cpp', 'tests/portable_contract.cpp']:
    stem = Path(relative).stem
    command = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror', '-pedantic',
               '-MMD', '-MF', str(out / (stem + '.d')), '-c', str(base / relative),
               '-o', str(out / (stem + '.o'))]
    p = subprocess.run(command, text=True, capture_output=True, timeout=60)
    (out / (stem + '.log')).write_text(p.stdout + p.stderr)
    result['checks'].append({'command': command, 'exit': p.returncode})
result['after'] = {str(p): digest(p) for p in inputs}
result['passed'] = result['before'] == result['after'] and all(c['exit'] == 0 for c in result['checks'])
(out / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('before', 'after', 'checks')}, indent=2))
raise SystemExit(not result['passed'])
