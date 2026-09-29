#!/usr/bin/env python3
"""Rebuild Win32 Release baseline, relink a link-only candidate, compare whole PEs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import re

HERE = Path(__file__).resolve().parent
PROJECT = 'src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj'
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--base-archive', type=Path, required=True, help='git archive --format=tar of the baseline')
p.add_argument('--candidate-archive', type=Path, required=True, help='git archive --format=tar of the candidate')
p.add_argument('--output', type=Path, required=True, help='new disposable directory; must not exist')
p.add_argument('--environment-template', type=Path, required=True,
               help='prepared Win32 build tree supplying ignored SDK/configuration files')
p.add_argument('--msbuild', type=Path, required=True, help='VS2013 MSBuild12 executable')
a = p.parse_args()
if os.name != 'nt':
    p.error('native Windows with the documented v120 SDK environment is required')
out = a.output.resolve()
if out.exists():
    p.error('--output must be new; refusing to overwrite existing evidence')
def inspect_archive(path):
    with tarfile.open(path) as archive:
        sha = archive.pax_headers.get('comment', '')
        if not re.fullmatch('[0-9a-f]{40}', sha):
            p.error('archive must carry the full commit ID written by git archive')
        files = {m.name: hashlib.sha256(archive.extractfile(m).read()).hexdigest()
                 for m in archive.getmembers() if m.isfile()}
        project = archive.extractfile(PROJECT).read()
    return sha, files, project
base, base_files, base_project = inspect_archive(a.base_archive)
head, head_files, head_project = inspect_archive(a.candidate_archive)
changed = sorted(x for x in base_files.keys() | head_files.keys()
                 if base_files.get(x) != head_files.get(x))
if [x for x in changed if not x.startswith('tools/test-link-inputs/')] != [PROJECT]:
    p.error('candidate must change only the SwgClient project plus this test tooling')
out.mkdir(parents=True)
work = out / 'build-tree'
record = {'base': base, 'candidate': head, 'outcome': 'incomplete', 'commands': []}
def save():
    (out / 'run.json').write_text(json.dumps(record, indent=2) + '\n')
def run(cmd, label):
    record['commands'].append(cmd); save()
    with (out / (label + '.log')).open('w') as log:
        log.write(f'base={base}\ncandidate={head}\n'); log.flush()
        r = subprocess.run(cmd, cwd=work, stdout=log, stderr=subprocess.STDOUT)
    (out / (label + '.exit')).write_text(str(r.returncode) + '\n')
    if r.returncode:
        raise RuntimeError(f'{label} failed: {r.returncode}')
try:
    # The template supplies dependencies, not the source oracle or compiled game objects.
    shutil.copytree(a.environment_template, work, ignore=shutil.ignore_patterns('.git'))
    record['base_archive_sha256'] = hashlib.sha256(a.base_archive.read_bytes()).hexdigest()
    record['candidate_archive_sha256'] = hashlib.sha256(a.candidate_archive.read_bytes()).hexdigest()
    with tarfile.open(a.base_archive) as archive:
        archive.extractall(work, filter='data')
    for revision, target, label in [(base, 'SwgClient:Rebuild', 'before'),
                                    (head, 'SwgClient', 'after')]:
        (work / PROJECT).write_bytes(base_project if label == 'before' else head_project)
        exe = work / 'src/compile/win32/SwgClient/Release/SwgClient_r.exe'
        exe.unlink(missing_ok=True)
        run([str(a.msbuild), str(work / 'src/build/win32/swg.sln'), '/t:' + target,
             '/p:Configuration=Release', '/p:Platform=Win32', '/m:2', '/v:normal'], label)
        exe = work / 'src/compile/win32/SwgClient/Release/SwgClient_r.exe'
        if not exe.is_file():
            raise RuntimeError(f'expected product not found: {exe}')
        shutil.copy2(exe, out / ('product-' + label + '.exe'))
    run([sys.executable, str(HERE / 'compare.py'), str(out / 'product-before.exe'),
         str(out / 'product-after.exe'), '--output', str(out / 'comparison.json')], 'compare')
    record['outcome'] = 'passed'
except Exception as exc:
    record['outcome'] = 'failed'; record['error'] = str(exc)
    raise
finally:
    save()
