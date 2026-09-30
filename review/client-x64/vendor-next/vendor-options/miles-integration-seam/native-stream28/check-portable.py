"""Compile public declarations/example only; no SDK, link or executable."""
from pathlib import Path
import ast
import hashlib
import json
import re
import shutil
import subprocess

base = Path(__file__).resolve().parent
out = base / 'evidence-portable-v1'
build = base / 'private-portable-v1'
out.mkdir(exist_ok=False)
build.mkdir(mode=0o700, exist_ok=False)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


compiler = Path(shutil.which('g++')).resolve()
nm = Path(shutil.which('nm')).resolve()
manifest = json.loads((base / 'source-manifest.json').read_text())
inputs = [base.parent / relative for relative in manifest]
inputs += [base / 'source-manifest.json', compiler, nm]
before = {str(path): digest(path) for path in inputs}
result = {'scope': __doc__, 'linked': False, 'executed': False,
          'before': before, 'checks': []}
try:
    for relative, expected in manifest.items():
        if digest(base.parent / relative) != expected:
            raise RuntimeError('frozen source changed: ' + relative)
    for script in base.glob('*.py'):
        ast.parse(script.read_text(), filename=str(script))
    for name in ['stream_calls.cpp', 'portable_contract.cpp']:
        source = base / name
        command = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror', '-pedantic',
                   '-c', str(source), '-o', str(build / (source.stem + '.o'))]
        completed = subprocess.run(command, capture_output=True, timeout=60)
        (out / (source.stem + '.log')).write_bytes(completed.stdout + completed.stderr)
        (out / (source.stem + '-command.json')).write_text(json.dumps(command, indent=2) + '\n')
        result['checks'].append({'source': name, 'exit': completed.returncode})
        if completed.returncode:
            raise RuntimeError('portable compile failed; preserve first result')

    command = [str(nm), '-C', '-u', str(build / 'stream_calls.o')]
    symbols = subprocess.run(command, capture_output=True, timeout=15)
    (out / 'stream-symbols.log').write_bytes(symbols.stdout + symbols.stderr)
    (out / 'stream-symbols-command.json').write_text(json.dumps(command, indent=2) + '\n')
    required = {'open_stream', 'close_stream', 'start_stream', 'set_stream_loop_count',
                'set_stream_loop_block', 'stream_status', 'set_stream_ms_position',
                'stream_ms_position'}
    observed = set(re.findall(r'\bClientMiles::([A-Za-z_]\w*)\(',
                              symbols.stdout.decode('utf-8', errors='strict')))
    result['undefined_facade_functions'] = sorted(observed)
    result['exact_eight_unresolved'] = observed == required
    if symbols.returncode or observed != required:
        raise RuntimeError('example does not retain exactly eight unresolved facade functions')
    result['objects'] = {path.name: digest(path) for path in sorted(build.glob('*.o'))}
except Exception as error:
    result['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    result['after'] = {str(path): digest(path) for path in inputs}
    result['passed'] = (not result.get('failure') and before == result['after'] and
                        len(result.get('objects', {})) == 2)
    receipt = out / 'receipt.json'
    receipt.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'passed': result['passed'], 'receipt_sha256': digest(receipt),
                      'linked': False, 'executed': False,
                      'failure': result.get('failure')}, indent=2))
raise SystemExit(not result['passed'])
