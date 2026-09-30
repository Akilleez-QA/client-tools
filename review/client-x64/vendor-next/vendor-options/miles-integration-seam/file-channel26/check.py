"""Portable scripted checks only; no VM, vendor, engine or real file callbacks."""
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


def snapshot(paths):
    return {str(path): digest(path) for path in paths}


def run(name, command):
    (evidence / (name + '-command.json')).write_text(json.dumps(command, indent=2) + '\n')
    with (evidence / (name + '.log')).open('wb') as output:
        result = subprocess.run(command, cwd=build, stdout=output,
                                stderr=subprocess.STDOUT, timeout=60)
    return result.returncode


inputs = [base / name for name in ['file_channel.h', 'file_channel.cpp',
          'canonical_services.cpp', 'channel_test.cpp', 'check.py', 'PLAN.md', 'CONTRACT.md']]
inputs += [root / name for name in ['reverse-file-seam20/ClientAudioFileCallbacks.h',
           'transport-candidate/codec.h', 'transport-candidate/codec.cpp',
           'transport-candidate/resource_registry.h', 'protocol-candidate/miles_wire.h',
           'coordinator-candidate/coordinator.h', 'coordinator-candidate/coordinator.cpp']]
compiler = Path(shutil.which('g++')).resolve()
inputs.append(compiler)
before = snapshot(inputs)
record = {'scope': __doc__, 'inputs_before': before, 'compiler': str(compiler)}
try:
    flags = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror',
             '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
    executable = build / 'file-values-test'
    record['build_exit'] = run('build', flags + [str(base / 'channel_test.cpp'),
        str(base / 'file_channel.cpp'), str(root / 'transport-candidate/codec.cpp'),
        str(root / 'coordinator-candidate/coordinator.cpp'), '-o', str(executable)])
    if record['build_exit']:
        raise RuntimeError('portable build failed; preserve first failure')
    record['executable_sha256'] = digest(executable)
    record['run_exit'] = run('run', [str(executable)])
    if record['run_exit']:
        raise RuntimeError('scripted tests failed; preserve first failure')
    canonical = build / 'canonical-services.o'
    record['canonical_compile_exit'] = run('canonical-compile', flags + ['-c',
        str(base / 'canonical_services.cpp'), '-o', str(canonical)])
    if record['canonical_compile_exit']:
        raise RuntimeError('canonical adapter object failed')
    record['canonical_object_sha256'] = digest(canonical)
    nm = shutil.which('nm')
    record['symbols_exit'] = run('canonical-symbols', [nm, '-C', '-u', str(canonical)])
    symbols = (evidence / 'canonical-symbols.log').read_text()
    for name in ['open', 'close', 'seek', 'read']:
        if 'ClientAudioFileCallbacks::' + name + '(' not in symbols:
            raise RuntimeError('missing real unresolved seam symbol: ' + name)
    if record['symbols_exit']:
        raise RuntimeError('symbol inspection failed')
    record['canonical_linked_or_executed'] = False
except Exception as error:
    record['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    record['inputs_after'] = snapshot(inputs)
    record['inputs_unchanged'] = before == record['inputs_after']
    path = evidence / 'results.json'
    path.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'result': str(path), 'sha256': digest(path),
                      'failure': record.get('failure'),
                      'inputs_unchanged': record['inputs_unchanged']}, indent=2))
sys.exit(1 if record.get('failure') or not record['inputs_unchanged'] else 0)
