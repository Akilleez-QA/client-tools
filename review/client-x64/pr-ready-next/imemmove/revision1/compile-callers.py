from pathlib import Path
import subprocess,re,json,hashlib,sys
root=Path('C:/pr-imemmove18-v1');rows=[]
units=[('sharedFoundation','src/engine/shared/library/sharedFoundation','src/shared/Md5.cpp'),('sharedFile','src/engine/shared/library/sharedFile','src/shared/Iff.cpp'),('clientGame','src/engine/client/library/clientGame','src/shared/HTTPpost/TCPQueue.cpp')]
for platform,arch,workspace in [('x64','amd64','C:/integration-current-v2/workspace/repo'),('win32','x86','C:/integration-current-v1/workspace/repo')]:
 for cfg in ['Release','Debug']:
  for project,folder,source in units:
   out=root/'caller-results'/(platform+'-'+cfg+'-'+project);out.mkdir(parents=True,exist_ok=False);repo=Path(workspace);command=None
   for f in (repo/'src/compile'/platform/project/cfg).rglob('cl.command.1.tlog'):
    lines=f.read_text(encoding='utf-16').splitlines()
    for i,line in enumerate(lines[:-1]):
     if line.startswith('^') and line.upper().endswith(Path(source).name.upper()):command=lines[i+1];original=line[1:];break
    if command:break
   row=dict(platform=platform,configuration=cfg,project=project);rows.append(row)
   if not command:row['error']='metadata absent';continue
   candidate=root/'candidate'/folder/source
   command=command.replace(original,str(candidate));command=re.sub(r'/F[od]"[^"]*"','',command,flags=re.I)
   command+=' /Y- /showIncludes /Fo"'+str(out/'caller.obj')+'" /Fd"'+str(out/'caller.pdb')+'" /I"'+str(repo/folder/Path(source).parent)+'"'
   rsp=out/'compile.rsp';rsp.write_text(command)
   row.update(source_sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),metadata_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),metadata=str(f))
   batch=out/'compile.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\nif errorlevel 1 exit /b 1\ncl @"'+str(rsp)+'"\n')
   x=subprocess.run(['cmd','/d','/c',str(batch)],cwd=repo/folder/'build/win32',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120);(out/'build.log').write_bytes(x.stdout);row['exit']=x.returncode
(root/'caller-results.json').write_text(json.dumps(rows,indent=2));sys.exit(0 if all(x.get('exit')==0 for x in rows) else 1)
