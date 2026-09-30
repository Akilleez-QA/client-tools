"""Freeze authored sources and existing helpers only; no SDK body or VM work."""
from pathlib import Path
import hashlib
import json
import tarfile

base = Path(__file__).resolve().parent
root = base.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


files = {str(p.relative_to(root)): p for p in base.iterdir()
         if p.is_file() and (p.suffix in ('.h', '.cpp', '.py', '.md') or
                            p.name in ('.gitignore', 'input-identities.json'))}
prior = json.loads((root / 'native-startup25/source-manifest.json').read_text())
for relative in ['backend-boundary24/ClientMiles.h',
                 'live-bridge-candidate/revision4-tools/build_receipt.py',
                 'live-bridge-candidate/revision4-tools/receipt.py']:
    path = root / relative
    if digest(path) != prior[relative]:
        raise RuntimeError('frozen dependency changed: ' + relative)
    files[relative] = path
manifest = {name: digest(path) for name, path in sorted(files.items())}
manifest_path = base / 'source-manifest.json'
with manifest_path.open('x') as stream:
    json.dump(manifest, stream, indent=2)
    stream.write('\n')
archive_path = base / 'source-v1.tar'
with tarfile.open(archive_path, 'x') as archive:
    for name, path in sorted(files.items()):
        archive.add(path, arcname=name, recursive=False)
    archive.add(manifest_path, arcname='native-sample27/source-manifest.json', recursive=False)
print(json.dumps({'members': len(manifest), 'source_sha256': digest(archive_path),
                  'manifest_sha256': digest(manifest_path)}, indent=2))
