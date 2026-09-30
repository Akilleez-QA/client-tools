from pathlib import Path
import subprocess,json,re,hashlib
out=Path('C:/capture-win32-link-v1');out.mkdir(exist_ok=False);subprocess.run(['subst','Q:','C:/integration-current-v1/workspace'],check=True);rows=[];original=Path('C:/capture-win32-original.rsp').read_text()
for variant in ['baseline','candidate']:
 d=out/variant;d.mkdir();command=original
 for flag,name in [('OUT','SwgClient.exe'),('PDB','SwgClient.pdb'),('IMPLIB','SwgClient.lib')]:
  command,n=re.subn('/'+flag+':"[^"]+"','/'+flag+':"'+str(d/name).replace('\\','/')+'"',command,flags=re.I);assert n==1,(flag,n)
 if variant=='candidate':
  provider=Path('C:/capture-poll-candidate-v2/Debug-win32/clientUserInterface.lib');command,n=re.subn(r'(?<!\S)clientUserInterface\.lib(?!\S)','"'+str(provider).replace('\\','/')+'"',command);assert n==1
 command+='\n/VERBOSE:LIB /MAP:"'+str(d/'SwgClient.map')+'"';rsp=d/'link.rsp';rsp.write_text(command);batch=d/'link.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul\nif errorlevel 1 exit /b %errorlevel%\n"C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/link.exe" @"'+str(rsp)+'"\n');r=subprocess.run(['cmd','/d','/c',str(batch)],cwd='Q:/repo/src/game/client/application/SwgClient/build/win32',stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'link.log').write_bytes(r.stdout);rows.append(dict(variant=variant,exit=r.returncode));print(rows[-1],flush=True)
(out/'results.json').write_text(json.dumps(rows,indent=2))
