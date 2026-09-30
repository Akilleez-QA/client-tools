"""Freeze authored source only; never stage/build/run on the VM."""
from pathlib import Path
import hashlib
import json
import shutil
import tarfile
BASE = Path(__file__).resolve().parent
SEAM = BASE.parent

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

native = SEAM / 'pipe-native26'
if digest(native / 'source-manifest.json') != '8a04b23fb0e7377fecba9557b0121ccc85313d2e84ac4c581ddfec92f52fa1de':
    raise RuntimeError('native26 frozen manifest changed')
prior = json.loads((native / 'source-manifest.json').read_text())
shared = ['transport-candidate/codec.cpp', 'transport-candidate/codec.h',
          'transport-candidate/resource_registry.h', 'protocol-candidate/miles_wire.h',
          'pipe-transport-candidate/endpoint.h',
          'live-bridge-candidate/common.h',
          'host-candidate/host_dispatch.cpp', 'host-candidate/host_dispatch.h',
          'host-candidate/registry_resolver.h',
          'startup-metadata-v4/metadata.h', 'startup-metadata-v4/metadata_wire.cpp',
          'session-version22/session_version.h', 'session-version22/session_version.cpp',
          'session-version22/session_version_host.h',
          'startup-bridge23/backend.h', 'startup-bridge23/reply.h',
          'backend-boundary24/ClientMiles.h', 'backend-boundary24/pipe/Channel.h',
          'backend-boundary24/pipe/Session.h', 'backend-boundary24/pipe/ClientMilesPipe.cpp',
          'backend-boundary24/pipe/LiveChannel.h', 'backend-boundary24/pipe/LiveChannel.cpp',
          'native-startup25/ClientMilesStartup.h',
          'live-bridge-candidate/revision4-tools/build_receipt.py',
          'live-bridge-candidate/revision4-tools/receipt.py']
mapping = {}
for name in shared:
    path = native / 'private-source-v1' / name
    if digest(path) != prior[name]:
        raise RuntimeError('composed native26 input changed: ' + name)
    mapping[name] = path
old = json.loads((SEAM / 'startup-bridge23/source-manifest.json').read_text())
for name in ['live-bridge-candidate/admission.h', 'coordinator-candidate/coordinator.h',
             'coordinator-candidate/coordinator.cpp', 'pipe-transport-candidate/endpoint.cpp',
             'startup-metadata-v4/metadata_host.cpp', 'session-version22/session_version_host.cpp']:
    path = SEAM / name
    if digest(path) != old[name]:
        raise RuntimeError('frozen23 admission input changed: ' + name)
    mapping[name] = path
for path in BASE.iterdir():
    if path.is_file() and path.suffix in ['.py', '.cpp', '.h', '.md', '.json'] and path.name != 'source-manifest.json':
        mapping['pipe-live27/' + path.name] = path
snapshot = BASE / 'private-source-v1'
snapshot.mkdir(exist_ok=False)
for name, path in mapping.items():
    target = snapshot / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
manifest = {name: digest(snapshot / name) for name in sorted(mapping)}
manifest_path = BASE / 'source-manifest.json'
with manifest_path.open('x') as stream:
    json.dump(manifest, stream, indent=2)
    stream.write('\n')
with tarfile.open(BASE / 'source-v1.tar', 'x') as archive:
    for name in sorted(mapping):
        archive.add(snapshot / name, arcname=name, recursive=False)
    archive.add(manifest_path, arcname='source-manifest.json', recursive=False)
print(json.dumps({'manifest': digest(manifest_path), 'source': digest(BASE / 'source-v1.tar'), 'files': len(manifest)}, indent=2))
