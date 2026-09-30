"""Parent attribution audit of the native26 compile record, not a native rerun."""
from pathlib import Path
import hashlib
import io
import json
import tarfile

root = Path(__file__).resolve().parent.parent
base = root / 'pipe-native26'
digest = lambda data: hashlib.sha256(data).hexdigest()

def check(value, label):
    if not value:
        raise RuntimeError(label)

allowed = {'.h', '.cpp', '.py', '.md', '.json', '.txt', '.log', '.cmd', '.rsp', '.tar', '.sha256', '.patch'}
def contents(data):
    result = {}
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers():
            p = Path(member.name)
            check(member.isfile() and not p.is_absolute() and '..' not in p.parts, member.name)
            check(member.name not in result and p.suffix in allowed and p.name.lower() != 'mss.h', member.name)
            value = archive.extractfile(member).read()
            check(not value.startswith((b'MZ', b'\x7fELF')), member.name)
            if p.suffix == '.tar':
                contents(value)
            result[member.name] = value
    return result

for name, expected in json.loads((base / 'FREEZE-v1.json').read_text()).items():
    check(digest((base / name).read_bytes()) == expected, 'freeze: ' + name)
source = json.loads((base / 'source-manifest.json').read_text())
source_files = contents((base / 'source-v1.tar').read_bytes())
for name, expected in source.items():
    check(digest(source_files[name]) == expected, 'composed source: ' + name)
packet = json.loads((base / 'packet-manifest-v1.json').read_text())
packet_files = contents((base / 'packet-v1.tar').read_bytes())
for name, expected in packet.items():
    check(digest(packet_files[name]) == expected, 'packet: ' + name)
receipt_path = base / 'evidence-native-v1/receipt.json'
receipt = json.loads(receipt_path.read_text())
check(receipt['passed'] and receipt['stable_inputs'] and receipt['no_binary_image_or_library_output'], 'receipt verdict')
check(not receipt['executed'] and not receipt['linked'], 'compile-only scope')
check(receipt['inputs_before'] == receipt['inputs_after'], 'source stability')
prefix = 'C:\\pipe-native26\\'
for name, expected in receipt['inputs_after'].items():
    check(name.startswith(prefix), name)
    relative = name[len(prefix):].replace('\\', '/')
    check(digest(source_files[relative]) == expected, 'native input: ' + relative)
check(len(receipt['groups']) == 2, 'two ABIs')
for group, architecture, machine, count in zip(receipt['groups'], ['x86', 'amd64'], [0x14c, 0x8664], [2, 6]):
    check(group['architecture'] == architecture, 'architecture order')
    check(group['discovery_exit'] == group['compile_exit'] == 0, 'actual exits')
    check(group['before'] == group['after'] and group['inputs_unchanged'], 'compile stability')
    check(group['expected_sdk_includes'] and not group['unrecorded_local_headers'], 'include discovery')
    sdk = {name: value for name, value in group['before']['headers'].items() if Path(name.replace('\\', '/')).name.lower() == 'mss.h'}
    check(len(sdk) == 1 and next(iter(sdk.values())) == '966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e', 'actual SDK header')
    check(len(group['objects']) == count and all(o['machine'] == machine for o in group['objects']), 'COFF objects')
    check(group['symbol_oracle'], 'symbol evidence')
result = {'scope': __doc__, 'passed': True, 'composed_source_files': len(source),
          'packet_files': len(packet), 'receipt_sha256': digest(receipt_path.read_bytes()),
          'object_counts': {'x86': 2, 'x64': 6}, 'objects_executed': False,
          'packet_sha256': digest((base / 'packet-v1.tar').read_bytes())}
(Path(__file__).parent / 'native26-attribution.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
