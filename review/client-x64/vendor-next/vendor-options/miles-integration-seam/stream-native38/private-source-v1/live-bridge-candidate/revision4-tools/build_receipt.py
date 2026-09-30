"""Compile-only v120 matrix with input and immediate output receipts; never runs a PE."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from receipt import digest, machine

DIRECTORIES = ['live-bridge-candidate', 'host-candidate', 'transport-candidate',
               'pipe-transport-candidate', 'protocol-candidate', 'coordinator-candidate',
               'buffer-upload-candidate']
LIB_NAMES = ['libcmt', 'libcmtd', 'libcpmt', 'libcpmtd', 'msvcrt', 'msvcrtd',
             'msvcprt', 'msvcprtd', 'oldnames', 'kernel32', 'advapi32', 'user32',
             'gdi32', 'shell32', 'ole32', 'oleaut32', 'uuid', 'ws2_32', 'winmm']

def exclusive_json(path, data):
    with Path(path).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(data, stream, indent=2, sort_keys=True)
        stream.write('\n')

def environment(vcvars, architecture, output):
    command = output / 'environment.cmd'
    command.write_text('@echo off\nset VSLANG=1033\ncall "' + str(vcvars) + '" ' + architecture + ' >nul\nif errorlevel 1 exit /b 1\nset\n')
    process = subprocess.run(['cmd', '/d', '/c', str(command)], capture_output=True, check=True)
    values = {}
    for line in process.stdout.decode('mbcs', errors='replace').splitlines():
        if '=' in line and not line.startswith('='):
            key, value = line.split('=', 1)
            values[key.upper()] = value
    return values

def identities(paths):
    return {str(Path(p).resolve()): digest(p) for p in sorted(set(paths), key=lambda x: str(x).lower())}

def includes(log):
    result = set()
    for line in log.splitlines():
        match = re.match(r'\s*Note: including file:\s*(.+?)\s*$', line)
        if match:
            path = Path(match.group(1)).resolve()
            if not path.is_file():
                raise RuntimeError('discovered header missing: ' + str(path))
            result.add(path)
    return result

def run(command, output, name, env):
    exclusive_json(output / (name + '-command.json'), {'argv': command, 'cwd': str(output),
        'environment': {k: env.get(k, '') for k in ['PATH', 'INCLUDE', 'LIB', 'VSLANG']}})
    process = subprocess.run(command, cwd=output, env=env, capture_output=True, timeout=180)
    raw = process.stdout + process.stderr
    (output / (name + '.log')).write_bytes(raw)
    return process.returncode, raw.decode('mbcs', errors='replace')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--vcvars', type=Path, default=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat'))
    parser.add_argument('--miles', type=Path, default=Path('C:/client-next-build/src/external/3rd/library/miles'))
    args = parser.parse_args()
    source = args.source.resolve();output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source_files = [p for directory in DIRECTORIES for p in (source/directory).glob('*') if p.suffix in ('.h', '.cpp')]
    initial_sources = identities(source_files)
    builder_files = identities(Path(__file__).parent.glob('*.py'))
    receipt = {'schema': 'miles-build-receipt-v4', 'builds': [],
               'builder_before': builder_files, 'source_snapshot_before': initial_sources,
               'system': platform.platform(), 'python': sys.version, 'python_sha256': digest(sys.executable),
               'scope': 'compile only; private vendor import library and headers hashed, not published'}
    common = ['transport-candidate/codec.cpp', 'pipe-transport-candidate/endpoint.cpp', 'coordinator-candidate/coordinator.cpp']
    for config in ['Debug', 'Release']:
        for architecture in ['x86', 'amd64']:
            target = output / (architecture + '-' + config);target.mkdir()
            env = environment(args.vcvars, architecture, target)
            compiler = Path(shutil.which('cl.exe', path=env['PATH']))
            linker = Path(shutil.which('link.exe', path=env['PATH']))
            tool_files = {compiler, linker, args.vcvars.resolve()}
            tool_files.update(compiler.parent.glob('*.dll'))
            tool_files.update(compiler.parent.glob('1033/*.dll'))
            tool_files.update((args.vcvars.parent/'bin').glob('*.dll'))
            tool_files.update((args.vcvars.parent.parent/'Common7/IDE').glob('mspdb*.dll'))
            libraries = set()
            for directory in env['LIB'].split(';'):
                for name in LIB_NAMES:
                    path = Path(directory)/(name+'.lib')
                    if path.is_file():libraries.add(path.resolve())
            sources = ['live-bridge-candidate/bridge.cpp'] + common
            if architecture == 'x86':
                sources += ['host-candidate/host_dispatch.cpp', 'host-candidate/retained_buffers.cpp', 'buffer-upload-candidate/buffer_upload.cpp']
                libraries.add((args.miles/'lib/win/Mss32.lib').resolve())
            argv = [str(compiler), '/nologo', '/EHsc', '/W4', '/WX', '/DWIN32', '/D_WIN32_WINNT=0x0601',
                    '/I'+str(args.miles/'include'), '/MTd' if config=='Debug' else '/MT', '/Od' if config=='Debug' else '/O2']
            argv += [str(source/p) for p in sources]
            discovery_exit, discovery_log = run(argv+['/showIncludes','/Zs'], target, 'headers', env)
            record = {'config': config, 'architecture': architecture, 'discovery_exit': discovery_exit}
            if discovery_exit:
                record.update(exit_code=discovery_exit, inputs_unchanged=False, failure='header discovery failed');receipt['builds'].append(record);continue
            headers = includes(discovery_log)
            if not headers:raise RuntimeError('no header identities discovered')
            before = {'sources': identities(source_files), 'headers': identities(headers),
                      'tools': identities(tool_files), 'libraries': identities(libraries)}
            exclusive_json(target/'inputs-before.json', before)
            exe = target/('host.exe' if architecture=='x86' else 'controller.exe')
            compile_command = argv + ['/showIncludes', '/Fe'+str(exe)]
            if architecture=='x86':compile_command.append(str(args.miles/'lib/win/Mss32.lib'))
            compile_command += ['/link', '/VERBOSE:LIB']
            code, log = run(compile_command, target, 'compile', env)
            # Capture bytes immediately after the linker returns, before later input scans.
            pe = {'path': str(exe), 'sha256': digest(exe), 'machine': machine(exe)} if code==0 and exe.is_file() else None
            after = {'sources': identities(source_files), 'headers': identities(headers),
                     'tools': identities(tool_files), 'libraries': identities(libraries)}
            observed_headers = includes(log)
            searched = {Path(m.group(1)).resolve() for line in log.splitlines()
                        for m in [re.match(r'\s*Searching (.+\.lib):\s*$', line)] if m and Path(m.group(1)).is_file()}
            unrecorded_libraries = sorted(str(p) for p in searched-libraries)
            unchanged = before==after and before['sources']==initial_sources and headers==observed_headers and not unrecorded_libraries
            record.update(exit_code=code, command=compile_command, before=before, after=after,
                inputs_unchanged=unchanged, output=pe, headers_match=observed_headers==headers,
                unrecorded_libraries=unrecorded_libraries, observed_link_library_paths=sorted(str(p) for p in searched))
            receipt['builds'].append(record)
    receipt['builder_after'] = identities(Path(__file__).parent.glob('*.py'))
    receipt['source_snapshot_after'] = identities(source_files)
    receipt['stable_matrix'] = receipt['builder_before']==receipt['builder_after'] and receipt['source_snapshot_before']==receipt['source_snapshot_after']
    path = output/'receipt.json';exclusive_json(path, receipt)
    pin = digest(path);(output/'receipt.sha256').write_text(pin+'\n', encoding='ascii')
    os.chmod(path, 0o444)
    print(json.dumps({'receipt': str(path), 'sha256': pin, 'stable_matrix': receipt['stable_matrix'],
                     'builds': [{k:r.get(k) for k in ['config','architecture','exit_code','inputs_unchanged','unrecorded_libraries']} for r in receipt['builds']]}, indent=2))
    return 0 if receipt['stable_matrix'] and all(r['exit_code']==0 and r['inputs_unchanged'] and r.get('output') for r in receipt['builds']) else 1

if __name__ == '__main__':
    raise SystemExit(main())
