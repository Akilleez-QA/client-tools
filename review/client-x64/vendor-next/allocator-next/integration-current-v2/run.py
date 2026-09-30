from pathlib import Path
import json,subprocess,tarfile,time,re,hashlib,os
base=Path('C:/integration-current-v2');base.mkdir(exist_ok=False);space=base/'workspace';space.mkdir();root=Path('R:/repo');out=base/'results';out.mkdir()
if Path('R:/').exists():raise RuntimeError('Q already exists; do not reuse')
subprocess.run(['subst','R:',str(space)],check=True)
root.mkdir()
with tarfile.open('C:/integration-current-v2-candidate.tar') as t:t.extractall(root,filter='data')
record=json.loads(Path('C:/integration-current-v2-snapshot.json').read_text())
for f in record['files']:
 if hashlib.sha256((root/f['path']).read_bytes()).hexdigest()!=f['sha256']:raise RuntimeError('Snapshot mismatch: '+f['path'])
(out/'snapshot.json').write_text(json.dumps(record,indent=2))
ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';projects=json.loads(Path('C:/integration-current-v2-projects.json').read_text())
target=base/'audit.targets';target.write_text('''<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003"><ItemGroup><Link Include="__audit"/><Lib Include="__audit"/><PostBuildEvent Include="__audit"/></ItemGroup><Target Name="SwgAudit"><Message Importance="High" Text="GLOBAL|$(OutDir)|$(IntDir)|$(TargetPath)"/><Message Importance="High" Text="LINK|%(Link.OutputFile)|%(Link.ImportLibrary)|%(Link.ProgramDatabaseFile)"/><Message Importance="High" Text="LIB|%(Lib.OutputFile)"/><Message Importance="High" Text="POST|%(PostBuildEvent.Command)"/></Target></Project>''')
common=['/p:DXSDK_DIR=C:/SDKs/DXSDK','/p:SwgJpegArchive=C:/allocator-next/jpegsrc.v6b.tar.gz','/p:SwgPythonExecutable=C:/ci-dpvs-review/python/python.exe','/nologo']
audits=[]
for cfg in ['Release','Debug']:
 for platform in ['x64']:
  for project in projects:
   cmd=[ms,str(root/project),'/t:SwgAudit','/p:Configuration='+cfg,'/p:Platform='+platform,'/p:ForceImportAfterCppTargets='+str(target),'/v:minimal']+common
   rr=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);text=rr.stdout.decode(errors='replace');name=Path(project).stem+'-'+cfg+'-'+platform;(out/(name+'.audit.log')).write_bytes(rr.stdout)
   if rr.returncode:raise RuntimeError('Audit failed '+name)
   outputs=[]
   for line in text.splitlines():
    line=line.strip()
    if line.startswith(('GLOBAL|','LINK|','LIB|')):
     for p in line.split('|')[1:]:
      if not p or '%' in p or '$(' in p:continue
      resolved=Path(os.path.abspath(root/Path(project).parent/p)) if not Path(p).is_absolute() else Path(p)
      if not str(resolved).lower().startswith(('r:','c:\\integration-current-v2\\')):raise RuntimeError('Unisolated output '+name+' '+str(resolved))
      outputs.append(str(resolved))
    elif line.startswith('POST|') and re.search(r'(?i)[cdef]:[\\/]',line):raise RuntimeError('Review explicit postbuild destination '+name+' '+line)
   audits.append(dict(name=name,outputs=outputs))
(out/'audit.json').write_text(json.dumps(audits,indent=2));print('Output audits passed',len(audits),flush=True)
results=[]
for cfg in ['Release','Debug']:
 for platform in ['x64']:
  name=cfg+'-'+platform;cmd=[ms,str(root/'src/build/win32/swg.sln'),'/t:SwgClient','/p:Configuration='+cfg,'/p:Platform='+platform,'/m:2','/v:normal']+common
  (out/(name+'.cmd.json')).write_text(json.dumps(cmd,indent=2));t=time.time()
  with (out/(name+'.log')).open('w') as f:r=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
  lines=(out/(name+'.log')).read_text(errors='replace').splitlines();errors=sorted(set(l.strip() for l in lines if re.search(r'(?:fatal )?error [A-Z]+\d+',l)))
  (out/(name+'.errors.txt')).write_text('\n'.join(errors));results.append(dict(name=name,exit=r.returncode,seconds=time.time()-t,unique_error_lines=len(errors)));(out/'results.json').write_text(json.dumps(results,indent=2));print(results[-1],flush=True)
