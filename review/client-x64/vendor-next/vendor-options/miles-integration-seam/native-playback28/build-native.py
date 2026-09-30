"""Prepared v120 amd64 object-only gate. Do not invoke before parent review."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import struct
import sys

if os.name != 'nt' or sys.argv[1:] != ['--approved-compile-only']:
    raise SystemExit('Requires Windows and explicit parent-approved compile-only invocation')

root = Path('C:/native-playback28')
base = root / 'native-playback28'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


manifest = json.loads((base / 'source-manifest.json').read_text())
for relative, expected in manifest.items():
    if sha256(root / relative) != expected:
        raise RuntimeError('source/helper identity mismatch: ' + relative)
sdk = Path('C:/client-next-build/src/external/3rd/library/miles/include/Mss.h')
if sha256(sdk) != '966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
    raise RuntimeError('private SDK header identity mismatch')

sys.path.insert(0, str(root / 'live-bridge-candidate/revision4-tools'))
from build_receipt import environment, identities, includes, run, exclusive_json

out = root / 'native-v1'
out.mkdir(exist_ok=False)
source_files = [root / p for p in manifest if Path(p).suffix in ('.h', '.cpp')]
builders = [root / p for p in manifest if Path(p).suffix in ('.py', '.json')]
before_sources = identities(source_files)
before_builders = identities(builders)
result = {'schema': 'miles-native-object-receipt-v1', 'architecture': 'amd64',
          'linked': False, 'executed': False, 'python_sha256': sha256(sys.executable),
          'sources_before': before_sources, 'builders_before': before_builders}
try:
    vc = Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
    env = environment(vc, 'amd64', out)
    compiler = Path(shutil.which('cl.exe', path=env['PATH']))
    dumpbin = Path(shutil.which('dumpbin.exe', path=env['PATH']))
    tool_files = {compiler, dumpbin, vc}
    tool_files.update(compiler.parent.glob('*.dll'))
    tool_files.update(compiler.parent.glob('1033/*.dll'))
    tool_files.update((vc.parent / 'bin').glob('*.dll'))
    tool_files.update((vc.parent.parent / 'Common7/IDE').glob('mspdb*.dll'))
    sources = [base / name for name in ['native_playback28.cpp', 'compile_exercise.cpp',
                                        'portable_contract.cpp']]
    command = [str(compiler), '/nologo', '/W4', '/WX', '/EHsc', '/MT', '/O2',
               '/DWIN32', '/D_WIN32_WINNT=0x0601', '/I' + str(sdk.parent)]
    command += [str(p) for p in sources]
    code, log = run(command + ['/Zs', '/showIncludes'], out, 'headers', env)
    result['discovery_exit'] = code
    if code:
        raise RuntimeError('native header/type discovery failed; no retry')
    headers = includes(log)
    if not headers or sdk.resolve() not in headers:
        raise RuntimeError('actual private SDK header not observed')
    before = {'sources': identities(source_files), 'headers': identities(headers),
              'tools': identities(tool_files)}
    result['before'] = before
    code, log = run(command + ['/c', '/showIncludes'], out, 'objects', env)
    result['compile_exit'] = code
    if code == 0:
        result['objects'] = [
            {'path': str(out / (source.stem + '.obj')),
             'sha256': sha256(out / (source.stem + '.obj')),
             'machine': struct.unpack('<H', (out / (source.stem + '.obj')).read_bytes()[:2])[0]}
            for source in sources]
    result['after'] = {'sources': identities(source_files), 'headers': identities(headers),
                       'tools': identities(tool_files)}
    result['inputs_unchanged'] = before == result['after'] and includes(log) == headers
    if code:
        raise RuntimeError('native object compile failed; no retry')
    if not result['inputs_unchanged']:
        raise RuntimeError('native inputs changed')
    code, symbols = run([str(dumpbin), '/symbols', str(out / 'native_playback28.obj')],
                         out, 'native-symbols', env)
    result['symbols_exit'] = code
    required = {'__imp_AIL_' + name for name in json.loads((base / 'operations.json').read_text())}
    observed = {line.split()[-1] for line in symbols.splitlines()
                if 'UNDEF' in line and '__imp_AIL_' in line}
    result['undefined_miles_imports'] = sorted(observed)
    result['exact_nineteen_unresolved'] = observed == required
    if code or observed != required:
        raise RuntimeError('actual nineteen unresolved SDK imports not observed exactly')
except Exception as error:
    result['failure'] = {'type': type(error).__name__, 'message': str(error)}
finally:
    result['sources_after'] = identities(source_files)
    result['builders_after'] = identities(builders)
    result['stable_sources'] = (before_sources == result['sources_after'] and
                                before_builders == result['builders_after'])
    result['no_link_output'] = not any(out.glob('*.exe')) and not any(out.glob('*.dll')) and not any(out.glob('*.lib'))
    result['passed'] = (not result.get('failure') and result.get('inputs_unchanged') and
                        result['stable_sources'] and result['no_link_output'] and
                        len(result.get('objects', [])) == 3 and
                        all(obj['machine'] == 0x8664 for obj in result.get('objects', [])))
    exclusive_json(out / 'receipt.json', result)
    pin = sha256(out / 'receipt.json')
    (out / 'receipt.sha256').write_text(pin + '\n')
    print(json.dumps({'passed': result['passed'], 'receipt_sha256': pin,
                      'linked': False, 'executed': False, 'failure': result.get('failure')}, indent=2))
raise SystemExit(not result['passed'])
