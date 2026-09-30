from pathlib import Path
import subprocess,json,re,hashlib
out=Path('C:/stl-selection-link-v2');out.mkdir(exist_ok=False);subprocess.run(['subst','R:','C:/integration-current-v2/workspace'],check=True);root=Path('R:/repo');project=root/'src/game/client/application/SwgClient/build/win32';rows=[]
for cfg,suffix in [('Release','r'),('Debug','d')]:
 d=out/cfg;d.mkdir();lines=Path('C:/integration-incremental-v3/results',cfg+'.log').read_text(errors='replace').splitlines();matches=[i for i,l in enumerate(lines) if 'link.exe /ERRORREPORT:QUEUE /OUT:' in l and 'SwgClient_'+suffix+'.exe' in l];assert len(matches)==1
 i=matches[0];command=lines[i].strip();exe,command=command.split('link.exe ',1);link=exe+'link.exe';i+=1
 while i<len(lines) and lines[i].strip().startswith('"'):
  command+='\n'+lines[i].strip();i+=1
 (d/'original.rsp').write_text(command)
 assert command.count(' stlport_vc71_stldebug_static.lib ')==1
 command=command.replace(' stlport_vc71_stldebug_static.lib ',' ')
 for flag,name in [('OUT','SwgClient.exe'),('PDB','SwgClient.pdb'),('IMPLIB','SwgClient.lib')]:
  command,n=re.subn('/'+flag+':"[^"]+"','/'+flag+':"'+str(d/name).replace('\\','/')+'"',command,flags=re.I);assert n==1,(flag,n)
 provider=root/'src/compile/deps/v120/x64'/cfg/'stlport.lib';assert provider.is_file()
 command+='\n"'+str(provider)+'" /NODEFAULTLIB:stlport_vc71_static.lib /VERBOSE:LIB /MAP:"'+str(d/'SwgClient.map')+'"'
 rsp=d/'candidate.rsp';rsp.write_text(command)
 batch=d/'link.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86_amd64 >nul\nif errorlevel 1 exit /b %errorlevel%\n"'+link+'" @"'+str(rsp)+'"\n')
 r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'link.log').write_bytes(r.stdout)
 row=dict(configuration=cfg,exit=r.returncode,provider=str(provider),provider_sha256=hashlib.sha256(provider.read_bytes()).hexdigest());rows.append(row);print(row,flush=True)
(out/'results.json').write_text(json.dumps(rows,indent=2))
