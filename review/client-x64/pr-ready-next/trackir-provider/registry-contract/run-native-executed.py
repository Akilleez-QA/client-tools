import hashlib
import json
from pathlib import Path
import struct
import subprocess

out = Path(__file__).resolve().parent
identity = json.loads((out / 'run-id.json').read_text())
rows = []
for platform, arch, machine in [('Win32', 'x86', 0x14c), ('x64', 'amd64', 0x8664)]:
    d = out / platform
    d.mkdir(exist_ok=False)
    source = out / 'probe.cpp'
    exe = d / 'probe.exe'
    command = ('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '
               + arch + ' >nul\nif errorlevel 1 exit /b %errorlevel%\ncl /nologo /EHsc /MT /O2 /W4 /WX '
               '/D_CRT_SECURE_NO_WARNINGS "' + str(source) + '" /Fo"' + str(d / 'probe.obj')
               + '" /Fe"' + str(exe) + '" /link advapi32.lib\nexit /b %errorlevel%\n')
    (d / 'build.cmd').write_text(command)
    r = subprocess.run(['cmd', '/d', '/c', str(d / 'build.cmd')], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (d / 'build.log').write_bytes(r.stdout)
    row = {'platform': platform, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
           'contract_sha256': hashlib.sha256((out / 'prospective-contract.json').read_bytes()).hexdigest(),
           'compile_exit': r.returncode}
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
