"""Check attribution and publication contents; this is not a runtime test."""
import hashlib
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
B = ROOT / 'backend-boundary24'
sha = lambda data: hashlib.sha256(data).hexdigest()
source = json.loads((B / 'source-manifest.json').read_text())
def local_source(name):
    if name.startswith('revision4-tools/'):
        return ROOT / 'live-bridge-candidate' / name
    return ROOT / name

for name, expected in source.items():
    assert sha(local_source(name).read_bytes()) == expected, name

allowed = {'.h', '.cpp', '.py', '.md', '.json', '.yaml', '.txt', '.log', '.cmd', '.rsp', '.tar', '.sha256'}
archives = {}
for name in ('source-v1.tar', 'packet-v1.tar'):
    with tarfile.open(B / name) as archive:
        members = archive.getmembers()
        assert len({m.name for m in members}) == len(members)
        for member in members:
            path = Path(member.name)
            assert member.isfile() and not path.is_absolute() and '..' not in path.parts
            assert path.name.lower() != 'mss.h'
            assert path.suffix in allowed or path.name == '.gitignore', member.name
            data = archive.extractfile(member).read()
            assert not data.startswith((b'MZ', b'\x7fELF')), member.name
            # The packet includes the source tar, audited independently above.
            if name == 'source-v1.tar' and member.name in source:
                assert sha(data) == source[member.name]
        archives[name] = {'sha256': sha((B / name).read_bytes()), 'members': len(members)}

r = json.loads((B / 'evidence-native-v1/receipt.json').read_text())
assert all(r[k] == 0 for k in ('compile_exit', 'discovery_exit', 'symbol_exit'))
assert all(r[k] for k in ('inputs_unchanged', 'stable_sources', 'no_pe_output', 'required_imports_unresolved'))
assert not r['linked'] and not r['executed']
assert r['sources_before'] == r['sources_after']
assert r['builders_before'] == r['builders_after']
assert len(r['objects']) == 5 and all(o['machine'] == 0x8664 for o in r['objects'])
prefix = 'C:\\backend-boundary24\\'
for name, expected in r['sources_after'].items():
    assert name.startswith(prefix), name
    assert sha(local_source(name[len(prefix):].replace('\\', '/')).read_bytes()) == expected, name
expected_imports = {'AIL_startup', 'AIL_shutdown', 'AIL_get_preference', 'AIL_set_preference',
                    'AIL_last_error', 'AIL_set_redist_directory', 'AIL_open_digital_driver',
                    'AIL_speaker_configuration'}
assert {s.split('__imp_')[1] for s in r['undefined_miles_imports']} == expected_imports
p = json.loads((B / 'evidence-portable-v1/results.json').read_text())
assert p['adapter_build_exit'] == p['adapter_run_exit'] == p['isolation_link_exit'] == 0
assert p['missing_implementation_link_exit'] != 0
assert p['inputs_unchanged'] and p['inputs_before'] == p['inputs_after']
assert not p['vendor_execution'] and not p['native_execution'] and not p['isolated_executable_run']
result = {'source_files_checked': len(source), 'archives': archives,
          'native_receipt_sha256': sha((B / 'evidence-native-v1/receipt.json').read_bytes()),
          'portable_receipt_sha256': sha((B / 'evidence-portable-v1/results.json').read_bytes()),
          'native_objects_reported': len(r['objects']), 'real_imports_reported': sorted(expected_imports),
          'passed': True, 'scope': 'Artifact attribution and recorded-result checks only; no native rerun.'}
(Path(__file__).parent / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
