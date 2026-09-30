#!/usr/bin/env python3
"""Bounded native v120 network checks; no PCH, header stubs, or library providers."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

NETWORK = 'src/engine/shared/library/sharedNetwork'
HEADERS = [NETWORK + '/src/win32/Sock.h',
           'src/external/3rd/library/udplibrary/UdpLibrary.hpp',
           'src/external/3rd/library/soePlatform/VChatAPI/utils2.0/utils/UdpLibrary/UdpLibrary.hpp']
TUS = [NETWORK + '/src/win32/' + name + '.cpp' for name in ('Sock', 'TcpClient', 'TcpServer')]
PROJECT = NETWORK + '/build/win32/sharedNetwork.vcxproj'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def project_inputs(root, config, arch):
    project = root / PROJECT
    ns = {'m': 'http://schemas.microsoft.com/developer/msbuild/2003'}
    groups = ET.parse(str(project)).getroot().findall('m:ItemDefinitionGroup', ns)
    group, = [g for g in groups if g.get('Condition') == "'$(Configuration)|$(Platform)'=='%s|Win32'" % config]
    cl = group.find('m:ClCompile', ns)
    dirs = cl.find('m:AdditionalIncludeDirectories', ns).text.split(';')
    includes = [(project.parent / p.replace('\\', '/')).resolve() for p in dirs if not p.startswith('%(')]
    # Preserve even stale project include entries: cl ignores an absent search
    # directory, and still diagnoses any genuinely missing required header.
    definitions = cl.find('m:PreprocessorDefinitions', ns).text.split(';')
    definitions = [d for d in definitions if not d.startswith('%(')]
    # The project supplies Win32 only. This is an explicit source-level x64
    # compile adaptation, not a new project configuration or full-library build.
    if arch == 'amd64':
        definitions.remove('_USE_32BIT_TIME_T=1')
    options = ['/MTd', '/Od', '/RTC1'] if config == 'Debug' else ['/MT', '/O2']
    return includes, definitions, options


def replace_once(data, old, new):
    if data.count(old) != 1:
        raise ValueError('Control mutation must bind exactly once: ' + repr(old))
    return data.replace(old, new)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path, help='Must not exist')
    parser.add_argument('--vcvars', type=Path, default=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat'))
    parser.add_argument('--only', choices=('all', 'implementation', 'headers'), default='all')
    parser.add_argument('--revision', default='unreported', help='Reported source revision; hashes below bind actual inputs')
    args = parser.parse_args()
    if os.name != 'nt':
        parser.error('Run on native Windows with Visual Studio 2013 v120 installed')
    root, out, vcvars = args.checkout.resolve(), args.out.resolve(), args.vcvars.resolve()
    out.mkdir(parents=True, exist_ok=False)
    results, source_hashes, included_hashes = [], {}, {}
    runner, probe = Path(__file__).resolve(), Path(__file__).resolve().with_name('probe.cpp')
    for path in HEADERS + TUS + [PROJECT]:
        source_hashes[path] = sha(root / path)
    write_json(out / 'identity.json', {'reported_revision': args.revision,
               'checkout': str(root), 'python': sys.version, 'vcvars': str(vcvars),
               'vcvars_sha256': sha(vcvars), 'runner_sha256': sha(runner),
               'probe_sha256': sha(probe), 'sources': source_hashes})

    def compile_case(name, arch, config, source, includes, definitions, options,
                     executable=False, expected_diagnostic=None, positive_name=None, probe_values=None):
        directory = out / name
        directory.mkdir()
        obj, exe = directory / 'case.obj', directory / 'case.exe'
        arguments = ['cl', '/nologo', '/EHsc', '/W4', '/Zc:wchar_t-', '/GR', '/Gy', '/showIncludes'] + options
        arguments += ['/D' + d for d in definitions] + ['/I' + str(p) for p in includes]
        arguments += [str(source), '/Fo' + str(obj)]
        arguments += ['/Fe' + str(exe), '/link', 'Ws2_32.lib'] if executable else ['/c']
        command = subprocess.list2cmdline(arguments)
        batch = directory / 'compile.cmd'
        batch.write_text('@echo off\ncall "' + str(vcvars) + '" ' + arch + ' >nul\nif errorlevel 1 exit /b %errorlevel%\n' + command + '\nexit /b %errorlevel%\n')
        record = {'name': name, 'arch': arch, 'configuration': config, 'source': str(source),
                  'source_sha256': sha(source), 'command': command,
                  'expected': expected_diagnostic or 'compile success', 'positive_case': positive_name}
        try:
            run = subprocess.run(['cmd', '/d', '/c', str(batch)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            raw = run.stdout
            record['compile_exit'] = run.returncode
            text = raw.decode('utf-8', errors='replace')
            (directory / 'compile.log').write_bytes(raw)
            for line in text.splitlines():
                if 'Note: including file:' in line:
                    path = Path(line.split('Note: including file:', 1)[1].strip()).resolve()
                    if path.is_file():
                        try:
                            key = 'checkout/' + path.relative_to(root).as_posix()
                        except ValueError:
                            key = str(path)
                        included_hashes[key] = sha(path)
            if expected_diagnostic:
                record['passed'] = (run.returncode != 0 and re.search(expected_diagnostic, text) is not None
                                    and any(r['name'] == positive_name and r['passed'] for r in results))
            else:
                record['passed'] = run.returncode == 0 and obj.is_file()
                if record['passed']:
                    record['object_machine'] = hex(struct.unpack('<H', obj.read_bytes()[:2])[0])
                    record['passed'] &= record['object_machine'] == ('0x8664' if arch == 'amd64' else '0x14c')
                if executable and record['passed']:
                    runtime = subprocess.run([str(exe)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=15)
                    (directory / 'run.log').write_bytes(runtime.stdout)
                    record['run_exit'] = runtime.returncode
                    record['run_sha256'] = hashlib.sha256(runtime.stdout).hexdigest()
                    sock, udp, order = probe_values
                    expected = 'SUMMARY PASS checks=21 pointer_bytes=%d udp_header=%d winsock_first=%d' % (8 if arch == 'amd64' else 4, udp, order)
                    lines = runtime.stdout.decode('utf-8', errors='replace').splitlines()
                    record['runtime_checks'] = sum(line.startswith('PASS ') for line in lines)
                    record['passed'] &= runtime.returncode == 0 and lines.count(expected) == 1 and record['runtime_checks'] == 21
        except subprocess.TimeoutExpired as error:
            (directory / 'timeout.log').write_bytes(error.stdout or b'')
            record.update(passed=False, error='timeout')
        results.append(record)
        write_json(out / 'results.json', results)
        print(('%s ' % ('PASS' if record['passed'] else 'FAIL')) + name, flush=True)

    # Capture compiler/SDK paths and versions separately for both architectures.
    for arch in ('x86', 'amd64'):
        metadata = out / ('toolchain-' + arch + '.cmd')
        metadata.write_text('@echo off\ncall "' + str(vcvars) + '" ' + arch + ' >nul\nif errorlevel 1 exit /b %errorlevel%\nwhere cl\nwhere link\ncl /Bv\nset INCLUDE\nset LIB\nver\n')
        run = subprocess.run(['cmd', '/d', '/c', str(metadata)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30)
        (out / ('toolchain-' + arch + '.log')).write_bytes(run.stdout)

    if args.only in ('all', 'headers'):
        controls = out / 'reverted-headers'
        for path in HEADERS:
            source = (root / path).read_bytes()
            source = replace_once(source, b'typedef uintptr_t SOCKET;', b'typedef unsigned int SOCKET;')
            source, count = re.subn(rb'(?m)^[ \t]*#include <stdint.h>\r?\n', b'', source)
            if count != 1:
                raise ValueError('Expected one added stdint include in ' + path)
            if path.endswith('/Sock.h'):
                source = replace_once(source, b'SOCKET                      handle;', b'int                         handle;')
            target = controls / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source)
        common = [root / 'src', root / (NETWORK + '/include/public'),
                  root / 'src/external/3rd/library/soePlatform/VChatAPI/utils2.0/utils']
        for arch in ('x86', 'amd64'):
            for config in ('Debug', 'Release'):
                for sock, udp in ((1, 0), (0, 1), (0, 2), (1, 1), (1, 2)):
                    for order in (0, 1):
                        suffix = '%s-%s-s%d-u%d-w%d' % (arch, config, sock, udp, order)
                        defines = ['WIN32', 'SOCKET_PROBE_SOCK=%d' % sock, 'SOCKET_PROBE_UDP=%d' % udp,
                                   'SOCKET_PROBE_WINSOCK_FIRST=%d' % order]
                        options = ['/MTd', '/Od', '/D_DEBUG'] if config == 'Debug' else ['/MT', '/O2', '/DNDEBUG']
                        siblings = [root / HEADERS[udp].rsplit('/', 1)[0]] if udp else []
                        compile_case('headers-' + suffix, arch, config, probe, common, defines, options, True,
                                     probe_values=(sock, udp, order))
                        compile_case('reverted-headers-' + suffix, arch, config, probe, [controls / 'src'] + common + siblings,
                                     defines, options, True,
                                     expected_diagnostic=r'error C(?:2371|2338)' if arch == 'amd64' else None,
                                     positive_name='headers-' + suffix, probe_values=(sock, udp, order))

    if args.only in ('all', 'implementation'):
        for arch in ('x86', 'amd64'):
            for config in ('Debug', 'Release'):
                includes, definitions, options = project_inputs(root, config, arch)
                for path in TUS:
                    source = root / path
                    suffix = '%s-%s-%s' % (arch, config, source.stem)
                    compile_case('production-' + suffix, arch, config, source, includes, definitions, options)
                    if source.stem != 'Sock':
                        # Copy the entire production TU and independently revert its key.
                        # The actual Windows API declaration remains responsible for rejection.
                        original = source.read_bytes()
                        if not re.search(rb'GetQueuedCompletionStatus\s*\([^;]*&completionKey', original):
                            raise ValueError('Missing production completion-key API binding: ' + path)
                        reverted = replace_once(original, b'ULONG_PTR completionKey = 0;', b'unsigned long completionKey = 0;')
                        target = out / ('reverted-' + source.name)
                        target.write_bytes(reverted)
                        compile_case('reverted-key-' + suffix, arch, config, target, includes, definitions, options,
                                     expected_diagnostic=r'error C2664:[^\r\n]*GetQueuedCompletionStatus[^\r\n]*PULONG_PTR' if arch == 'amd64' else None,
                                     positive_name='production-' + suffix)

    write_json(out / 'included-files-sha256.json', included_hashes)
    expected = {'all': 100, 'headers': 80, 'implementation': 20}[args.only]
    summary = {'expected_compile_cases': expected, 'observed_compile_cases': len(results),
               'passed_cases': sum(bool(r['passed']) for r in results),
               'runtime_checks': sum(r.get('runtime_checks', 0) for r in results),
               'failed_cases': [r['name'] for r in results if not r['passed']]}
    summary['passed'] = len(results) == expected and not summary['failed_cases']
    summary['source_inputs_unchanged'] = all(sha(root / path) == value for path, value in source_hashes.items())
    summary['passed'] &= summary['source_inputs_unchanged']
    write_json(out / 'summary.json', summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
