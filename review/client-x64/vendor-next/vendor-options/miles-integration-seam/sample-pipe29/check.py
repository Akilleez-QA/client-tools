"""Portable/scripted gate only; never loads a vendor or runs a native fixture."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import tarfile

root=Path(__file__).resolve().parent
base=root.parent
out=root/'evidence-v1'
out.mkdir(exist_ok=False)
stage=out/'stage'
stage.mkdir()
digest=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
inputs={str(p):digest(p) for p in root.rglob('*') if p.is_file() and out not in p.parents}
for path,expected in json.loads((root/'input-identities.json').read_text()).items():
    assert digest(path)==expected, path
    inputs[path]=expected
archive=base/'pipe-native26/source-v1.tar'
with tarfile.open(archive) as tar:
    for member in tar.getmembers():
        if not member.isfile():
            raise RuntimeError('non-file archive member')
        target=stage/member.name
        if not target.resolve().is_relative_to(stage.resolve()):
            raise RuntimeError('archive traversal')
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(tar.extractfile(member).read())
for folder,names in {
    'native-sample27':['ClientMilesSample.h','sample_time.h','sample_time.cpp'],
    'buffer-upload-candidate':['buffer_upload.h','buffer_upload.cpp'],
    'host-candidate':['retained_buffers.h','retained_buffers.cpp'],
}.items():
    for name in names:
        source=base/folder/name
        inputs[str(source)]=digest(source)
        (stage/folder).mkdir(exist_ok=True)
        shutil.copyfile(source,stage/folder/name)
(stage/'sample-pipe29').mkdir()
for name in ['client_test.cpp','prepared_input.h']:
    shutil.copyfile(root/name,stage/'sample-pipe29'/name)
compiler=Path(shutil.which('g++')).resolve()
receipt={'inputs_before':inputs,'compiler':str(compiler),'compiler_sha256':digest(compiler),
         'scope':'scripted existing Session/Channel; no actual vendor/engine/native runtime',
         'named_bind_implemented':False}
(out/'pretest-manifest.json').write_text(json.dumps(receipt,indent=2)+'\n')
def run(command,name):
    (out/(name+'-command.json')).write_text(json.dumps(command,indent=2)+'\n')
    p=subprocess.run(command,cwd=stage,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    (out/(name+'.log')).write_text(p.stdout)
    receipt[name+'_exit']=p.returncode
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return p
try:
    p=run(['patch','--batch','-p1','-i',str(root/'patches/01-owned-sample-client.patch')],'apply')
    assert p.returncode==0,'overlay application'
    sources=['sample-pipe29/client_test.cpp','backend-boundary24/pipe/ClientMilesPipe.cpp',
             'transport-candidate/codec.cpp','session-version22/session_version.cpp',
             'startup-metadata-v4/metadata_wire.cpp','buffer-upload-candidate/buffer_upload.cpp',
             'host-candidate/retained_buffers.cpp']
    flags=[str(compiler),'-std=c++11','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-g']
    p=run(flags+sources+['-o',str(out/'client-test')],'build')
    assert p.returncode==0,'portable build'
    p=run([str(out/'client-test')],'scripted')
    assert p.returncode==0 and p.stdout.startswith('PASS '),'scripted operations'
    receipt['scripted_output']=p.stdout
    p=run(flags+sources+['native-sample27/sample_time.cpp','-o',str(out/'must-not-link')],'missing-bind')
    assert p.returncode!=0 and 'set_named_sample_file' in p.stdout,'missing bind link control'
    receipt['passed']=True
finally:
    receipt['inputs_unchanged']=all(digest(path)==value for path,value in inputs.items())
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='inputs_before'},indent=2))
