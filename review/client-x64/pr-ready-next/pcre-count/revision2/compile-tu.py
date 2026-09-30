from pathlib import Path
import subprocess,re,json,hashlib,sys
root=Path('C:/pr-pcre18-tu');root.mkdir(exist_ok=True);results=[]
for platform,arch,workspace in [('x64','amd64','C:/integration-current-v2/workspace/repo'),('win32','x86','C:/integration-current-v1/workspace/repo')]:
 for cfg in ['Release','Debug']:
  out=root/(platform+'-'+cfg);out.mkdir(exist_ok=True)
  repo=Path(workspace);search=repo/'src/compile'/platform/'swgClientUserInterface'/cfg
  files=list(search.rglob('*.tlog'));command=None
  for f in files:
   if f.name.lower()!='cl.command.1.tlog':continue
   lines=f.read_text(encoding='utf-16').splitlines()
   for i,line in enumerate(lines[:-1]):
    if line.startswith('^') and line.upper().endswith('SWGCUICOMMANDPARSERSCENE.CPP'):
     command=lines[i+1];original=line[1:];break
   if command:break
  if not command:results.append(dict(platform=platform,cfg=cfg,error='metadata absent'));continue
  command=command.replace(original,'C:/pr-pcre18-revision2/src/game/client/library/swgClientUserInterface/src/shared/parser/SwgCuiCommandParserScene.cpp')
  command=re.sub(r'/F[od]"[^"]*"','',command,flags=re.I)
  command+= ' /Y- /showIncludes /Fo"'+str(out/'scene.obj')+'" /Fd"'+str(out/'scene.pdb')+'" /I"'+str(repo/'src/game/client/library/swgClientUserInterface/src/shared/parser')+'"'
  rsp=out/'compile.rsp';rsp.write_text(command)
  batch=out/'compile.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\nif errorlevel 1 exit /b 1\ncl @"'+str(rsp)+'"\n')
  r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=repo/'src/game/client/library/swgClientUserInterface/build/win32',capture_output=True,timeout=120);(out/'compile.log').write_bytes(r.stdout+r.stderr)
  results.append(dict(platform=platform,cfg=cfg,exit=r.returncode,tlog=str(f), tlog_sha256=hashlib.sha256(f.read_bytes()).hexdigest(), source_sha256=hashlib.sha256(Path('C:/pr-pcre18-revision2/src/game/client/library/swgClientUserInterface/src/shared/parser/SwgCuiCommandParserScene.cpp').read_bytes()).hexdigest()))
(root/'results.json').write_text(json.dumps(results,indent=2))

sys.exit(0 if len(results)==4 and all(x.get("exit")==0 for x in results) else 1)
