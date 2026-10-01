import hashlib
import json
from pathlib import Path
import struct
import subprocess

def validate_results(rows, source_hash, contract_hash):
    """Check the original required verdict and identity; safe to use on saved records."""
    problems = []
    if not isinstance(rows, list) or len(rows) != 2:
        return ['Expected exactly two architecture records']
    for platform, machine in [('Win32', 0x14c), ('x64', 0x8664)]:
        matches = [row for row in rows if isinstance(row, dict) and row.get('platform') == platform]
        if len(matches) != 1:
            problems.append(platform + ': expected exactly one record')
            continue
        row = matches[0]
        for field, expected in [('compile_exit', 0), ('machine', machine), ('run_exit', 0),
                                ('source_sha256', source_hash), ('contract_sha256', contract_hash)]:
            if row.get(field) != expected:
                problems.append(platform + ': incorrect or missing ' + field)
        output = row.get('output')
        lines = output.splitlines() if isinstance(output, str) else []
        verdict = 'RESULT arch=' + platform + ' cases=16 queries=32 failures=0 keyDeleted=1'
        if [line for line in lines if line.startswith('RESULT ')] != [verdict]:
            problems.append(platform + ': missing, duplicate or failed required verdict')
        if 'CLEANUP close=0 delete=0 absent=2' not in lines:
            problems.append(platform + ': missing successful cleanup record')
        if sum(line.startswith('CASE ') for line in lines) != 16 or sum(line.startswith('QUERY ') for line in lines) != 32:
            problems.append(platform + ': incorrect corpus count')
        if any(line.startswith('FAIL') for line in lines):
            problems.append(platform + ': failure record')
    return problems


def result_exit_status(rows, source_hash, contract_hash):
    return 1 if validate_results(rows, source_hash, contract_hash) else 0


def main():
    out = Path(__file__).resolve().parent
    identity = json.loads((out / 'run-id.json').read_text())
    source = out / 'probe.cpp'
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    contract_hash = hashlib.sha256((out / 'prospective-contract.json').read_bytes()).hexdigest()
    rows = []
    for platform, arch, machine in [('Win32', 'x86', 0x14c), ('x64', 'amd64', 0x8664)]:
        d = out / platform
        d.mkdir(exist_ok=False)
        exe = d / 'probe.exe'
        command = ('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '
                   + arch + ' >nul\nif errorlevel 1 exit /b %errorlevel%\ncl /nologo /EHsc /MT /O2 /W4 /WX '
                   '/D_CRT_SECURE_NO_WARNINGS "' + str(source) + '" /Fo"' + str(d / 'probe.obj')
                   + '" /Fe"' + str(exe) + '" /link advapi32.lib\nexit /b %errorlevel%\n')
        (d / 'build.cmd').write_text(command)
        r = subprocess.run(['cmd', '/d', '/c', str(d / 'build.cmd')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (d / 'build.log').write_bytes(r.stdout)
        row = {'platform': platform, 'source_sha256': source_hash,
               'contract_sha256': contract_hash, 'compile_exit': r.returncode}
        rows.append(row)
        (out / 'results.json').write_text(json.dumps(rows, indent=2))
        if r.returncode:
            print(json.dumps(row), flush=True)
            continue
        data = exe.read_bytes()
        pe = struct.unpack_from('<I', data, 0x3c)[0]
        row['machine'] = struct.unpack_from('<H', data, pe + 4)[0]
        row['executable_sha256'] = hashlib.sha256(data).hexdigest()
        if row['machine'] != machine:
            row['machine_failure'] = True
        else:
            argv = [str(exe), identity['run_id']]
            (d / 'run-command.json').write_text(json.dumps(argv, indent=2))
            r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (d / 'run.log').write_bytes(r.stdout)
            row.update(run_exit=r.returncode, output=r.stdout.decode('utf-8', errors='replace'))
        (out / 'results.json').write_text(json.dumps(rows, indent=2))
        print(json.dumps(row), flush=True)
    problems = validate_results(rows, source_hash, contract_hash)
    (out / 'verification.json').write_text(json.dumps({'problems': problems}, indent=2))
    return result_exit_status(rows, source_hash, contract_hash)


if __name__ == '__main__':
    raise SystemExit(main())
