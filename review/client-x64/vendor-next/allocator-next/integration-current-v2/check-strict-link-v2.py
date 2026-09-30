from pathlib import Path
import subprocess,json,tarfile,re,html
out=Path('C:/strict-link-policy-v2');out.mkdir(exist_ok=False)
for drive,physical in [('Q:','C:/integration-current-v1/workspace'),('R:','C:/integration-current-v2/workspace')]:subprocess.run(['subst',drive,physical],check=True)
root=Path('Q:/repo');ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';proj=root/'src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj'
with tarfile.open('C:/strict-link-input.tar') as t:t.extractall(out/'input',filter='data')
paths=[str(p.relative_to(out/'input/candidate')) for p in (out/'input/candidate').rglob('*') if p.is_file()];original={p:(root/p).read_bytes() if (root/p).exists() else None for p in paths};rows=[]
try:
 for variant in ['baseline','candidate']:
  for p in paths:(root/p).write_bytes((out/'input'/variant/p).read_bytes())
  d=out/variant;d.mkdir();rsp=Path('C:/capture-cleanup-link-v1/Debug/candidate.rsp').read_text();rsp,n=re.subn(r'(?i)(?<!\S)/FORCE(?!\S)','',rsp);assert n==1
  for flag,name in [('OUT','SwgClient.exe'),('PDB','SwgClient.pdb'),('IMPLIB','SwgClient.lib'),('MAP','SwgClient.map')]:
   rsp,n=re.subn('/'+flag+':"[^"]+"','/'+flag+':"'+str(d/name).replace('\\','/')+'"',rsp,flags=re.I);assert n==1,(flag,n)
  rsp=re.sub(r'/LIBPATH:(\S+)',lambda m:'/LIBPATH:"'+str((Path('R:/repo/src/game/client/application/SwgClient/build/win32')/m.group(1)).resolve())+'"' if m.group(1).startswith('..') else m.group(0),rsp)
  match=re.findall(r'"([^"\n]*ClientMain\.obj)"',rsp);assert len(match)==1;source=match[0];rsp=rsp.replace('"'+source+'"','');(d/'inputs.rsp').write_text(rsp)
  target=d/'check.targets';target.write_text('<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup><Link Include="__audit"/></ItemGroup><Target Name="AuditForce"><Message Importance="High" Text="FORCE|%(Link.ForceFileOutput)"/></Target><Target Name="StrictRelink"><Link Sources="'+html.escape(source,quote=True)+'" ForceFileOutput="%(Link.ForceFileOutput)" AdditionalOptions="'+html.escape(rsp,quote=True)+'" ToolPath="C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/x86_amd64/" /></Target></Project>')
  for cfg,plat in [('Release','Win32'),('Debug','Win32'),('Release','x64'),('Debug','x64')]:
   cmd=[ms,str(proj),'/t:AuditForce','/p:Configuration='+cfg,'/p:Platform='+plat,'/p:ForceImportAfterCppTargets='+str(target),'/v:minimal','/nologo'];r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/(cfg+'-'+plat+'.log')).write_bytes(r.stdout);rows.append(dict(variant=variant,configuration=cfg,platform=plat,operation='metadata',exit=r.returncode))
  cmd='"'+ms+'" "'+str(proj)+'" /t:StrictRelink /p:Configuration=Debug /p:Platform=x64 /p:ForceImportAfterCppTargets="'+str(target)+'" /v:normal /nologo'
  batch=d/'run.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86_amd64 >nul\nif errorlevel 1 exit /b %errorlevel%\n'+cmd+'\n');r=subprocess.run(['cmd','/d','/c',str(batch)],cwd='R:/repo/src/game/client/application/SwgClient/build/win32',stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'native-link.log').write_bytes(r.stdout);rows.append(dict(variant=variant,operation='native Link task',exit=r.returncode));print(rows[-1],flush=True)
 (out/'results.json').write_text(json.dumps(rows,indent=2))
finally:
 for p,data in original.items():
  if data is None:(root/p).unlink(missing_ok=True)
  else:(root/p).write_bytes(data)
