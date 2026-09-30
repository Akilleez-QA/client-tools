from pathlib import Path
import subprocess,json,tarfile
out=Path('C:/stl-props-target-v1');out.mkdir(exist_ok=False);subprocess.run(['subst','Q:','C:/integration-current-v1/workspace'],check=True);root=Path('Q:/repo');ms='C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe';rows=[]
with tarfile.open('C:/stl-target-input.tar') as t:t.extractall(out/'input',filter='data')
paths=[str(p.relative_to(out/'input')) for p in (out/'input').rglob('*') if p.is_file()];original={p:(root/p).read_bytes() if (root/p).exists() else None for p in paths}
try:
 for p in paths:(root/p).write_bytes((out/'input'/p).read_bytes())
 for run in ['fresh','cache']:
  cmd=[ms,str(root/'src/game/client/application/SwgClient/build/win32/SwgClient.vcxproj'),'/t:BuildSwgClientDependencies','/p:Configuration=Release','/p:Platform=x64','/p:SwgClientDepsDir='+str(out/'deps'),'/p:SwgJpegArchive=C:/allocator-next/jpegsrc.v6b.tar.gz','/p:SwgPythonExecutable=C:/ci-dpvs-review/python/python.exe','/v:normal','/nologo'];(out/(run+'.cmd.json')).write_text(json.dumps(cmd,indent=2));r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/(run+'.log')).write_bytes(r.stdout);rows.append(dict(run=run,exit=r.returncode));print(rows[-1],flush=True)
  if r.returncode:break
 (out/'results.json').write_text(json.dumps(rows,indent=2))
finally:
 for p,data in original.items():
  if data is None:(root/p).unlink(missing_ok=True)
  else:(root/p).write_bytes(data)
