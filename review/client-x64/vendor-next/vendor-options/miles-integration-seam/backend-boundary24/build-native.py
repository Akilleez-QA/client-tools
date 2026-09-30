"""v120 amd64 object-only check. No linking, vendor call, or produced-PE execution."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import struct
import sys

root = Path('C:/backend-boundary24')
sys.path.insert(0, str(root / 'revision4-tools'))
from build_receipt import environment, identities, includes, run, exclusive_json
from receipt import digest

out = root / 'native-v1'
out.mkdir(exist_ok=False)
sdk = Path('C:/client-next-build/src/external/3rd/library/miles')
if digest(sdk / 'include/Mss.h') != '966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
    raise RuntimeError('actual SDK header identity mismatch')
manifest = json.loads((root / 'source-manifest.json').read_text())
for relative, expected in manifest.items():
    if digest(root / relative) != expected:
        raise RuntimeError('source snapshot mismatch: ' + relative)
source_files = [root / p for p in manifest if Path(p).suffix in ('.h', '.cpp')]
builder_files = [root / p for p in manifest if Path(p).suffix == '.py']
sources_before = identities(source_files)
builders_before = identities(builder_files)
vc = Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
env = environment(vc, 'amd64', out)
compiler = Path(shutil.which('cl.exe', path=env['PATH']))
dumpbin = Path(shutil.which('dumpbin.exe', path=env['PATH']))
tools = {compiler, dumpbin, vc}
tools.update(compiler.parent.glob('*.dll'))
tools.update(compiler.parent.glob('1033/*.dll'))
tools.update((vc.parent / 'bin').glob('*.dll'))
tools.update((vc.parent.parent / 'Common7/IDE').glob('mspdb*.dll'))
sources = [root / 'backend-boundary24' / p for p in [
    'native/native_miles64.cpp', 'pipe/ClientMilesPipe.cpp', 'pipe/LiveChannel.cpp',
    'sample/startup_calls.cpp', 'fixture/live_controller.cpp']]
command = [str(compiler), '/nologo', '/W4', '/WX', '/EHsc', '/MT', '/O2',
           '/DWIN32', '/D_WIN32_WINNT=0x0601', '/I' + str(sdk / 'include')]
command += [str(p) for p in sources]
discovery_exit, discovery_log = run(command + ['/Zs', '/showIncludes'], out, 'headers', env)
result = {'schema': 'miles-source-compile-receipt-v1', 'architecture': 'amd64',
          'discovery_exit': discovery_exit, 'linked': False, 'executed': False,
          'sources_before': sources_before, 'builders_before': builders_before,
          'python_sha256': digest(sys.executable)}
if discovery_exit == 0:
    headers = includes(discovery_log)
    before = {'sources': identities(source_files), 'headers': identities(headers),
              'tools': identities(tools)}
    code, log = run(command + ['/c', '/showIncludes'], out, 'objects', env)
    objects = []
    if code == 0:
        for source in sources:
            path = out / (source.stem + '.obj')
            objects.append({'path': str(path), 'sha256': digest(path),
                            'machine': struct.unpack('<H', path.read_bytes()[:2])[0]})
    after = {'sources': identities(source_files), 'headers': identities(headers),
             'tools': identities(tools)}
    result.update(compile_exit=code, before=before, after=after, objects=objects,
                  inputs_unchanged=before == after and includes(log) == headers)
    if code == 0:
        symbol_exit, symbols = run([str(dumpbin), '/symbols', str(out / 'native_miles64.obj')],
                                   out, 'native-symbols', env)
        required = ['AIL_startup', 'AIL_shutdown', 'AIL_get_preference', 'AIL_set_preference',
                    'AIL_last_error', 'AIL_set_redist_directory', 'AIL_open_digital_driver',
                    'AIL_speaker_configuration']
        unresolved = [line for line in symbols.splitlines() if 'UNDEF' in line and '__imp_AIL_' in line]
        result.update(symbol_exit=symbol_exit, undefined_miles_imports=unresolved,
                      required_imports_unresolved=all(any('__imp_' + name in line for line in unresolved)
                                                      for name in required))
result['sources_after'] = identities(source_files)
result['builders_after'] = identities(builder_files)
result['stable_sources'] = (result['sources_before'] == result['sources_after'] and
                            result['builders_before'] == result['builders_after'])
result['no_pe_output'] = not list(out.glob('*.exe')) and not list(out.glob('*.dll'))
path = out / 'receipt.json'
exclusive_json(path, result)
pin = digest(path)
(out / 'receipt.sha256').write_text(pin + '\n')
os.chmod(path, 0o444)
passed = (result['discovery_exit'] == 0 and result.get('compile_exit') == 0 and
          result.get('inputs_unchanged') and result['stable_sources'] and
          result.get('symbol_exit') == 0 and result.get('required_imports_unresolved') and
          result['no_pe_output'] and all(p['machine'] == 0x8664 for p in result.get('objects', [])))
print(json.dumps({'receipt_sha256': pin, 'passed': bool(passed),
                  'discovery_exit': result['discovery_exit'], 'compile_exit': result.get('compile_exit'),
                  'linked': False, 'executed': False, 'object_count': len(result.get('objects', []))}, indent=2))
raise SystemExit(not passed)
