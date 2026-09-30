#!/usr/bin/env python3
"""Local preparation only; does not contact VM or invoke a compiler."""
from pathlib import Path
import hashlib,json,shutil,subprocess
D=Path(__file__).resolve().parent;BASE=D.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
frozen=json.loads((D/'source-manifest.json').read_text())
for n,v in frozen['sha256'].items():assert sha(D/n)==v,n
for n,v in frozen['inputs'].items():assert sha(BASE/n)==v,n
product=Path('/home/akilleez/Work/swg-source/client-build-next')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=product,text=True).strip()=='49d0eeed4ddaa177d7a93ea396c37c3d9b9942da'
assert not subprocess.check_output(['git','status','--porcelain'],cwd=product,text=True)
old=BASE/'file-executor33/native-inputs'
manifest=json.loads((old/'input-manifest.json').read_text())
for n,v in manifest['sha256'].items():assert sha(old/n)==v,n
out=D/'private-inputs-v1';out.mkdir(exist_ok=False)
# Snapshot is private; make independent copies so future writes cannot alter33.
shutil.copytree(old/'snapshot',out/'snapshot')
(out/'inputs').mkdir()
shutil.copy2(old/'inputs/clientAudio-Debug-x64.audit.log',out/'inputs')
(out/'seam/native-file-callbacks35').mkdir(parents=True)
for n in ['ClientMilesFileCallbacks.h','native_file_callbacks.cpp','engine_header_probe.cpp']:
 shutil.copy2(D/n,out/'seam/native-file-callbacks35'/n)
(out/'seam/file-executor29').mkdir()
shutil.copy2(BASE/'file-executor29/ClientAudioFileCallbacks.h',out/'seam/file-executor29')
shutil.copy2(D/'run-native35.py',out/'run-native35.py')
entries={str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file()}
(out/'input-manifest.json').write_text(json.dumps({'product_head':'49d0eeed4ddaa177d7a93ea396c37c3d9b9942da','sha256':entries},indent=2)+'\n')
print(json.dumps({'input_count':len(entries),'input_manifest_sha256':sha(out/'input-manifest.json'),'runner_sha256':sha(D/'run-native35.py'),'frozen_source_manifest_sha256':sha(D/'source-manifest.json')},indent=2))
