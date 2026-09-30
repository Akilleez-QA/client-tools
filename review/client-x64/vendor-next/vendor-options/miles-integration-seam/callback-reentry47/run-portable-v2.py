#!/usr/bin/env python3
"""One reviewed authored-only portable gate; never invokes vendor/engine code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--approved-portable', action='store_true')
a = p.parse_args()
if not a.approved_portable:
    p.error('explicit reviewed portable gate required')
root = Path(__file__).resolve().parent
manifest = root / 'composition-freeze-v2.json'
expected = json.loads(manifest.read_text())['files']
def identities():
    result = {}
    for entry in expected:
        path = root / entry['path']
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != entry['sha256']:
            raise RuntimeError('input mismatch: ' + entry['path'])
        result[entry['path']] = actual
    return result
before = identities()
evidence = root / 'portable-evidence-v2'
evidence.mkdir(exist_ok=False)  # Previous failure/success cannot be overwritten.
source = root / 'portable-composition-v2'
roots = json.loads((root / 'composition-provenance-v2.json').read_text())['roots']
command = ['g++', '-std=c++11', '-Wall', '-Wextra', '-Werror', '-pedantic',
           '-fsanitize=address,undefined', '-fno-omit-frame-pointer', '-g', '-pthread']
command += [str(source / name) for name in roots]
command += ['-o', str(evidence / 'guard47-test')]
run = [str(evidence / 'guard47-test')]
(evidence / 'commands.json').write_text(json.dumps({'build': command, 'run': run}, indent=2)+'\n')
receipt = {'manifest_sha256': hashlib.sha256(manifest.read_bytes()).hexdigest(),
           'before': before, 'build_attempted': False, 'run_attempted': False,
           'scope': 'Authored portable test only; no SDK/native/engine runtime'}
env = os.environ.copy()
env['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1'
env['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
def invoke(command, log, seconds):
    with (evidence / log).open('wb') as output:
        completed = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                                   timeout=seconds, env=env, check=False)
    return completed.returncode
try:
    receipt['compiler_version_exit'] = invoke(['g++', '--version'], 'compiler-version.log', 15)
    if receipt['compiler_version_exit'] != 0:
        raise RuntimeError('compiler identification failed')
    receipt['build_attempted'] = True
    receipt['build_exit'] = invoke(command, 'build.log', 120)
    if receipt['build_exit'] != 0:
        raise RuntimeError('first compilation failed; no retry')
    receipt['run_attempted'] = True
    receipt['run_exit'] = invoke(run, 'run.log', 30)
    if receipt['run_exit'] != 0:
        raise RuntimeError('first test failed; no retry')
    receipt['passed'] = True
except Exception as error:
    receipt['passed'] = False
    receipt['failure'] = str(error)
finally:
    try:
        receipt['after'] = identities()
    except Exception as error:
        receipt['passed'] = False
        receipt['identity_failure'] = str(error)
    (evidence / 'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
sys.exit(0 if receipt.get('passed') else 1)
