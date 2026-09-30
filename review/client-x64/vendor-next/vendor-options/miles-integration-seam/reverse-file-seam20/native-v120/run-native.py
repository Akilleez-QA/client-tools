#!/usr/bin/env python3
"""Compile full baseline/candidate Audio.cpp using native v120; never link/run."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys

ROOT = Path('C:/file-seam21')
SNAPSHOT = ROOT / 'snapshot'
PROJECT_REL = 'src/engine/client/library/clientAudio/build/win32'
AUDIO_REL = 'src/engine/client/library/clientAudio/src/win32/Audio.cpp'
PROJECT = SNAPSHOT / PROJECT_REL
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=False)
MANIFEST = json.loads((ROOT / 'input-manifest.json').read_text())
VCVARS = Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


for relative, expected in MANIFEST['sha256'].items():
    if digest(ROOT / relative) != expected:
        raise RuntimeError('Input hash mismatch: ' + relative)

results = []
for configuration in ['Debug', 'Release']:
    for platform, arch, machine in [('Win32', 'x86', 0x14c), ('x64', 'amd64', 0x8664)]:
        setup = OUT / (configuration + '-' + platform + '-environment.cmd')
        setup.write_text('@echo off\ncall "' + str(VCVARS) + '" ' + arch +
                         ' >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n')
        # Never save or print the environment: it may contain credentials.
        prepared = subprocess.run(['cmd', '/d', '/c', str(setup)],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  timeout=45)
        if prepared.returncode:
            raise RuntimeError('vcvars failed: ' + platform)
        environment = {k.upper(): v for k, v in os.environ.items()}
        for line in prepared.stdout.decode(errors='replace').splitlines():
            if '=' in line and not line.startswith('='):
                key, value = line.split('=', 1)
                environment[key.upper()] = value
        compiler = shutil.which('cl.exe', path=environment['PATH'])
        if not compiler:
            raise RuntimeError('Native compiler missing')
        audit = ROOT / 'inputs' / ('clientAudio-' + configuration + '-' + platform + '.audit.log')
        rows = [line.strip().split('|') for line in audit.read_text(encoding='utf-8-sig').splitlines()
                if line.strip().startswith('CL|')]
        row = next(row for row in rows if row[1].replace('\\', '/').endswith('/Audio.cpp'))
        include_flags = ['/I' + entry for entry in row[7].split(';') if entry]
        definitions = ['/D' + entry for entry in row[6].split(';') if entry]
        for mode in ['baseline', 'candidate']:
            directory = OUT / (configuration + '-' + platform + '-' + mode)
            directory.mkdir()
            source = SNAPSHOT / AUDIO_REL if mode == 'baseline' else ROOT / 'candidate' / AUDIO_REL
            guard = directory / 'require-v120.h'
            guard.write_text('#if !defined(_MSC_VER) || _MSC_VER != 1800\n'
                             '#error Native VS2013 v120 required\n#endif\n'
                             '#define SEAM21_TEXT_INNER(x) #x\n'
                             '#define SEAM21_TEXT(x) SEAM21_TEXT_INNER(x)\n'
                             '#pragma message("SEAM21 _MSC_FULL_VER=" SEAM21_TEXT(_MSC_FULL_VER))\n')
            # Project config behavior, independently compiled with PCH disabled
            # and all output paths redirected into this one disposable directory.
            flags = ['/nologo', '/c', '/EHsc', '/Y-', '/Gm-', '/Zc:wchar_t-', '/Zc:forScope',
                     '/GR', '/Gy', '/fp:precise', '/W4', '/Zi', '/FC',
                     '/showIncludes', '/FI' + str(guard), '/Fd' + str(directory / 'Audio.pdb')]
            flags += ['/MTd', '/Od', '/Ob1', '/RTC1', '/WX'] if configuration == 'Debug' else ['/MT', '/O2', '/Ob1', '/Oi', '/Ot', '/Oy', '/GF', '/WX-']
            flags += definitions
            if mode == 'candidate':
                flags += ['/I' + str(ROOT / 'candidate/src/engine/client/library/clientAudio/include/public')]
            flags += include_flags
            obj = directory / 'Audio.obj'
            command = [compiler] + flags + [str(source), '/Fo' + str(obj)]
            (directory / 'command.json').write_text(json.dumps(command, indent=2) + '\n')
            record = dict(configuration=configuration, platform=platform, mode=mode,
                          source=str(source), source_sha256=digest(source),
                          audit_sha256=digest(audit), compiler=compiler,
                          compiler_sha256=digest(Path(compiler)), cwd=str(PROJECT),
                          command=command, status='pending')
            results.append(record)
            try:
                completed = subprocess.run(command, cwd=PROJECT, env=environment,
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                           timeout=180)
                code, output = completed.returncode, completed.stdout
            except subprocess.TimeoutExpired as error:
                code, output = -999, (error.stdout or b'') + b'\nTIMEOUT\n'
            (directory / 'compile.log').write_bytes(output)
            record['exit_code'] = code
            headers = {}
            for line in output.decode(errors='replace').splitlines():
                matched = re.match(r'^Note: including file:\s*(.+?)\s*$', line)
                if matched:
                    path = Path(matched.group(1)).resolve()
                    headers[str(path)] = digest(path)
            (directory / 'actual-includes.json').write_text(json.dumps(headers, indent=2) + '\n')
            record['actual_include_count'] = len(headers)
            record['actual_includes_sha256'] = digest(directory / 'actual-includes.json')
            record['diagnostics'] = [line for line in output.decode(errors='replace').splitlines()
                                     if re.search(r'\b(?:warning|error|fatal error) [A-Z]\d+', line)]
            record['status'] = 'compile-failed' if code else 'compiled'
            if not code:
                data = obj.read_bytes()
                actual_machine = struct.unpack_from('<H', data)[0]
                record.update(object_sha256=digest(obj), object_bytes=len(data),
                              coff_machine=hex(actual_machine))
                if actual_machine != machine:
                    record['status'] = 'wrong-object-machine'
                if mode == 'candidate':
                    names = [b'?open@ClientAudioFileCallbacks@@', b'?close@ClientAudioFileCallbacks@@',
                             b'?seek@ClientAudioFileCallbacks@@', b'?read@ClientAudioFileCallbacks@@']
                    record['adapter_symbol_prefixes_present'] = {name.decode(): name in data for name in names}
                    if not all(record['adapter_symbol_prefixes_present'].values()):
                        record['status'] = 'missing-adapter-object-symbol'
            (OUT / 'results.json').write_text(json.dumps(dict(builds=results), indent=2) + '\n')
            print(json.dumps({key: record[key] for key in ['configuration', 'platform', 'mode', 'status', 'exit_code', 'actual_include_count']}), flush=True)

sys.exit(0 if all(record['status'] == 'compiled' for record in results) else 1)
