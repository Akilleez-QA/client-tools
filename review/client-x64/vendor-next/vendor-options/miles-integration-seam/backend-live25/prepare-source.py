"""Freeze the selected source allowlist only. This script builds/runs no executable."""
from pathlib import Path
import hashlib
import json
import tarfile

base = Path(__file__).resolve().parent
root = base.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


shared = ['transport-candidate/codec.cpp', 'transport-candidate/codec.h',
          'transport-candidate/resource_registry.h', 'protocol-candidate/miles_wire.h',
          'pipe-transport-candidate/endpoint.cpp', 'pipe-transport-candidate/endpoint.h',
          'coordinator-candidate/coordinator.cpp', 'coordinator-candidate/coordinator.h',
          'live-bridge-candidate/common.h', 'live-bridge-candidate/admission.h',
          'host-candidate/host_dispatch.h', 'host-candidate/registry_resolver.h',
          'startup-metadata-v4/metadata.h', 'startup-metadata-v4/metadata_wire.cpp',
          'startup-metadata-v4/metadata_host.cpp', 'session-version22/session_version.h',
          'session-version22/session_version.cpp', 'session-version22/session_version_host.h',
          'session-version22/session_version_host.cpp', 'startup-bridge23/bridge.cpp',
          'startup-bridge23/backend.h', 'startup-bridge23/fixture.h', 'startup-bridge23/reply.h',
          'backend-boundary24/ClientMiles.h', 'backend-boundary24/pipe/Channel.h',
          'backend-boundary24/pipe/Session.h', 'backend-boundary24/pipe/ClientMilesPipe.cpp',
          'backend-boundary24/pipe/LiveChannel.h', 'backend-boundary24/pipe/LiveChannel.cpp',
          'backend-boundary24/sample/startup_calls.h', 'backend-boundary24/sample/startup_calls.cpp',
          'backend-boundary24/fixture/live_controller.cpp']
prior = {}
for name in ['startup-bridge23/source-manifest.json', 'backend-boundary24/source-manifest.json']:
    prior.update(json.loads((root / name).read_text()))
for name in shared:
    if name not in prior or digest(root / name) != prior[name]:
        raise RuntimeError('frozen source identity mismatch: ' + name)
mapping = {name: root / name for name in shared}
for path in base.iterdir():
    if path.suffix in ('.py', '.md') or path.name == '.gitignore':
        mapping['backend-live25/' + path.name] = path
for name in ['receipt.py', 'build_receipt.py']:
    logical = 'revision4-tools/' + name
    path = root / 'live-bridge-candidate/revision4-tools' / name
    if digest(path) != prior[logical]:
        raise RuntimeError('frozen helper identity mismatch: ' + logical)
    mapping[logical] = path
manifest = {name: digest(path) for name, path in sorted(mapping.items())}
manifest_path = base / 'source-manifest.json'
with manifest_path.open('x') as stream:
    json.dump(manifest, stream, indent=2)
    stream.write('\n')
archive_path = base / 'source-v1.tar'
with tarfile.open(archive_path, 'x') as archive:
    for name, path in sorted(mapping.items()):
        archive.add(path, arcname=name, recursive=False)
    archive.add(manifest_path, arcname='source-manifest.json', recursive=False)
print(json.dumps({'files': len(manifest), 'manifest_sha256': digest(manifest_path),
                  'source_archive_sha256': digest(archive_path)}, indent=2))
