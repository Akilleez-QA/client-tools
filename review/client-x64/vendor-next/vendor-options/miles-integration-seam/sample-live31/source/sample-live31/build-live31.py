"""One native Release pair; frozen revision4 receipt mechanics, no PE launches."""
from pathlib import Path
import sys, json, shutil, re, os, platform
root = Path('C:/sample-live31')
sys.path.insert(0, str(root / 'live-bridge-candidate/revision4-tools'))
from build_receipt import environment, identities, includes, run, exclusive_json, LIB_NAMES
from receipt import digest, machine
if sys.argv[1:] != ['--approved-build-only']:
    raise RuntimeError('explicit parent-approved build-only gate required')
out = root / 'build-v1'
out.mkdir(exist_ok=False)
records = []
source_files = []
builder_files = []
initial = {}
builder_before = {}
failure = None
try:
    vc = Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
    sdk = Path('C:/client-next-build/src/external/3rd/library/miles')
    if digest(sdk / 'include/Mss.h') != '966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
        raise RuntimeError('SDK mismatch')
    if digest(sdk / 'lib/win/Mss32.lib') != 'e8c57b302fa2ea699a635ae1dad5467abd810370472c3b1d7d6e6ebc15af9252':
        raise RuntimeError('original import library mismatch')
    manifest = json.loads((root / 'source-manifest.json').read_text())
    for relative, expected in manifest.items():
        if digest(root / relative) != expected:
            raise RuntimeError('snapshot mismatch ' + relative)
    source_files = [root / p for p in manifest if Path(p).suffix in ['.cpp', '.h']]
    builder_files = [root / p for p in manifest if Path(p).suffix in ['.py', '.json']]
    initial = identities(source_files)
    builder_before = identities(builder_files)
    records = []
    for arch in ['x86', 'amd64']:
        target = out / (arch + '-Release')
        target.mkdir()
        env = environment(vc, arch, target)
        cl = Path(shutil.which('cl.exe', path=env['PATH']))
        link = Path(shutil.which('link.exe', path=env['PATH']))
        dumpbin = Path(shutil.which('dumpbin.exe', path=env['PATH']))
        source = ['transport-candidate/codec.cpp', 'pipe-transport-candidate/endpoint.cpp',
                  'startup-metadata-v4/metadata_wire.cpp', 'session-version22/session_version.cpp']
        if arch == 'x86':
            source += ['sample-live31/host.cpp', 'host-candidate/host_dispatch.cpp', 'coordinator-candidate/coordinator.cpp',
                       'startup-metadata-v4/metadata_host.cpp', 'session-version22/session_version_host.cpp']
        else:
            source += ['sample-live31/controller.cpp',
                       'backend-boundary24/pipe/ClientMilesPipe.cpp',
                       'backend-boundary24/pipe/LiveChannel.cpp']
        flags = [str(cl), '/nologo', '/W4', '/WX', '/EHsc', '/DWIN32', '/D_WIN32_WINNT=0x0601', '/I' + str(sdk / 'include'), '/MT', '/O2']
        command = flags + [str(root / x) for x in source]
        code, log = run(command + ['/Zs', '/showIncludes'], target, 'headers', env)
        record = dict(config='Release', architecture=arch, discovery_exit=code)
        if code:
            record.update(exit_code=code, inputs_unchanged=False)
            records.append(record)
            break
        headers = includes(log)
        if not headers or (arch == 'x86' and (sdk / 'include/Mss.h').resolve() not in headers):
            record.update(exit_code=-1, inputs_unchanged=False, failure='missing actual SDK include evidence')
            records.append(record)
            break
        tools = {cl, link, dumpbin, vc}
        tools.update(cl.parent.glob('*.dll'))
        tools.update(cl.parent.glob('1033/*.dll'))
        tools.update((vc.parent / 'bin').glob('*.dll'))
        tools.update((vc.parent.parent / 'Common7/IDE').glob('mspdb*.dll'))
        libs = set()
        for directory in env['LIB'].split(';'):
            for name in LIB_NAMES:
                p = Path(directory) / (name + '.lib')
                if p.is_file():
                    libs.add(p.resolve())
        if arch == 'x86':
            libs.add((sdk / 'lib/win/Mss32.lib').resolve())
    
        def snapshot():
            return dict(sources=identities(source_files), headers=identities(headers), tools=identities(tools), libraries=identities(libs))
        before = snapshot()
        exe = target / ('host.exe' if arch == 'x86' else 'controller.exe')
        command += ['/showIncludes', '/Fe' + str(exe)]
        if arch == 'x86':
            command.append(str(sdk / 'lib/win/Mss32.lib'))
        command += ['/link', '/VERBOSE:LIB', 'user32.lib']
        code, log = run(command, target, 'compile', env)
        output = dict(path=str(exe), sha256=digest(exe), machine=machine(exe)) if code == 0 else None
        import_code, import_log = (None, '')
        imports_ok = False
        if code == 0:
            import_code, import_log = run([str(dumpbin), '/imports', str(exe)], target, 'imports', env)
            expected_imports = ['AIL_allocate_sample_handle', 'AIL_sample_ms_position',
                                'AIL_end_sample', 'AIL_release_sample_handle']
            imports_ok = import_code == 0 and (all(name in import_log for name in expected_imports)
                         and 'mss32.dll' in import_log.lower() if arch == 'x86'
                         else 'mss32.dll' not in import_log.lower() and 'mss64.dll' not in import_log.lower())
        after = snapshot()
        searched = {Path(m.group(1)).resolve() for line in log.splitlines() for m in [re.match('\\s*Searching (.+\\.lib):\\s*$', line)] if m and Path(m.group(1)).is_file()}
        uncovered = sorted((str(p) for p in searched - libs))
        record.update(exit_code=code, before=before, after=after, output=output, inputs_unchanged=before == after and before['sources'] == initial and (includes(log) == headers) and (not uncovered), unrecorded_libraries=uncovered, observed_link_library_paths=sorted((str(p) for p in searched)))
        record['imports_ok'] = imports_ok
        record['import_discovery_exit'] = import_code
        record['machine_ok'] = imports_ok and output is not None and output['machine'] == (0x14c if arch == 'x86' else 0x8664)
        records.append(record)
        if code or not record['inputs_unchanged'] or not record['machine_ok']:
            break
except Exception as error:
    failure = {'type': type(error).__name__, 'message': str(error)}

r = dict(schema='miles-build-receipt-v4', builds=records, builder_before=builder_before, builder_after=identities(builder_files), source_snapshot_before=initial, source_snapshot_after=identities(source_files), python_sha256=digest(sys.executable), system=platform.platform(), scope='sample-live31 Release pair from frozen live27 plus repaired client29/host29 and fixture30; compile only; no execution')
r['source_manifest_sha256'] = digest(root / 'source-manifest.json')
r['failure'] = failure
r['stable_matrix'] = failure is None and len(records) == 2 and all(x.get('machine_ok', False) for x in records) and r['builder_before'] == r['builder_after'] and r['source_snapshot_before'] == r['source_snapshot_after']
p = out / 'receipt.json'
exclusive_json(p, r)
pin = digest(p)
(out / 'receipt.sha256').write_text(pin + '\n')
os.chmod(p, 292)
print(json.dumps(dict(receipt_sha256=pin, stable_matrix=r['stable_matrix'], builds=[{k: x.get(k) for k in ['architecture', 'discovery_exit', 'exit_code', 'inputs_unchanged']} for x in records]), indent=2))
raise SystemExit(not r['stable_matrix'] or any((x['exit_code'] or not x['inputs_unchanged'] for x in records)))
