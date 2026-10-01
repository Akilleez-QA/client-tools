"""Build the actual ByteOrder TU using MSVC 2013 or newer, real headers and a byte oracle."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import struct
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assembly_failure(output, source):
    """Accept only diagnostics from the pinned original assembly body."""
    allowed = {16: {'C2485'}, 18: {'C4235'},
               20: {'C2065', 'C2146', 'C2143', 'C3481', 'C2059'},
               28: {'C4235'},
               30: {'C2065', 'C2146', 'C2143', 'C3481', 'C2059', 'C1903'}}
    diagnostics = []
    for line in output.decode(errors='replace').splitlines():
        if not re.search(r'\b(?:fatal\s+)?error\b|not recognized|cannot find', line, re.I):
            continue
        match = re.match(r'^(.*?)\((\d+)(?:,\d+)?\)\s*:\s*(?:fatal )?error (C\d+):', line)
        if not match:
            return False
        path, number, code = match.groups()
        if (os.path.normcase(os.path.abspath(path)) != os.path.normcase(os.path.abspath(source))
                or code not in allowed.get(int(number), set())):
            return False
        diagnostics.append(code)
    return 'C2485' in diagnostics and 'C4235' in diagnostics


def build_case(directory, source, probe, includes, vcvars, arch, config, mode):
    directory.mkdir()
    flags = ['/nologo', '/EHsc', '/Y-', '/Gy', '/Zc:wchar_t-', '/DWIN32', '/showIncludes',
             '/I"' + str(includes) + '"']
    flags += ['/MTd', '/Od', '/D_DEBUG'] if config == 'Debug' else ['/MT', '/O2', '/DNDEBUG']
    commands = ['@echo off', 'call "' + str(vcvars) + '" ' + arch,
                'if errorlevel 1 exit /b 1', 'where cl']
    for name, unit in (('production', source), ('probe', probe)):
        response = directory / (name + '.rsp')
        response.write_text(' '.join(flags + ['/c', '"' + str(unit) + '"',
            '/Fo"' + str(directory / (name + '.obj')) + '"']), encoding='utf-8')
        commands += ['cl @"' + str(response) + '"', 'if errorlevel 1 exit /b 1']
    commands += ['link /nologo /OPT:REF /NODEFAULTLIB:stlport_vc71_static.lib '
                 'production.obj probe.obj /OUT:probe.exe /MAP:probe.map', 'exit /b %errorlevel%']
    batch = directory / 'build.cmd'
    batch.write_text('\n'.join(commands) + '\n', encoding='utf-8')
    environment = dict(os.environ, VSLANG='1033')
    build = subprocess.run(['cmd', '/d', '/c', str(batch)], cwd=directory, env=environment,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    (directory / 'build.log').write_bytes(build.stdout)
    row = dict(configuration=config, arch=arch, mode=mode, build_exit=build.returncode,
               source_sha256=digest(source), passed=False)
    if mode == 'baseline' and arch == 'amd64':
        # An unrelated missing-header/error is NOT a successful negative control.
        row['passed'] = build.returncode != 0 and assembly_failure(build.stdout, source)
    elif build.returncode == 0:
        binding = (directory / 'probe.map').read_text(errors='replace')
        row['production_symbols_bound'] = all(any('?' + symbol + '@@' in line and
            'production.obj' in line for line in binding.splitlines())
            for symbol in ('htonl', 'ntohl', 'htons', 'ntohs'))
        row['object_machine'] = struct.unpack('<H', (directory / 'production.obj').read_bytes()[:2])[0]
        run = subprocess.run([str(directory / 'probe.exe')], stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, timeout=30)
        (directory / 'run.log').write_bytes(run.stdout)
        row.update(run_exit=run.returncode, output=run.stdout.decode(errors='replace'))
        oracle = (run.returncode == 1 and b'FAIL long' in run.stdout) if mode == 'mutant' else (
            run.returncode == 0 and run.stdout.strip() == b'PASS 166631 input cases (both directions)')
        row['passed'] = (oracle and row['production_symbols_bound'] and
                        row['object_machine'] == (0x14c if arch == 'x86' else 0x8664))
    return row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path, help='new output directory')
    parser.add_argument('--baseline', type=Path, help='original ByteOrder.cpp for baseline/negative controls')
    parser.add_argument('--vcvars', type=Path, default=Path(os.environ.get(
        'VS120COMNTOOLS', 'C:/Program Files (x86)/Microsoft Visual Studio 12.0/Common7/Tools'
    )) / '../../VC/vcvarsall.bat')
    args = parser.parse_args()
    if os.name != 'nt':
        parser.error('run natively on Windows with MSVC 2013 or newer installed')
    vcvars = args.vcvars.resolve(strict=True)
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    checkout = Path(__file__).resolve().parents[2]
    library = checkout / 'src/engine/shared/library/sharedFoundation'
    source = library / 'src/win32/ByteOrder.cpp'
    probe = Path(__file__).with_name('probe.cpp').resolve()
    inputs = [source, probe, Path(__file__).resolve()]
    inputs += list((checkout / 'src/engine/shared/library').rglob('*.h'))
    before = {str(p.relative_to(checkout)): digest(p) for p in sorted(set(inputs))}
    (output / 'input-sha256.json').write_text(json.dumps(before, indent=2) + '\n')
    baseline = args.baseline.resolve(strict=True) if args.baseline else None
    if baseline:
        # Freeze explicit baseline input; use this checkout's same headers for all modes.
        frozen = output / 'baseline.cpp'
        frozen.write_bytes(baseline.read_bytes())
        baseline = frozen
        needle = 'return _byteswap_ulong(hostLong);'
        original = source.read_text()
        if original.count(needle) != 1:
            parser.error('mutation target must occur exactly once')
        mutant = output / 'mutant.cpp'
        mutant.write_text(original.replace(needle, 'return hostLong;'))
    rows = []
    for config in ('Debug', 'Release'):
        for arch in ('x86', 'amd64'):
            modes = [('candidate', source)]
            if baseline:
                modes.append(('baseline', baseline))
                if arch == 'amd64':
                    modes.append(('mutant', mutant))
            for mode, unit in modes:
                row = build_case(output / (config + '-' + arch + '-' + mode), unit, probe,
                                 library / 'include/public', vcvars, arch, config, mode)
                rows.append(row)
                print(json.dumps(row), flush=True)
                (output / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    unchanged = all(digest(checkout / name) == value for name, value in before.items())
    summary = dict(expected_cases=10 if baseline else 4, observed_cases=len(rows),
                   inputs_unchanged=unchanged, controls_run=bool(baseline))
    summary['passed'] = unchanged and len(rows) == summary['expected_cases'] and all(r['passed'] for r in rows)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return 0 if summary['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
