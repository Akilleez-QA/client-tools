$ErrorActionPreference = 'Stop'
$stage = @'
from pathlib import Path
import hashlib, tarfile
root=Path('C:/native-stream28')
archive=root/'source-v1.tar'
if hashlib.sha256(archive.read_bytes()).hexdigest() != '6055b9c780cdaf90d5ce152989a4f6b5abab6520c364b9bee7425556cb809cd9':
    raise RuntimeError('archive identity mismatch')
with tarfile.open(archive) as t:
    members=t.getmembers()
    if len(members)!=17:
        raise RuntimeError('unexpected member count')
    for m in members:
        if not m.isfile() or Path(m.name).is_absolute() or '..' in Path(m.name).parts:
            raise RuntimeError('unsafe member')
        if (root/m.name).exists():
            raise RuntimeError('source already staged')
    t.extractall(root)
manifest=root/'native-stream28/source-manifest.json'
if hashlib.sha256(manifest.read_bytes()).hexdigest() != '087ca6c4241d1ce36122f022f6f383b702510a5ac7175d0529c70d6486865aba':
    raise RuntimeError('manifest identity mismatch')
print('Exact archive and manifest verified before first native gate')
'@
& 'C:/ci-dpvs-review/python/python.exe' -c $stage
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& 'C:/ci-dpvs-review/python/python.exe' 'C:/native-stream28/native-stream28/build-native.py' --approved-compile-only
exit $LASTEXITCODE
