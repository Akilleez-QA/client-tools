"""Native VS2013 actual MemoryManager.cpp compile-only acceptance.

Example (Windows): python run-memory-compile.py --source C:/client-next-build
 --audit C:/native-audit --output C:/memory-next --negative-header

Consumes saved effective definitions/includes, verifies v120, matches the project's
Debug/Release CRT and compiler settings. Explicit changes: /EHsc, /Y-, isolated
outputs, /Gm- (no incremental database), /showIncludes. Does not link or run an allocator.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import xml.etree.ElementTree as ET


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quoted(value):
    value = str(value)
    if any(c in value for c in '\r\n"%&|<>^!'):
        raise ValueError('Unsafe command/response path: ' + value)
    return '"' + value + '"'


def audit_metadata(path, config, platform):
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    globals_ = [line.strip().split('|') for line in lines if line.strip().startswith('GLOBAL|')]
    if len(globals_) != 1 or globals_[0][1:4] != ['sharedMemoryManager', config, platform] or globals_[0][-1] != 'v120':
        raise ValueError('Wrong project/config/toolset in ' + str(path))
    rows = [line.strip().split('|') for line in lines if line.strip().startswith('CL|')]
    rows = [row for row in rows if row[1].replace('\\', '/').endswith('/MemoryManager.cpp')]
    if len(rows) != 1 or len(rows[0]) != 8:
        raise ValueError('Expected exactly one complete MemoryManager.cpp metadata row')
    row = rows[0]
    definitions = [x for x in row[6].split(';') if x]
    includes = [x for x in row[7].split(';') if x]
    if any('$(' in x or '%(' in x for x in definitions + includes):
        raise ValueError('Unexpanded effective metadata')
    if platform == 'x64' and any(x.startswith('_USE_32BIT_TIME_T') for x in definitions):
        raise ValueError('x64 still defines _USE_32BIT_TIME_T')
    return definitions, includes


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=Path('C:/client-next-build'))
    p.add_argument('--audit', type=Path, required=True)
    p.add_argument('--output', type=Path, default=Path('C:/memory-next'))
    p.add_argument('--vcvars', type=Path, default=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat'))
    p.add_argument('--negative-header', action='store_true')
    args = p.parse_args()
    if os.name != 'nt':
        p.error('Run on native Windows with VS2013; no Wine or cross-compiler fallback')
    source = args.source.resolve()
    project_dir = source / 'src/engine/shared/library/sharedMemoryManager/build/win32'
    project = project_dir / 'sharedMemoryManager.vcxproj'
    tu = source / 'src/engine/shared/library/sharedMemoryManager/src/shared/MemoryManager.cpp'
    text = tu.read_text()
    marker = 'SystemAllocation must occupy one block'
    if marker not in text or not re.search(r'static_assert\s*\(\s*sizeof\(SystemAllocation\)\s*==\s*cms_blockSize', text):
        raise ValueError('Candidate must contain actual SystemAllocation compile-time assertion')
    if not args.vcvars.is_file():
        raise ValueError('VS2013 vcvarsall missing')
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    ns = {'m': 'http://schemas.microsoft.com/developer/msbuild/2003'}
    tree = ET.parse(project)
    result = {'passed': False, 'kind': 'actual TU compile only; not linked/runtime acceptance', 'source': str(source),
              'source_sha256': digest(tu), 'project_sha256': digest(project), 'runs': []}
    modes = [('candidate', tu)]
    if args.negative_header:
        negative = args.output / 'old-padding-MemoryManager.cpp'
        old = text
        for field in ('m_pad1', 'm_pad2'):
            old, count = re.subn(r'\bsize_t\s+' + field + r'\s*;', 'int ' + field + ';', old)
            if count != 1:
                raise ValueError('Expected one widened pad declaration: ' + field)
        negative.write_text(old)
        modes.append(('old-padding-negative', negative))
    for config in ('Debug', 'Release'):
        runtime = 'MultiThreadedDebug' if config == 'Debug' else 'MultiThreaded'
        matching = [g for g in tree.findall('m:ItemDefinitionGroup', ns)
                    if config + '|Win32' in g.get('Condition', '') or config + '|x64' in g.get('Condition', '')]
        rt = [g.findtext('m:ClCompile/m:RuntimeLibrary', namespaces=ns) for g in matching]
        if not rt or any(x != runtime for x in rt if x is not None):
            raise ValueError('Project CRT metadata differs from reviewed assumptions: ' + repr(rt))
        for platform, arch, machine in (('Win32', 'x86', 0x14c), ('x64', 'amd64', 0x8664)):
            audit = args.audit / ('sharedMemoryManager-' + config + '-' + platform + '.audit.log')
            definitions, includes = audit_metadata(audit, config, platform)
            for mode, input_tu in modes:
                if mode != 'candidate' and platform != 'x64':
                    continue
                run_dir = args.output / (config + '-' + platform + '-' + mode)
                run_dir.mkdir()
                obj = run_dir / 'MemoryManager.obj'
                flags = ['/c', '/EHsc', '/Y-', '/Gm-', '/W4', '/Zi', '/Gy', '/GR', '/Zc:forScope',
                         '/Zc:wchar_t-', '/FC', '/showIncludes', '/Ob1']
                flags += ['/MTd', '/Od', '/RTC1'] if config == 'Debug' else ['/MT', '/O2', '/Oi', '/Ot', '/Oy', '/GF']
                flags += ['/D' + quoted(x) for x in definitions]
                flags += ['/I' + quoted(x) for x in includes]
                flags += ['/Fo' + quoted(obj), '/Fd' + quoted(run_dir / 'compile.pdb'), quoted(input_tu)]
                rsp = run_dir / 'compile.rsp'
                rsp.write_text('\n'.join(flags) + '\n')
                bat = run_dir / 'compile.cmd'
                bat.write_text('@echo off\ncall ' + quoted(args.vcvars) + ' ' + arch + '\n'
                               'if errorlevel 1 exit /b 90\n'
                               'cd /d ' + quoted(project_dir) + '\n'
                               'set CL=\nset _CL_=\nwhere cl\ncl @' + quoted(rsp) + '\nexit /b %errorlevel%\n')
                r = subprocess.run(['cmd', '/d', '/c', str(bat)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
                log = run_dir / 'compile.log'
                log.write_bytes(r.stdout)
                output = r.stdout.decode('utf-8', errors='replace')
                toolset_ok = bool(re.search(r'Version 18\.00\.', output))
                actual_machine = struct.unpack('<H', obj.read_bytes()[:2])[0] if obj.exists() and obj.stat().st_size > 20 else None
                expected_failure = mode != 'candidate'
                passed = (r.returncode != 0 and bool(re.search(r'error C2338:.*' + re.escape(marker), output))) if expected_failure else (r.returncode == 0 and actual_machine == machine)
                included = {}
                for line in output.splitlines():
                    if 'including file:' in line:
                        name = Path(line.split('including file:', 1)[1].strip())
                        if name.is_file():
                            included[str(name.resolve())] = digest(name)
                row = {'name': run_dir.name, 'returncode': r.returncode, 'passed': passed and toolset_ok,
                       'toolset_18_confirmed': toolset_ok, 'coff_machine': actual_machine,
                       'input_sha256': digest(input_tu), 'audit_sha256': digest(audit),
                       'flags': flags, 'included_sha256': included}
                result['runs'].append(row)
                (args.output / 'results.json').write_text(json.dumps(result, indent=2))
                print(json.dumps({k: row[k] for k in ('name', 'returncode', 'passed', 'coff_machine')}), flush=True)
    result['source_unchanged'] = digest(tu) == result['source_sha256'] and digest(project) == result['project_sha256']
    result['passed'] = result['source_unchanged'] and all(x['passed'] for x in result['runs']) and len(result['runs']) == (6 if args.negative_header else 4)
    (args.output / 'results.json').write_text(json.dumps(result, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
