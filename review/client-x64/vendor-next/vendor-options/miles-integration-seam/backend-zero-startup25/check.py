"""Pure test-only observation of frozen facade startup0 behavior. No vendor execution."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

base = Path(__file__).resolve().parent
root = base.parent
out = base / 'evidence-v1'
out.mkdir(exist_ok=False)
private = base / 'private-build-v1'
private.mkdir(mode=0o700, exist_ok=False)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


sources = [base / 'zero_startup.cpp', root / 'backend-boundary24/pipe/ClientMilesPipe.cpp',
           root / 'transport-candidate/codec.cpp', root / 'session-version22/session_version.cpp',
           root / 'startup-metadata-v4/metadata_wire.cpp']
inputs = sources + [base / 'check.py', root / 'backend-boundary24/ClientMiles.h',
                   root / 'backend-boundary24/pipe/Session.h', root / 'backend-boundary24/pipe/Channel.h',
                   root / 'startup-bridge23/reply.h', root / 'startup-metadata-v4/metadata.h',
                   root / 'host-candidate/host_dispatch.h', root / 'transport-candidate/codec.h',
                   root / 'transport-candidate/resource_registry.h', root / 'protocol-candidate/miles_wire.h',
                   root / 'session-version22/session_version.h']
compiler = Path(shutil.which('g++')).resolve()
before = {str(p): digest(p) for p in sorted(inputs)}
result = {'inputs_before': before, 'compiler': str(compiler), 'compiler_sha256': digest(compiler),
          'scope': 'test-only known zero reply; no vendor, Wine or native executable'}
command = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror',
           '-fsanitize=address,undefined', '-g'] + [str(p) for p in sources]
command += ['-o', str(private / 'zero-startup')]
(out / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
try:
    build = subprocess.run(command, text=True, capture_output=True, timeout=60)
    (out / 'build.log').write_text(build.stdout + build.stderr)
    result['build_exit'] = build.returncode
    if build.returncode:
        raise RuntimeError('pure zero-startup compile failed')
    result['test_executable_sha256'] = digest(private / 'zero-startup')
    process = subprocess.run([str(private / 'zero-startup')], text=True, capture_output=True, timeout=10)
    (out / 'run.log').write_text(process.stdout + process.stderr)
    result['run_exit'] = process.returncode
    if process.returncode:
        raise RuntimeError('pure zero-startup prediction failed')
    result['observation'] = json.loads(process.stdout)
except Exception as error:
    result['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    result['inputs_after'] = {str(p): digest(p) for p in sorted(inputs)}
    result['inputs_unchanged'] = result['inputs_after'] == before
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('inputs_before', 'inputs_after')}, indent=2))
raise SystemExit(bool(result.get('failure')) or not result['inputs_unchanged'])
