"""Check frozen inputs, applied overlay, and receipt attribution; no vendor run."""
from pathlib import Path
import hashlib
import io
import json
import tarfile

root = Path(__file__).resolve().parent.parent
base = root / 'pipe-startup26'
digest = lambda b: hashlib.sha256(b).hexdigest()

def check(condition, label):
    if not condition:
        raise RuntimeError(label)

freeze = json.loads((base / 'FREEZE-v1.json').read_text())
for name, expected in freeze.items():
    check(digest((base / name).read_bytes()) == expected, 'freeze: ' + name)
source = json.loads((base / 'source-manifest.json').read_text())
for name, expected in source.items():
    check(digest((root / name).read_bytes()) == expected, 'source: ' + name)
packet = json.loads((base / 'packet-manifest.json').read_text())
for name, expected in packet.items():
    check(digest((root / name).read_bytes()) == expected, 'packet: ' + name)
allowed = {'.h', '.cpp', '.py', '.md', '.json', '.yaml', '.txt', '.log', '.cmd', '.rsp', '.tar', '.sha256', '.patch'}

def audit_archive(data, expected=None):
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        members = archive.getmembers()
        check(len({m.name for m in members}) == len(members), 'duplicate archive member')
        hashes = {}
        for member in members:
            p = Path(member.name)
            check(member.isfile() and not p.is_absolute() and '..' not in p.parts, member.name)
            check(p.name.lower() != 'mss.h' and p.suffix in allowed, member.name)
            content = archive.extractfile(member).read()
            check(not content.startswith((b'MZ', b'\x7fELF')), 'executable: ' + member.name)
            hashes[member.name] = digest(content)
            if p.suffix == '.tar':
                audit_archive(content)
        if expected is not None:
            for name, value in expected.items():
                check(hashes.get(name) == value, 'archive identity: ' + name)
        return len(members)

archives = {}
for name, manifest in [('source-v1.tar', source), ('packet-v1.tar', packet)]:
    content = (base / name).read_bytes()
    archives[name] = {'sha256': digest(content), 'members': audit_archive(content, manifest)}
receipt = json.loads((base / 'evidence-portable-v2/receipt.json').read_text())
check(receipt['passed'] and receipt['original_inputs_unchanged'], 'recorded portable verdict')
check(not receipt['vendor_execution'] and not receipt['native_execution'], 'scope')
check(receipt['authored_before'] == receipt['authored_after'], 'builder/patch stability')
for name, expected in receipt['staged_sources'].items():
    check(digest((base / 'private-stage-v2' / name).read_bytes()) == expected, 'overlay: ' + name)
check(receipt['seven_stdout'] == 'PASS 1267 scripted-framed checks; no vendor execution\n', 'mapping check count')
check('202' in receipt['baseline_stdout'], 'baseline check count')
check(receipt['callbacks_unimplemented_link_exit'] != 0, 'callback negative link')
result = {'scope': 'Parent attribution/source audit only. Portable receipt is reported execution, not an independent run.',
          'passed': True, 'frozen_sources': len(source), 'packet_files': len(packet),
          'applied_sources': len(receipt['staged_sources']), 'archives': archives,
          'receipt_sha256': digest((base / 'evidence-portable-v2/receipt.json').read_bytes())}
(Path(__file__).parent / 'pipe26-attribution.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
