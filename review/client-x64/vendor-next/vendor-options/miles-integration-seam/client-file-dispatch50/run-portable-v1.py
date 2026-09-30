#!/usr/bin/env python3
"""One frozen portable attempt; never retries or replaces its evidence directory."""
import argparse, hashlib, json, os, pathlib, subprocess, time
parser=argparse.ArgumentParser()
parser.add_argument('--approved-portable',action='store_true')
if not parser.parse_args().approved_portable: parser.error('reviewed portable gate required')
root = pathlib.Path(__file__).resolve().parent
frozen = json.loads((root / 'freeze-v1.json').read_text())
for item in frozen['files']:
    if hashlib.sha256((root / item['path']).read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit('Frozen input differs: ' + item['path'])
evidence = root / 'evidence-v1'
evidence.mkdir(exist_ok=False)
binary = evidence / 'dispatch50-portable'
command = ['/usr/bin/clang++', '-std=c++11', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
           '-O1', '-g', '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
           '-fno-omit-frame-pointer', '-include', str(root / 'portable-v1/native35_compat.h'),
           str(root / 'portable-v1/callback-control45/tests.cpp'),
           str(root / 'portable-v1/callback-composition46/selected_fixture.cpp'),
           str(root / 'portable-v1/callback-control45/host_association_mapper.cpp'),
           str(root / 'portable-v1/session-file-admission34/coordinator.cpp'),
           str(root / 'portable-v1/file-owner36/session_file_owner.cpp'),
           str(root / 'portable-v1/file-owner36/portable_job.cpp'),
           str(root / 'portable-v1/selected-file-services44/selected_services.cpp'),
           str(root / 'portable-v1/file-channel26/file_channel.cpp'),
           str(root / 'portable-v1/transport-candidate/codec.cpp'),
           str(root / 'portable-v1/callback-protocol48/file_protocol.cpp'),
           str(root / 'portable-v1/callback-reentry47/invocation_guard.cpp'), '-o', str(binary)]
env = os.environ.copy()
env['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1:abort_on_error=1'
env['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
expected_markers = ['PASS distinct coordinator same session refused', 'PASS Pending forward join and older original ACK after newer intake', 'PASS ACK before forward return does not settle prematurely', 'PASS pending early unsent wrong-session unknown and duplicate ACK refused', 'PASS exact retained ACK context opcode registration and unused fields', 'PASS malformed file fields rejected before correlation publication', 'PASS sibling uncertainty retained across both slot poll orders and close ACK']
result = {'scope': 'portable real mapper/owner/selected-services/Invocation/codec with scripted worker/job; no ABI/Windows/engine/vendor evidence',
          'first_attempt': True, 'build_command': command, 'run_command': [str(binary)],
          'ASAN_OPTIONS': env['ASAN_OPTIONS'], 'UBSAN_OPTIONS': env['UBSAN_OPTIONS'],
          'start_epoch': time.time(), 'build_exit': None, 'run_exit': None}
(evidence / 'commands.json').write_text(json.dumps(result, indent=2)+'\n')
try:
    with (evidence / 'build.log').open('wb') as out:
        result['build_exit'] = subprocess.run(command, stdout=out, stderr=subprocess.STDOUT, timeout=120).returncode
    if result['build_exit'] == 0:
        with (evidence / 'run.log').open('wb') as out:
            result['run_exit'] = subprocess.run([str(binary)], env=env, stdout=out, stderr=subprocess.STDOUT, timeout=30).returncode
except Exception as exc:
    result['error'] = repr(exc)
finally:
    result['end_epoch'] = time.time()
    result['frozen_inputs_changed'] = [item['path'] for item in frozen['files']
        if not (root / item['path']).is_file() or
        hashlib.sha256((root / item['path']).read_bytes()).hexdigest() != item['sha256']]
    lines = (evidence / 'run.log').read_text(errors='replace').splitlines() if (evidence / 'run.log').exists() else []
    result['scenario_counts'] = {marker: lines.count(marker) for marker in expected_markers}
    result['all_scenarios_exactly_once'] = all(count == 1 for count in result['scenario_counts'].values())
    result['pass'] = (result['build_exit'] == 0 and result['run_exit'] == 0
        and not result['frozen_inputs_changed'] and result['all_scenarios_exactly_once'])
    (evidence / 'results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['pass'] else 1)
