"""Attribute file26's frozen source and portable evidence, without rerunning callbacks."""
from pathlib import Path
import hashlib
import json
import tarfile

root = Path(__file__).resolve().parent.parent
base = root / 'file-channel26'
sha = lambda value: hashlib.sha256(value).hexdigest()
def check(value, message):
    if not value:
        raise RuntimeError(message)

source = json.loads((base / 'source-manifest.json').read_text())
with tarfile.open(base / 'source-v1.tar') as archive:
    for member in archive.getmembers():
        path = Path(member.name)
        check(member.isfile() and not path.is_absolute() and '..' not in path.parts, member.name)
        check(path.suffix in {'.h', '.cpp', '.py', '.json', '.md'} or path.name == '.gitignore', member.name)
        check(path.name.lower() != 'mss.h', member.name)
        data = archive.extractfile(member).read()
        check(not data.startswith((b'MZ', b'\x7fELF')), member.name)
        if member.name in source:
            check(sha(data) == source[member.name] == sha((root / member.name).read_bytes()), member.name)
frozen_cpp = (base / 'file_channel.cpp').read_bytes()
check(sha(frozen_cpp) == '0c5253d7f2a3a7b06ba54af756f170eca6c5f3b84fbbdce952a5700de6a64e27', 'source frozen for review')
check(b'result.bytes.resize(operation.count() ? operation.count() : 1)' in frozen_cpp, 'nonnull zero-count storage')
receipt = json.loads((base / 'evidence-v1/results.json').read_text())
check(not receipt.get('failure') and receipt['inputs_unchanged'], 'portable verdict')
check(receipt['inputs_before'] == receipt['inputs_after'], 'input stability')
for path, expected in receipt['inputs_after'].items():
    check(sha(Path(path).read_bytes()) == expected, 'input: ' + path)
for field in ('build_exit', 'run_exit', 'canonical_compile_exit', 'symbols_exit'):
    check(receipt[field] == 0, field)
check(not receipt['canonical_linked_or_executed'], 'canonical scope')
symbols = (base / 'evidence-v1/canonical-symbols.log').read_text()
for operation in ('open', 'close', 'seek', 'read'):
    check('ClientAudioFileCallbacks::' + operation + '(' in symbols, 'unresolved real service')
packet = json.loads((base / 'packet-manifest.json').read_text())
with tarfile.open(base / 'packet-v1.tar') as archive:
    for member in archive.getmembers():
        path = Path(member.name)
        check(member.isfile() and not path.is_absolute() and '..' not in path.parts, member.name)
        check(path.suffix in {'.h', '.cpp', '.py', '.json', '.md', '.log', '.yaml'} or path.name == '.gitignore', member.name)
        data = archive.extractfile(member).read()
        check(not data.startswith((b'MZ', b'\x7fELF')) and path.name.lower() != 'mss.h', member.name)
        if member.name in packet:
            item = packet[member.name]
            check(len(data) == item['bytes'] and sha(data) == item['sha256'], 'packet member: ' + member.name)
result = {'passed': True, 'scope': __doc__, 'source_files': len(source), 'packet_files': len(packet),
          'receipt_sha256': sha((base / 'evidence-v1/results.json').read_bytes()),
          'correction': 'Parent inspected an in-progress nullable-zero version before worker freeze. Frozen26 already contains nonnull zero-count staging. Only missing explicit test discrimination remained.',
          'audit_history': 'First two attribution invocations rejected authored .gitignore and CONTINUATION.yaml extensions. Allowlist corrected; candidate and recorded tests unchanged.'}
(Path(__file__).parent / 'file26-attribution.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
