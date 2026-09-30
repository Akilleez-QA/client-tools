#!/usr/bin/env python3
"""Prospective one-shot gate. No default execution; parent review first."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

if sys.argv[1:] != ['--approved-portable-v2']:
    raise SystemExit('Requires reviewed --approved-portable-v2; no default execution')
root = Path(__file__).resolve().parent
freeze = json.loads((root / 'freeze-v2.json').read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect_inputs():
    mismatches = []
    for name, expected in freeze['sha256'].items():
        path = root / name
        try:
            actual = digest(path)
        except Exception as error:
            mismatches.append({'path': name, 'error': repr(error)})
            continue
        if actual != expected:
            mismatches.append({'path': name, 'expected': expected, 'actual': actual})
    for name, expected in freeze['tools'].items():
        try:
            actual = digest(Path(name))
        except Exception as error:
            mismatches.append({'tool': name, 'error': repr(error)})
            continue
        if actual != expected:
            mismatches.append({'tool': name, 'expected': expected, 'actual': actual})
    return mismatches

# Creating a fresh evidence directory is itself the no-retry guard.
output = root / 'evidence-v2'
output.mkdir(exist_ok=False)
result = {'scope': 'actual93 Core/Session, codec/reply, registry and BufferUpload; scripted Channel and Runtime; no host/SDK/Endpoint/ACK',
          'start': time.time(), 'freeze_sha256': digest(root / 'freeze-v2.json'),
          'compile': None, 'processes': [], 'passed': False}
env = os.environ.copy()
env['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1:abort_on_error=1'
env['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
result['sanitizer_environment'] = {k: env[k] for k in ('ASAN_OPTIONS', 'UBSAN_OPTIONS')}

modes = ['success', 'budget', 'malformed-begin', 'refused-release', 'malformed-release']
expected = {
    'success': ['PASS literal-signed-results-sequential-retirement', 'PASS literal-cross-frame-reconstruction'],
    'budget': ['PASS explicit-two-N-budget-restoration'],
    'malformed-begin': ['PASS malformed-begin-terminal-no-classification-return'],
    'refused-release': ['PASS refused-release-terminal-no-classification-return'],
    'malformed-release': ['PASS malformed-release-terminal-no-classification-return']}
command = ['/usr/bin/clang++', '-std=c++11', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
           '-O1', '-g', '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
           '-fno-omit-frame-pointer', '-include', str(root / 'compat.h'), str(root / 'tests.cpp')]
command += [str(root / 'tree' / p) for p in [
    'transport-candidate/codec.cpp', 'buffer-upload-candidate/buffer_upload.cpp',
    'session-version22/session_version.cpp', 'startup-metadata-v4/metadata_wire.cpp',
    'callback-reentry47/invocation_guard.cpp']]
command += ['-o', str(output / 'image98-portable')]

def run(argv, log_name, record, timeout):
    record.update({'command': argv, 'log': log_name, 'exit_code': None, 'start': time.time()})
    try:
        with (output / log_name).open('wb') as log:
            child = subprocess.run(argv, cwd=root, env=env, stdout=log,
                                   stderr=subprocess.STDOUT, timeout=timeout, check=False)
        record['exit_code'] = child.returncode
    except Exception as error:
        record['execution_error'] = repr(error)
        raise
    finally:
        record['end'] = time.time()
    if record['exit_code'] != 0:
        raise RuntimeError(log_name + ': nonzero exit; stopped without retry')

try:
    result['before_mismatches'] = inspect_inputs()
    if result['before_mismatches']:
        raise RuntimeError('Frozen input/tool identity mismatch before build')
    if json.loads((root / 'expected-markers.json').read_text()) != expected:
        raise RuntimeError('Mode/marker specification mismatch')
    result['compile'] = {}
    run(command, 'build.log', result['compile'], 120)
    for mode in modes:
        record = {'mode': mode}
        result['processes'].append(record)
        run([str(output / 'image98-portable'), mode], mode + '.log', record, 60)
        lines = (output / (mode + '.log')).read_text().splitlines()
        record['markers'] = {marker: lines.count(marker) for marker in expected[mode]}
        if any(count != 1 for count in record['markers'].values()):
            raise RuntimeError(mode + ': missing or duplicate scenario marker')
        scenario_lines = [line for line in lines if line.startswith('PASS ') and not line.startswith('PASS assertions=')]
        if scenario_lines != expected[mode]:
            raise RuntimeError(mode + ': unexpected scenario markers/order')
        summaries = [line for line in lines if line.startswith('PASS assertions=')]
        if len(summaries) != 1 or not summaries[0][len('PASS assertions='):].isdigit():
            raise RuntimeError(mode + ': missing/duplicate/malformed assertion count')
        record['assertions'] = int(summaries[0][len('PASS assertions='):])
        if record['assertions'] <= 0:
            raise RuntimeError(mode + ': empty assertion count')
        if any(line.startswith('FAIL') for line in lines):
            raise RuntimeError(mode + ': explicit failure output')
    result['scenario_count'] = sum(len(record['markers']) for record in result['processes'])
    result['assertion_count'] = sum(record['assertions'] for record in result['processes'])
    if len(result['processes']) != 5 or result['scenario_count'] != 6:
        raise RuntimeError('Exact five-process/six-scenario requirement failed')
except Exception as error:
    result['failure'] = repr(error)
finally:
    result['after_mismatches'] = inspect_inputs()
    try:
        result['freeze_changed'] = digest(root / 'freeze-v2.json') != result['freeze_sha256']
    except Exception as error:
        result['freeze_changed'] = True
        result['freeze_check_error'] = repr(error)
    result['end'] = time.time()
    result['passed'] = not result.get('failure') and not result['after_mismatches'] and not result['freeze_changed']
    (output / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
raise SystemExit(0 if result['passed'] else 1)
