# Inputs are immutable Git manifests; no working-tree files enter this build.
from pathlib import Path
import subprocess,json,hashlib,tarfile,time,re
base=Path('C:/integration-current-head-v1');base.mkdir(exist_ok=False);out=base/'results';out.mkdir()
root=Path('R:/repo');subprocess.run(['subst','R:','C:/integration-current-v2/workspace'],check=True)
previous=json.loads(Path('C:/integration-current-v2-snapshot.json').read_text())
old_delta=json.loads(Path('C:/integration-incremental-v3-manifest.json').read_text())
expected={r['path']:r['sha256'] for r in previous['files']}
for p in old_delta['deleted']:expected.pop(p,None)
expected.update({r['path']:r['sha256'] for r in old_delta['files']})
for p,h in expected.items():
 if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h:raise RuntimeError('Previous source changed: '+p)
change=json.loads(Path('C:/integration-current-head-v1-manifest.json').read_text())
assert change['base']==old_delta['head']
(out/'manifest.json').write_text(json.dumps(change,indent=2))
with tarfile.open('C:/integration-current-head-v1.tar') as t:t.extractall(root,filter='data')
for p in change['deleted']:(root/p).unlink();expected.pop(p,None)
expected.update({r['path']:r['sha256'] for r in change['files']})
for p,h in expected.items():
 if hashlib.sha256((root/p).read_bytes()).hexdigest()!=h:raise RuntimeError('Current source mismatch: '+p)
(out/'source-verified.json').write_text(json.dumps({'head':change['head'],'tracked_files_checked':len(expected)},indent=2))
ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';results=[]
for plat,cfg in [('x64','Release'),('x64','Debug'),('Win32','Release'),('Win32','Debug')]:
 name=plat+'-'+cfg
 cmd=[ms,str(root/'src/build/win32/swg.sln'),'/t:SwgClient','/p:Configuration='+cfg,'/p:Platform='+plat,'/p:DXSDK_DIR=C:/SDKs/DXSDK','/p:SwgJpegArchive=C:/allocator-next/jpegsrc.v6b.tar.gz','/p:SwgPythonExecutable=C:/ci-dpvs-review/python/python.exe','/p:SwgLogitechLcdSdkDir=C:/lcd-props-eval-v1/LCDSDK','/p:SwgPcreArchive=C:/xml-pcre-next/pcre-4.1.tar.gz','/p:SwgLibxmlArchive=C:/xml-pcre-next/libxml2-2.6.7.tar.gz','/m:2','/v:normal','/nologo']
 (out/(name+'.command.json')).write_text(json.dumps(cmd,indent=2));start=time.time()
 with (out/(name+'.log')).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 text=(out/(name+'.log')).read_text(errors='replace');errors=sorted(set(l.strip() for l in text.splitlines() if re.search(r'(?:fatal )?error [A-Z]+\d+',l)));(out/(name+'.errors.txt')).write_text('\n'.join(errors))
 symbols=sorted(set(re.findall(r'unresolved external symbol (\S+)',text)))
 row=dict(platform=plat,configuration=cfg,exit=r.returncode,seconds=time.time()-start,error_lines=len(errors),unresolved_symbols=symbols,valid_build=(r.returncode==0 and not errors and not symbols and 'LNK4088' not in text));results.append(row);(out/'results.json').write_text(json.dumps(results,indent=2));print(row,flush=True)
