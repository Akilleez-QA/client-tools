#!/usr/bin/env python3
"""Local private input preparation only; never VM/compiler/runtime."""
from pathlib import Path
import hashlib,json,shutil,subprocess
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
OLD=BASE/'file-executor29/native-inputs'
PRODUCT=Path('/home/akilleez/Work/swg-source/client-build-next')
OUT=ROOT/'native-inputs'
COMMIT='49d0eeed4ddaa177d7a93ea396c37c3d9b9942da'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert subprocess.check_output(['git','-C',str(PRODUCT),'rev-parse','HEAD']).decode().strip()==COMMIT
assert not subprocess.check_output(['git','-C',str(PRODUCT),'status','--porcelain=v1'])
old=json.loads((OLD/'input-manifest.json').read_text())
assert sha(OLD/'input-manifest.json')=='a02c162efe3dfd320f50cc4e0d8f56f236b99d770904c3c22e988e5dc48b135d'
for name,expected in old['sha256'].items():
 assert sha(OLD/name)==expected,name
 if name.startswith('snapshot/'):assert sha(PRODUCT/name[len('snapshot/'):])==expected,name
frozen=json.loads((BASE/'file-executor30/source-manifest.json').read_text())
for name,expected in frozen['sha256'].items():assert sha(BASE/'file-executor30'/name)==expected,name
OUT.mkdir(exist_ok=False)
shutil.copytree(OLD/'snapshot',OUT/'snapshot')
shutil.copytree(OLD/'inputs',OUT/'inputs')
paths=['file-executor31/EngineFileWorker.h','file-executor31/EngineFileWorker.cpp','file-executor31/FileInvocationJob.h','file-executor31/FileInvocationJob.cpp','file-channel26/file_channel.h','file-channel26/file_channel.cpp','file-channel26/canonical_services.cpp','transport-candidate/codec.h','transport-candidate/codec.cpp','transport-candidate/resource_registry.h','protocol-candidate/miles_wire.h','reverse-file-seam20/ClientAudioFileCallbacks.h']
for name in paths:
 target=OUT/'seam'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(BASE/name,target)
shutil.copyfile(ROOT/'run-native.py',OUT/'run-native.py')
m={'product_head':COMMIT,'predecessor30_manifest_sha256':sha(BASE/'file-executor30/source-manifest.json'),'sha256':{}}
for path in sorted(OUT.rglob('*')):
 if path.is_file():m['sha256'][str(path.relative_to(OUT))]=sha(path)
(OUT/'input-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'manifest_sha256':sha(OUT/'input-manifest.json'),'runner_sha256':sha(OUT/'run-native.py'),'entries':len(m['sha256']),'compiler_run':False,'vm_contacted':False},indent=2))
