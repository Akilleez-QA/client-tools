"""One portable baseline and explicit old-null mutation; no engine/vendor calls."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

base = Path(__file__).resolve().parent
root = base.parent
evidence = base / 'evidence-v1'
build = base / 'private-build-v1'
evidence.mkdir(exist_ok=False)
build.mkdir(mode=0o700, exist_ok=False)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(name, command):
    (evidence / (name + '-command.json')).write_text(json.dumps(command, indent=2) + '\n')
    with (evidence / (name + '.log')).open('wb') as output:
        return subprocess.run(command, cwd=build, stdout=output,
                              stderr=subprocess.STDOUT, timeout=60).returncode


compiler = Path(shutil.which('g++')).resolve()
source = root / 'file-channel26/file_channel.cpp'
inputs = [base / 'zero_buffer.cpp', base / 'check.py', base / 'PLAN.md', compiler,
          source, root / 'file-channel26/file_channel.h',
          root / 'reverse-file-seam20/ClientAudioFileCallbacks.h',
          root / 'protocol-candidate/miles_wire.h', root / 'transport-candidate/codec.h',
          root / 'transport-candidate/codec.cpp', root / 'transport-candidate/resource_registry.h']
before = {str(p): digest(p) for p in inputs}
record = {'scope': __doc__, 'inputs_before': before, 'cases': []}
try:
    if digest(source) != '0c5253d7f2a3a7b06ba54af756f170eca6c5f3b84fbbdce952a5700de6a64e27':
        raise RuntimeError('frozen source identity mismatch')
    original = source.read_text()
    selected = 'result.bytes.resize(operation.count() ? operation.count() : 1);'
    if original.count(selected) != 1:
        raise RuntimeError('mutation site changed')
    mutant = build / 'old-null.cpp'
    mutant.write_text(original.replace(selected, 'result.bytes.resize(operation.count());'))
    record['mutation_sha256'] = digest(mutant)
    record['mutation'] = {'from': selected, 'to': 'result.bytes.resize(operation.count());'}
    for name, implementation, expected in [('frozen', source, 0), ('old-null', mutant, 1)]:
        executable = build / name
        command = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror',
                   '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer',
                   '-I' + str(root / 'file-channel26'), str(base / 'zero_buffer.cpp'),
                   str(implementation), str(root / 'transport-candidate/codec.cpp'),
                   '-o', str(executable)]
        case = {'name': name, 'expected_exit': expected,
                'build_exit': run(name + '-build', command)}
        record['cases'].append(case)
        if case['build_exit']:
            raise RuntimeError(name + ' build failed')
        case['executable_sha256'] = digest(executable)
        case['run_exit'] = run(name + '-run', [str(executable)])
        log = (evidence / (name + '-run.log')).read_text()
        marker = ('PASS zero-count read invoked once with nonnull storage and no returned bytes'
                  if expected == 0 else 'FAIL zero-count read callback received null destination')
        case['expected_marker_observed'] = marker in log
        if case['run_exit'] != expected or not case['expected_marker_observed']:
            raise RuntimeError(name + ' contradicted prospective result')
except Exception as error:
    record['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    record['inputs_after'] = {str(p): digest(p) for p in inputs}
    record['inputs_unchanged'] = before == record['inputs_after']
    path = evidence / 'results.json'
    path.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'path': str(path), 'sha256': digest(path),
                      'failure': record.get('failure'), 'cases': record['cases']}, indent=2))
sys.exit(1 if record.get('failure') or not record['inputs_unchanged'] else 0)
