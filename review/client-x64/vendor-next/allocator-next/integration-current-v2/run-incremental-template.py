# Fill versioned input filenames only after parent supplies an immutable commit.
from pathlib import Path
import subprocess,json,hashlib,tarfile,time,re
base=Path('C:/integration-incremental-v3');base.mkdir(exist_ok=False);out=base/'results';out.mkdir();root=Path('R:/repo');subprocess.run(['subst','R:','C:/integration-current-v2/workspace'],check=True)
previous=json.loads(Path('C:/integration-current-v2-snapshot.json').read_text())
for row in previous['files']:
 if hashlib.sha256((root/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise RuntimeError('Prior immutable source was modified: '+row['path'])
change=json.loads(Path('C:/integration-incremental-v3-manifest.json').read_text());(out/'manifest.json').write_text(json.dumps(change,indent=2))
if change['base']!=previous['head']:raise RuntimeError('Wrong source base')
with tarfile.open('C:/integration-incremental-v3.tar') as t:t.extractall(root,filter='data')
for path in change['deleted']:(root/path).unlink()
for row in change['files']:
 if hashlib.sha256((root/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise RuntimeError('Overlay mismatch: '+row['path'])
ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';results=[]
for cfg in ['Release','Debug']:
 cmd=[ms,str(root/'src/build/win32/swg.sln'),'/t:SwgClient','/p:Configuration='+cfg,'/p:Platform=x64','/p:DXSDK_DIR=C:/SDKs/DXSDK','/p:SwgJpegArchive=C:/allocator-next/jpegsrc.v6b.tar.gz','/p:SwgPythonExecutable=C:/ci-dpvs-review/python/python.exe','/m:2','/v:normal','/nologo'];(out/(cfg+'.cmd.json')).write_text(json.dumps(cmd,indent=2));start=time.time()
 with (out/(cfg+'.log')).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
 lines=(out/(cfg+'.log')).read_text(errors='replace').splitlines();errors=sorted(set(l.strip() for l in lines if re.search(r'(?:fatal )?error [A-Z]+\d+',l)));(out/(cfg+'.errors.txt')).write_text('\n'.join(errors));row=dict(configuration=cfg,exit=r.returncode,seconds=time.time()-start,diagnostic_lines_including_repeated_summary=len(errors));results.append(row);(out/'results.json').write_text(json.dumps(results,indent=2));print(row,flush=True)
