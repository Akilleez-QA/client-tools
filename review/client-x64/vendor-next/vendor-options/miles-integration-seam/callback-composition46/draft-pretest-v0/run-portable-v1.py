#!/usr/bin/env python3
"""One frozen portable attempt; never retries or replaces its evidence directory."""
import hashlib, json, os, pathlib, subprocess, time
root = pathlib.Path(__file__).resolve().parent
frozen = json.loads((root / 'freeze-v1.json').read_text())
for item in frozen['files']:
    if hashlib.sha256((root / item['path']).read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit('Frozen input differs: ' + item['path'])
evidence = root / 'evidence-v1'
evidence.mkdir(exist_ok=False)
binary = evidence / 'composition46-portable'
command = ['/usr/bin/clang++', '-std=c++11', '-Wall', '-Wextra', '-Wpedantic', '-Werror',
           '-O1', '-g', '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
           '-fno-omit-frame-pointer', '-include', str(root / 'portable-v1/native35_compat.h'),
           str(root / 'candidate/callback-control45/tests.cpp'),
           str(root / 'candidate/callback-composition46/selected_fixture.cpp'),
           str(root / 'candidate/callback-control45/host_association_mapper.cpp'),
           str(root / 'candidate/session-file-admission34/coordinator.cpp'),
           str(root / 'candidate/file-owner36/session_file_owner.cpp'),
           str(root / 'candidate/file-owner36/portable_job.cpp'),
           str(root / 'candidate/selected-file-services44/selected_services.cpp'),
           str(root / 'candidate/file-channel26/file_channel.cpp'),
           str(root / 'candidate/transport-candidate/codec.cpp'), '-o', str(binary)]
env = os.environ.copy()
env['ASAN_OPTIONS'] = 'detect_leaks=1:halt_on_error=1:abort_on_error=1'
env['UBSAN_OPTIONS'] = 'halt_on_error=1:print_stacktrace=1'
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
    result['pass'] = result['build_exit'] == 0 and result['run_exit'] == 0
    (evidence / 'results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['pass'] else 1)
