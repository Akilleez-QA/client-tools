"""Source/adapter checks only. Never invokes a vendor, Wine, or native executable."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

base = Path(__file__).resolve().parent
root = base.parent
out = base / 'private-portable-v1'
out.mkdir(exist_ok=False)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(args, name, cwd=out):
    process = subprocess.run(args, cwd=cwd, text=True, capture_output=True, timeout=60)
    (out / (name + '.log')).write_text(process.stdout + process.stderr)
    (out / (name + '-command.json')).write_text(json.dumps(args, indent=2) + '\n')
    return process


def require(value, message):
    if not value:
        raise RuntimeError(message)


compiler = Path(shutil.which('g++')).resolve()
inputs = [p for p in base.rglob('*') if p.is_file() and p.suffix in ('.h', '.cpp', '.py')
          and not any(part.startswith('private-') for part in p.relative_to(base).parts)]
inputs += [root / name for name in [
    'startup-bridge23/reply.h', 'startup-metadata-v4/metadata.h',
    'startup-metadata-v4/metadata_wire.cpp', 'host-candidate/host_dispatch.h',
    'session-version22/session_version.h', 'session-version22/session_version.cpp',
    'transport-candidate/codec.h', 'transport-candidate/codec.cpp',
    'transport-candidate/resource_registry.h', 'protocol-candidate/miles_wire.h']]
before = {str(p): digest(p) for p in sorted(inputs)}
result = {'compiler': str(compiler), 'compiler_sha256': digest(compiler),
          'inputs_before': before, 'vendor_execution': False, 'native_execution': False}
try:
    sources = [base / 'tests/adapter_test.cpp', base / 'pipe/ClientMilesPipe.cpp',
               base / 'sample/startup_calls.cpp', root / 'transport-candidate/codec.cpp',
               root / 'session-version22/session_version.cpp',
               root / 'startup-metadata-v4/metadata_wire.cpp']
    args = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror',
            '-fsanitize=address,undefined', '-g']
    args += [str(p) for p in sources] + ['-o', str(out / 'adapter-test')]
    build = run(args, 'adapter-build')
    result['adapter_build_exit'] = build.returncode
    require(build.returncode == 0, 'portable adapter compilation failed')
    test = run([str(out / 'adapter-test')], 'adapter-run')
    result['adapter_run_exit'] = test.returncode
    result['adapter_stdout'] = test.stdout
    require(test.returncode == 0, 'portable adapter checks failed')

    # A physical copy with no pipe/protocol/native source and no repository -I.
    isolated = out / 'deleted-pipe-tree'
    allowed = ['ClientMiles.h', 'sample/startup_calls.h', 'sample/startup_calls.cpp',
               'tests/link_double.cpp', 'tests/link_main.cpp']
    for relative in allowed:
        destination = isolated / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(base / relative, destination)
    require(sorted(str(p.relative_to(isolated)) for p in isolated.rglob('*') if p.is_file())
            == sorted(allowed), 'isolation tree contains extra source')
    result['isolated_inputs'] = {name: digest(isolated / name) for name in allowed}
    objects = []
    dependencies = []
    for name in ['sample/startup_calls.cpp', 'tests/link_main.cpp', 'tests/link_double.cpp']:
        stem = Path(name).stem
        command = [str(compiler), '-std=c++11', '-Wall', '-Wextra', '-Werror',
                   '-DCLIENT_MILES_TEST_DOUBLE', '-MMD', '-MF', stem + '.d',
                   '-c', name, '-o', stem + '.o']
        build = run(command, 'isolation-' + stem, isolated)
        require(build.returncode == 0, 'isolated game-facing source compile failed')
        objects.append(stem + '.o')
        raw = (isolated / (stem + '.d')).read_text().replace('\\\n', ' ')
        deps = raw.split(':', 1)[1].split()
        for dependency in deps:
            resolved = (isolated / dependency).resolve()
            require(resolved.is_relative_to(isolated), 'dependency escaped isolated tree')
            require(str(resolved.relative_to(isolated)) in allowed, 'unlisted source dependency')
        dependencies.extend(deps)
    linked = run([str(compiler)] + objects + ['-o', 'link-only-test'], 'isolation-link', isolated)
    require(linked.returncode == 0, 'isolated test-only link failed')
    negative = run([str(compiler)] + objects[:2] + ['-o', 'must-not-link'], 'isolation-no-implementation', isolated)
    require(negative.returncode != 0 and 'ClientMiles::' in negative.stderr,
            'missing implementation unexpectedly linked or failed for another reason')
    result.update(isolation_link_exit=linked.returncode,
                  missing_implementation_link_exit=negative.returncode,
                  isolated_dependencies=sorted(set(dependencies)),
                  isolated_executable_run=False)
except Exception as error:
    result['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    result['inputs_after'] = {str(p): digest(p) for p in sorted(inputs)}
    result['inputs_unchanged'] = result['inputs_before'] == result['inputs_after']
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ('inputs_before', 'inputs_after', 'isolated_inputs')}, indent=2))
raise SystemExit(bool(result.get('failure')) or not result['inputs_unchanged'])
