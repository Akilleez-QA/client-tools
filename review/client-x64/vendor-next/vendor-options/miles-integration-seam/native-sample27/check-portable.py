"""Compile declarations and usage excerpt only; no SDK, link or executable."""
from pathlib import Path
import ast
import hashlib
import json
import shutil
import subprocess
import sys

base = Path(__file__).resolve().parent
out = base / 'evidence-portable-v1'
build = base / 'private-portable-v1'
out.mkdir(exist_ok=False)
build.mkdir(mode=0o700, exist_ok=False)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


compiler = Path(shutil.which('g++')).resolve()
nm = Path(shutil.which('nm')).resolve()
inputs = [base / p for p in ['ClientMilesSample.h', 'sample_time.h', 'sample_time.cpp',
          'portable_contract.cpp', 'native_sample27.cpp', 'build-native.py', 'check-portable.py']]
inputs += [base.parent / 'backend-boundary24/ClientMiles.h', compiler, nm]
before = {str(p): digest(p) for p in inputs}
result = {'scope': __doc__, 'linked': False, 'executed': False, 'before': before, 'checks': []}
try:
    for script in base.glob('*.py'):
        ast.parse(script.read_text(), filename=str(script))
    for name in ['sample_time.cpp', 'portable_contract.cpp']:
        source = base / name
        command = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror', '-pedantic',
                   '-c', str(source), '-o', str(build / (source.stem + '.o'))]
        completed = subprocess.run(command, capture_output=True, timeout=60)
        (out / (source.stem + '.log')).write_bytes(completed.stdout + completed.stderr)
        (out / (source.stem + '-command.json')).write_text(json.dumps(command, indent=2) + '\n')
        result['checks'].append({'source': name, 'exit': completed.returncode})
        if completed.returncode:
            raise RuntimeError('portable compile failed; preserve first result')
    symbols = subprocess.run([str(nm), '-C', '-u', str(build / 'sample_time.o')],
                             capture_output=True, timeout=15)
    (out / 'sample-symbols.log').write_bytes(symbols.stdout + symbols.stderr)
    (out / 'sample-symbols-command.json').write_text(json.dumps(
        [str(nm), '-C', '-u', str(build / 'sample_time.o')], indent=2) + '\n')
    required = ['allocate_sample_handle', 'set_named_sample_file', 'sample_ms_position',
                'end_sample', 'release_sample_handle']
    result['sample_references_all_five'] = all(
        ('ClientMiles::' + name + '(').encode() in symbols.stdout for name in required)
    if symbols.returncode or not result['sample_references_all_five']:
        raise RuntimeError('sample does not retain all five unresolved facade references')
    result['objects'] = {p.name: digest(p) for p in sorted(build.glob('*.o'))}
except Exception as error:
    result['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    result['after'] = {str(p): digest(p) for p in inputs}
    result['passed'] = not result.get('failure') and before == result['after']
    path = out / 'receipt.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'passed': result['passed'], 'sha256': digest(path),
                      'linked': False, 'executed': False, 'failure': result.get('failure')}, indent=2))
raise SystemExit(not result['passed'])
