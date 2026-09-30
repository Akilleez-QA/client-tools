#!/usr/bin/env python3
"""Prospective one-attempt portable gate. Does not run SDK/native/engine code."""
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'evidence-v1'
SOURCE_FREEZE_SHA256 = 'd99a5ffdb5e52484ce7a7bbab786300ab2aaf177771f106035468f8e79c38f00'
CREATED_EVIDENCE = False
OPS = ['startup', 'shutdown', 'get_preference', 'set_preference', 'last_error',
       'set_redist_directory', 'MSS_version', 'open_digital_driver', 'speaker_configuration_spec']
SCENARIOS = ['prestartup-separate-copied-snapshots', 'self-alias-and-retained-directory-growth',
             'null-versus-empty-text', 'native-status-and-pointer-width-preferences',
             'full-driver-and-speaker-forwarding', 'version-exact-writes-no-extra-guarantee',
             'shutdown-retention-and-second-lifecycle']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def frozen_inputs():
    source = ROOT / 'source-manifest-v1.json'
    if digest(source) != SOURCE_FREEZE_SHA256:
        raise RuntimeError('source freeze identity changed')
    result = {'source-manifest-v1.json': digest(source)}
    for manifest_name in ['source-manifest-v1.json', 'test-manifest-v1.json']:
        manifest = json.loads((ROOT / manifest_name).read_text())
        result[manifest_name] = digest(ROOT / manifest_name)
        for entry in manifest['files']:
            path = ROOT / entry['path']
            actual = digest(path)
            if actual != entry['sha256']:
                raise RuntimeError('frozen input changed: ' + entry['path'])
            result[entry['path']] = actual
    return result

def main():
    global CREATED_EVIDENCE
    if len(sys.argv) != 1:
        raise RuntimeError('no overrides accepted')
    before = frozen_inputs()
    OUT.mkdir()  # Exclusive: existing evidence forbids a retry/overwrite.
    CREATED_EVIDENCE = True
    (OUT / 'inputs-before.json').write_text(json.dumps(before, indent=2) + '\n')
    # Inherited by all children; no system-wide setting or core dump workload.
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    compiler = shutil.which('clang++')
    if not compiler:
        raise RuntimeError('clang++ required')
    env = dict(os.environ)
    for key in ['CPATH', 'CPLUS_INCLUDE_PATH', 'C_INCLUDE_PATH', 'LIBRARY_PATH',
                'LD_PRELOAD', 'LD_LIBRARY_PATH', 'CXXFLAGS', 'CPPFLAGS', 'LDFLAGS']:
        env.pop(key, None)
    env.update(ASAN_OPTIONS='detect_leaks=1:abort_on_error=1:disable_coredump=1',
               UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1', LC_ALL='C')
    binary = OUT / 'portable-tests'
    command = [compiler, '-std=c++11', '-O1', '-g', '-Wall', '-Wextra', '-Wpedantic',
               '-Werror', '-fsanitize=address,undefined', '-fno-sanitize-recover=all',
               '-fno-omit-frame-pointer', '-include', str(ROOT / 'portable-v1/native_compat.h'),
               str(ROOT / 'candidate/plain_startup.cpp'),
               str(ROOT / 'candidate/private/failure_boundary.cpp'),
               str(ROOT / 'portable-v1/tests.cpp'), '-o', str(binary)]
    (OUT / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
    results = []
    try:
        build = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=120)
        (OUT / 'build.stdout').write_bytes(build.stdout)
        (OUT / 'build.stderr').write_bytes(build.stderr)
        if build.returncode or build.stdout or build.stderr:
            raise RuntimeError('build failed or produced diagnostics')
        normal = subprocess.run([str(binary), 'normal'], cwd=ROOT, env=env, capture_output=True, timeout=30)
        (OUT / 'normal.stdout').write_bytes(normal.stdout)
        (OUT / 'normal.stderr').write_bytes(normal.stderr)
        lines = normal.stdout.decode('ascii').splitlines()
        if normal.returncode or normal.stderr or lines[:-1] != ['SCENARIO:' + x for x in SCENARIOS]:
            raise RuntimeError('normal scenario failure')
        match = re.fullmatch(r'PASS:scenarios=7:checks=([1-9][0-9]*)', lines[-1])
        if not match:
            raise RuntimeError('missing normal completion count')
        results.append({'mode': 'normal', 'scenarios': 7, 'checks': int(match.group(1)), 'returncode': 0})
        negatives = [('missing-reporter', None), ('null-bind', None), ('duplicate-bind', 1),
                     ('null-redist', 2), ('null-version', 2), ('zero-version', 2), ('negative-version', 2)]
        for kind in [1, 2]:
            for reporter in [0, 1, 2]:
                for op in OPS:
                    negatives.append((f'{kind}:{reporter}:{op}', 3 if kind == 1 else 4))
        for index, (mode, reason) in enumerate(negatives):
            child = subprocess.run([str(binary), mode], cwd=ROOT, env=env, capture_output=True, timeout=5)
            stem = OUT / f'negative-{index:02d}'
            stem.with_suffix('.stdout').write_bytes(child.stdout)
            stem.with_suffix('.stderr').write_bytes(child.stderr)
            expected = ['CHILD_STARTED']
            if ':' in mode:
                op = mode.split(':')[2]
                expected.append('NATIVE_THROW:' + op)
            if reason is not None:
                expected.append('REPORT:' + str(reason))
            if ':' in mode and op in ['shutdown', 'set_redist_directory']:
                expected.append('RETAINED_AT_REPORT')
            record = {'mode': mode, 'returncode': child.returncode, 'expected_lines': expected}
            results.append(record)
            (OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
            if child.returncode != -signal.SIGABRT or child.stderr or child.stdout.decode('ascii').splitlines() != expected:
                raise RuntimeError('negative child did not meet exact signal/marker contract: ' + mode)
    finally:
        after = frozen_inputs()
        (OUT / 'inputs-after.json').write_text(json.dumps(after, indent=2) + '\n')
        if after != before:
            raise RuntimeError('inputs changed during gate')
    (OUT / 'completion.json').write_text(json.dumps({'status': 'PASS', 'normal_scenarios': 7,
               'negative_scenarios': len(negatives), 'normal_assertions': int(match.group(1))}, indent=2) + '\n')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        if CREATED_EVIDENCE:
            # Preserve partial evidence. Never invoke another attempt automatically.
            with (OUT / 'failure.txt').open('a') as stream:
                stream.write(str(error) + '\n')
        print('GATE FAILED: ' + str(error), file=sys.stderr)
        sys.exit(1)
