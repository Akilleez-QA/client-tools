#!/usr/bin/env python3
"""Prospective protocol48 first gate. One build and at most one run; no retries."""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import time

root = pathlib.Path(__file__).resolve().parent
freeze_path = root / 'test-freeze-v1.json'
freeze_bytes = freeze_path.read_bytes()
freeze = json.loads(freeze_bytes)

def changed_inputs():
    return [item['path'] for item in freeze['files']
            if not (root / item['path']).is_file()
            or hashlib.sha256((root / item['path']).read_bytes()).hexdigest() != item['sha256']]

changed = changed_inputs()
if changed:
    raise SystemExit('Frozen inputs differ: ' + ', '.join(changed))
evidence = root / 'evidence-v1'
evidence.mkdir(exist_ok=False)
binary = evidence / 'protocol48-portable'
command = [
    '/usr/bin/clang++', '-std=c++11', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
    '-O1', '-g', '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
    '-fno-omit-frame-pointer',
    str(root / 'portable-v1/tests.cpp'),
    str(root / 'candidate/callback-protocol48/file_protocol.cpp'),
    str(root / 'candidate/file-channel26/file_channel.cpp'),
    str(root / 'candidate/transport-candidate/codec.cpp'), '-o', str(binary)
]
markers = [
    'PASS independent golden install reply and ACK bytes',
    'PASS bounded and vector Call encoding payloads and rejection sentinels',
    'PASS install request exact fields origin and malformed lengths',
    'PASS install statuses exact echo and unchanged rejected output',
    'PASS retained file ACK origins opcodes registration and stateless duplicate boundary',
    'PASS typed fixed encoders bounds and unchanged failure output',
    'PASS stream parent echo nullable alias and malformed success rejection',
    'PASS old versions rejected across all codec and typed surfaces',
]
env = os.environ.copy()
env['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1:abort_on_error=1'
env['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
record = {
    'scope': 'portable protocol48 helper, codec and file-channel only; no SDK, worker, mapper, endpoint or native ABI execution',
    'first_frozen_runner_attempt': True,
    'test_freeze_sha256': hashlib.sha256(freeze_bytes).hexdigest(),
    'build_command': command, 'run_command': [str(binary)],
    'build_timeout_seconds': 120, 'run_timeout_seconds': 30,
    'ASAN_OPTIONS': env['ASAN_OPTIONS'], 'UBSAN_OPTIONS': env['UBSAN_OPTIONS'],
    'start_epoch': time.time(), 'build_exit': None, 'run_exit': None,
}
(evidence / 'commands.json').write_text(json.dumps(record, indent=2) + '\n')
try:
    with (evidence / 'build.log').open('wb') as output:
        record['build_exit'] = subprocess.run(command, stdout=output, stderr=subprocess.STDOUT,
                                              timeout=120, cwd=root).returncode
    if record['build_exit'] == 0:
        with (evidence / 'run.log').open('wb') as output:
            record['run_exit'] = subprocess.run([str(binary)], stdout=output, stderr=subprocess.STDOUT,
                                                timeout=30, env=env, cwd=root).returncode
except Exception as exc:
    record['error'] = repr(exc)
finally:
    record['end_epoch'] = time.time()
    record['frozen_inputs_changed'] = changed_inputs()
    record['test_freeze_changed'] = freeze_path.read_bytes() != freeze_bytes
    run_log = evidence / 'run.log'
    lines = run_log.read_text(errors='replace').splitlines() if run_log.exists() else []
    record['scenario_counts'] = {marker: lines.count(marker) for marker in markers}
    record['all_scenarios_exactly_once'] = all(n == 1 for n in record['scenario_counts'].values())
    totals = [re.fullmatch(r'PASS ([1-9][0-9]*) protocol48 checks; no SDK or endpoint execution', line)
              for line in lines]
    totals = [match for match in totals if match is not None]
    record['reported_check_count'] = int(totals[0].group(1)) if len(totals) == 1 else None
    record['unexpected_output'] = [line for line in lines if line not in markers
                                    and not re.fullmatch(r'PASS ([1-9][0-9]*) protocol48 checks; no SDK or endpoint execution', line)]
    record['artifact_sha256'] = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in (evidence / 'build.log', run_log, binary) if p.is_file()
    }
    record['pass'] = (record['build_exit'] == 0 and record['run_exit'] == 0
                      and not record['frozen_inputs_changed'] and not record['test_freeze_changed']
                      and record['all_scenarios_exactly_once'] and len(totals) == 1
                      and not record['unexpected_output'])
    (evidence / 'results.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
raise SystemExit(0 if record['pass'] else 1)
