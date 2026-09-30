"""Build the checkout's real ByteOrder.cpp with VS2013. No header substitutes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path,
                        help='new directory for commands, objects and raw logs')
    parser.add_argument('--vcvars', type=Path, default=Path(os.environ.get(
        'VS120COMNTOOLS', 'C:/Program Files (x86)/Microsoft Visual Studio 12.0/Common7/Tools'
    )) / '../../VC/vcvarsall.bat')
    args = parser.parse_args()
    if os.name != 'nt':
        parser.error('run natively on Windows with VS2013 installed')
    vcvars = args.vcvars.resolve(strict=True)
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    checkout = Path(__file__).resolve().parents[2]
    library = checkout / 'src/engine/shared/library/sharedFoundation'
    source = library / 'src/win32/ByteOrder.cpp'
    probe = Path(__file__).with_name('probe.cpp').resolve()
    rows = []
    for config in ('Debug', 'Release'):
        for arch, machine in (('x86', 0x14c), ('amd64', 0x8664)):
            directory = output / (config + '-' + arch)
            directory.mkdir()
            flags = ['/nologo', '/EHsc', '/Y-', '/Gy', '/Zc:wchar_t-', '/DWIN32',
                     '/D_WIN32', '/showIncludes', '/I"' + str(library / 'include/public') + '"']
            flags += ['/MTd', '/Od', '/D_DEBUG'] if config == 'Debug' else ['/MT', '/O2', '/DNDEBUG']
            commands = ['@echo off', 'call "' + str(vcvars) + '" ' + arch,
                        'if errorlevel 1 exit /b 1', 'where cl']
            for name, unit in (('production', source), ('probe', probe)):
                response = directory / (name + '.rsp')
                response.write_text(' '.join(flags + ['/c', '"' + str(unit) + '"',
                    '/Fo"' + str(directory / (name + '.obj')) + '"']), encoding='utf-8')
                commands += ['cl @"' + str(response) + '"', 'if errorlevel 1 exit /b 1']
            commands += ['link /nologo /OPT:REF /NODEFAULTLIB:stlport_vc71_static.lib '
                         'production.obj probe.obj /OUT:probe.exe /MAP:probe.map',
                         'exit /b %errorlevel%']
            batch = directory / 'build.cmd'
            batch.write_text('\n'.join(commands) + '\n', encoding='utf-8')
            build = subprocess.run(['cmd', '/d', '/c', str(batch)], cwd=directory,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
            (directory / 'build.log').write_bytes(build.stdout)
            row = dict(configuration=config, arch=arch, build_exit=build.returncode, passed=False)
            if build.returncode == 0:
                binding = (directory / 'probe.map').read_text(errors='replace')
                row['production_symbols_bound'] = all(any('?' + symbol + '@@' in line and
                    'production.obj' in line for line in binding.splitlines())
                    for symbol in ('htonl', 'ntohl', 'htons', 'ntohs'))
                row['object_machine'] = struct.unpack('<H', (directory / 'production.obj').read_bytes()[:2])[0]
                run = subprocess.run([str(directory / 'probe.exe')], stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, timeout=30)
                (directory / 'run.log').write_bytes(run.stdout)
                row.update(run_exit=run.returncode, output=run.stdout.decode(errors='replace'))
                row['passed'] = (run.returncode == 0 and row['production_symbols_bound'] and
                    row['object_machine'] == machine and
                    run.stdout.strip() == b'PASS 166631 input cases (both directions)')
            rows.append(row)
            print(json.dumps(row), flush=True)
            (output / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    files = [source, probe, Path(__file__).resolve()]
    files += list((checkout / 'src/engine/shared/library').rglob('*.h'))
    (output / 'input-sha256.json').write_text(json.dumps({str(p.relative_to(checkout)):
        hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}, indent=2) + '\n')
    return 0 if len(rows) == 4 and all(row['passed'] for row in rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())
