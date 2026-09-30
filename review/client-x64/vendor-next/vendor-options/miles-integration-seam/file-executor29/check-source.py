#!/usr/bin/env python3
"""Static source identity and patch applicability only. Never compile/run C++."""
from pathlib import Path
import hashlib, json, re, shutil, subprocess, tempfile
ROOT=Path(__file__).resolve().parent
PRODUCT=Path('/home/akilleez/Work/swg-source/client-build-next')
AUDIO='src/engine/client/library/clientAudio/src/win32/Audio.cpp'
HEADER='src/engine/client/library/clientAudio/src/win32/ClientAudioFileCallbacks.h'
PUBLIC='src/engine/client/library/clientAudio/include/public/clientAudio/ClientAudioFileCallbacks.h'
manifest=json.loads((ROOT/'source-manifest.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for name,digest in manifest['sha256'].items(): assert sha(ROOT/name)==digest,name
assert subprocess.check_output(['git','-C',str(PRODUCT),'rev-parse','HEAD']).decode().strip()==manifest['product_commit']
assert sha(PRODUCT/AUDIO)==manifest['original_audio_sha256']
base=(ROOT/'baseline'/AUDIO).read_text()
old=(ROOT/'seam20'/AUDIO).read_text()
new=(ROOT/'candidate'/AUDIO).read_text()
TLS='\tif (once && !Os::isMainThread())\n\t{\n\t\tonce = false;\n\t\tPerThreadData::threadInstall(false);\n\t}\n\n'
comment='// Shared file operations only. Callers own TLS admission and serialization.\n'
delimiter='\n//-----------------------------------------------------------------------------'
def extract(text,signature):
    start=text.index(signature,text.index('static int once = true;'))
    end=text.index(delimiter,start)
    return text[start:end]
restored=new
bodies={}
for stem,result,args in [('Open','U32','fileName, fileHandle'),('Close','void','fileHandle'),('Seek','S32','fileHandle, offset, type'),('Read','U32','fileHandle, buffer, bytes')]:
    sdk='file'+stem+'CallBack'; common='file'+stem+'Common'
    original=extract(base,result+' __stdcall '+sdk+'(')
    assert original==extract(old,result+' __stdcall '+sdk+'(')
    sig,remainder=original.split('\n{\n',1)
    prefix,body=remainder.split(TLS)
    common_sig='static '+sig.replace('__stdcall ','').replace(sdk,common)
    actual_common=extract(new,common_sig)
    assert actual_common==common_sig+'\n{\n'+body,stem+' operation changed'
    invoke=('\t' if result=='void' else '\treturn ')+common+'('+args+');\n}\n'
    actual_sdk=extract(new,result+' __stdcall '+sdk+'(')
    assert actual_sdk==sig+'\n{\n'+prefix+TLS+invoke,stem+' native prologue changed'
    whole=comment+actual_common+delimiter+'\n'+actual_sdk
    assert restored.count(whole)==1
    restored=restored.replace(whole,original)
    adapter_start=restored.index('ClientAudioFileCallbacks::OpenResult ClientAudioFileCallbacks::open')
    restored=restored[:adapter_start]+restored[adapter_start:].replace(common+'(',sdk+'(')
    bodies[stem]={'identical_operation_body':True,'identical_native_prefix_and_TLS':True}
restored=restored.replace('// the shared operation bodies and their single AudioNamespace file map.\n// Admission guarantees installed engine TLS; these calls bypass legacy TLS setup.', '// the original callback bodies and their single AudioNamespace file map.')
assert restored==old,'Unrelated Audio source changed'
assert new.count(TLS)==4
assert new.count('static int once = true;')==1
assert 'isThreadInstalled' not in new
assert 'AIL_set_file_callbacks(fileOpenCallBack, fileCloseCallBack, fileSeekCallBack, fileReadCallBack);' in new
header=(ROOT/'candidate'/HEADER).read_text()
old_header=(ROOT/'seam20'/HEADER).read_text()
def without_comments(s): return '\n'.join(line.split('//',1)[0].rstrip() for line in s.splitlines() if line.split('//',1)[0].strip())
assert without_comments(header)==without_comments(old_header),'Public declarations changed'
assert re.findall(r'^#include (.*)$',header,re.M)==['<stdint.h>']
assert (ROOT/'candidate'/PUBLIC).read_bytes()==(ROOT/'seam20'/PUBLIC).read_bytes()
assert (ROOT/'ClientAudioFileCallbacks.h').read_text()==header
patch_checks=[]
for patch,folder in [('Audio-file-executor.patch','baseline'),('Audio-file-executor-from-seam20.patch','seam20')]:
    with tempfile.TemporaryDirectory(prefix='file-executor29-source-') as scratch:
        scratch=Path(scratch)
        shutil.copytree(ROOT/folder,scratch,dirs_exist_ok=True)
        subprocess.run(['git','apply','--check',str(ROOT/patch)],cwd=scratch,check=True)
        subprocess.run(['git','apply',str(ROOT/patch)],cwd=scratch,check=True)
        for path in [AUDIO,HEADER,PUBLIC]: assert (scratch/path).read_bytes()==(ROOT/'candidate'/path).read_bytes()
        patch_checks.append({'patch':patch,'applies_and_reconstructs_candidate':True})
subprocess.run(['git','-C',str(PRODUCT),'apply','--check',str(ROOT/'Audio-file-executor.patch')],check=True)
assert sha(PRODUCT/AUDIO)==manifest['original_audio_sha256']
report={'status':'static-source-checks-passed','body_checks':bodies,'unrelated_audio_source_unchanged':True,'sdk_registration_unchanged':True,'header_declarations_unchanged_vendor_free':True,'patch_checks':patch_checks,'product_unmodified_by_check':True,'compiler_run':False,'runtime_run':False}
(ROOT/'static-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
