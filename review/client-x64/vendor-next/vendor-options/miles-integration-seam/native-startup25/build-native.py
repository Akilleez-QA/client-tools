"""Prepared v120 x64 /c driver. Parent approval required before invocation.
Stage source-manifest paths under C:/native-startup25, preserving seam-relative paths.
No link, engine/vendor execution, import-library creation or DLL loading.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import struct
import sys

if os.name != 'nt' or sys.argv[1:] != ['--approved-compile-only']:
    raise SystemExit('Requires Windows and parent-approved compile-only invocation')
root = Path('C:/native-startup25')
base = root / 'native-startup25'
sys.path.insert(0, str(root / 'live-bridge-candidate/revision4-tools'))
from build_receipt import environment, identities, includes, run, exclusive_json
from receipt import digest

out = root / 'native-v1'
out.mkdir(exist_ok=False)
sdk = Path('C:/client-next-build/src/external/3rd/library/miles/include/Mss.h')
if digest(sdk) != '966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
    raise RuntimeError('SDK identity mismatch')
manifest = json.loads((base / 'source-manifest.json').read_text())
for name, expected in manifest.items():
    if digest(root / name) != expected:
        raise RuntimeError('source identity mismatch: ' + name)
source_files = [root / name for name in manifest if Path(name).suffix in ('.h', '.cpp')]
builders = [root / name for name in manifest if Path(name).suffix == '.py']
before_sources, before_builders = identities(source_files), identities(builders)
vc = Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
env = environment(vc, 'amd64', out)
compiler = Path(shutil.which('cl.exe', path=env['PATH']))
dumpbin = Path(shutil.which('dumpbin.exe', path=env['PATH']))
tools = {compiler, dumpbin, vc}
tools.update(compiler.parent.glob('*.dll'))
tools.update(compiler.parent.glob('1033/*.dll'))
tools.update((vc.parent / 'bin').glob('*.dll'))
tools.update((vc.parent.parent / 'Common7/IDE').glob('mspdb*.dll'))
sources = [root / 'backend-boundary24/native/native_miles64.cpp',
           base / 'native/native_startup25.cpp', base / 'sample/install_order.cpp',
           base / 'tests/portable_contract.cpp']
command = [str(compiler), '/nologo', '/W4', '/WX', '/EHsc', '/MT', '/O2',
           '/DWIN32', '/D_WIN32_WINNT=0x0601', '/I' + str(sdk.parent)] + [str(p) for p in sources]
code, log = run(command + ['/Zs', '/showIncludes'], out, 'headers', env)
result = {'architecture': 'amd64', 'discovery_exit': code, 'linked': False, 'executed': False,
          'python_sha256': digest(sys.executable), 'sources_before': before_sources,
          'builders_before': before_builders}
if code == 0:
    headers = includes(log)
    before = {'sources': identities(source_files), 'headers': identities(headers), 'tools': identities(tools)}
    code, log = run(command + ['/c', '/showIncludes'], out, 'objects', env)
    result['compile_exit'] = code
    result['before'] = before
    result['after'] = {'sources': identities(source_files), 'headers': identities(headers), 'tools': identities(tools)}
    result['inputs_unchanged'] = before == result['after'] and includes(log) == headers
    if code == 0:
        result['objects'] = [{'path': str(out / (p.stem + '.obj')),
                              'sha256': digest(out / (p.stem + '.obj')),
                              'machine': struct.unpack('<H', (out / (p.stem + '.obj')).read_bytes()[:2])[0]}
                             for p in sources]
        status, symbols = run([str(dumpbin), '/symbols', str(out / 'native_startup25.obj')],
                              out, 'native-symbols', env)
        required = ['set_file_callbacks', 'set_listener_3D_position', 'set_listener_3D_velocity_vector',
                    'set_listener_3D_orientation', 'set_3D_rolloff_factor', 'serve', 'room_type', 'set_room_type']
        unresolved = [line for line in symbols.splitlines() if 'UNDEF' in line and '__imp_AIL_' in line]
        result.update(symbol_exit=status, undefined_miles_imports=unresolved,
                      all_eight_imports_unresolved=all(any('__imp_AIL_' + name in line for line in unresolved)
                                                      for name in required))
result['sources_after'], result['builders_after'] = identities(source_files), identities(builders)
result['stable_sources'] = before_sources == result['sources_after'] and before_builders == result['builders_after']
result['no_pe_output'] = not list(out.glob('*.exe')) and not list(out.glob('*.dll'))
result['passed'] = (result['discovery_exit'] == 0 and result.get('compile_exit') == 0 and
                    result.get('inputs_unchanged') and result['stable_sources'] and
                    result.get('symbol_exit') == 0 and result.get('all_eight_imports_unresolved') and
                    result['no_pe_output'] and len(result.get('objects', [])) == 4 and
                    all(p['machine'] == 0x8664 for p in result.get('objects', [])))
exclusive_json(out / 'receipt.json', result)
(out / 'receipt.sha256').write_text(digest(out / 'receipt.json') + '\n')
print(json.dumps({k: result[k] for k in ('passed', 'linked', 'executed', 'discovery_exit')}, indent=2))
raise SystemExit(not result['passed'])
