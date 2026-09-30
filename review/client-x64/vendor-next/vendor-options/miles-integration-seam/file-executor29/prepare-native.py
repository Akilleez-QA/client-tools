#!/usr/bin/env python3
"""Optional AFTER scope review: prepare immutable local compile inputs only.
Does not contact a VM or invoke any compiler. Refuses an existing destination.
"""
from pathlib import Path
import hashlib, json, shutil
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'reverse-file-seam20/native-v120/staging'
PRODUCT=Path('/home/akilleez/Work/swg-source/client-build-next')
OUT=ROOT/'native-inputs'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
old=json.loads((OLD/'input-manifest.json').read_text())
source=json.loads((ROOT/'source-manifest.json').read_text())
assert old['product_head']==source['product_commit']
for relative,expected in old['sha256'].items():
    assert sha(OLD/relative)==expected,relative
    if relative.startswith('snapshot/'):
        assert sha(PRODUCT/relative[len('snapshot/'):])==expected,'Product snapshot drift: '+relative
for relative,expected in source['sha256'].items(): assert sha(ROOT/relative)==expected,relative
OUT.mkdir(exist_ok=False)
shutil.copytree(OLD/'snapshot',OUT/'snapshot')
shutil.copytree(OLD/'inputs',OUT/'inputs')
shutil.copytree(ROOT/'candidate',OUT/'candidate')
shutil.copyfile(ROOT/'run-native.py',OUT/'run-native.py')
manifest={'product_head':source['product_commit'],'source_root':str(PRODUCT),'patch_sha256':sha(ROOT/'Audio-file-executor.patch'),'sha256':{}}
for path in sorted(OUT.rglob('*')):
    if path.is_file(): manifest['sha256'][str(path.relative_to(OUT))]=sha(path)
(OUT/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Prepared local inputs only at '+str(OUT)+'; compiler and VM not invoked.')
