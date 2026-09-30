from pathlib import Path
import subprocess,os,shutil,json,hashlib,struct,re
out=Path('C:/runtime-readiness-v3');out.mkdir(exist_ok=False)
batch=out/'env.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" amd64 >nul\nset\n')
r=subprocess.run(['cmd','/d','/c',str(batch)],stdout=subprocess.PIPE,check=True);env={}
for line in r.stdout.decode(errors='replace').splitlines():
 if '=' in line:
  k,v=line.split('=',1);env[k]=v
path=next(v for k,v in env.items() if k.lower()=='path');dump=shutil.which('dumpbin.exe',path=path);assert dump
root=Path('C:/integration-current-v2/workspace/repo');files=[]
for folder in ['src/compile/x64','src/compile/deps/parsers-v120/x64','dev/x64']:
 files.extend((root/folder).rglob('*.dll'))
# Include direct vendor files loaded by name separately, never classify them as compiled outputs.
for name in ['binkw32.dll','vivoxsdk.dll','mss32.dll']:
 files.extend(root.glob('src/external/**/'+name))
rows=[]
def peinfo(p):
 data=p.read_bytes();off=struct.unpack_from('<I',data,0x3c)[0];assert data[off:off+4]==b'PE\0\0';machine=struct.unpack_from('<H',data,off+4)[0];return data,machine
for i,p in enumerate(sorted(set(files))):
 data,machine=peinfo(p);name=str(i).zfill(3)+'-'+p.name;cmd=[dump,'/nologo','/headers','/imports','/dependents',str(p)];r=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/(name+'.txt')).write_bytes(r.stdout);text=r.stdout.decode(errors='replace');dlls=sorted(set(re.findall(r'^\s+([A-Za-z0-9_.-]+\.dll)\s*$',text,re.M)),key=str.lower)
 rows.append({'path':str(p),'relative_path':str(p.relative_to(root)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'machine_hex':hex(machine),'machine':'AMD64' if machine==0x8664 else 'I386' if machine==0x14c else 'other','dumpbin_exit':r.returncode,'imports_including_delay':dlls,'log':name+'.txt'})
(out/'inventory.json').write_text(json.dumps({'source_head':'49d0eeed4ddaa177d7a93ea396c37c3d9b9942da','dumpbin':dump,'files':rows},indent=2));print([(r['relative_path'],r['machine'],r['imports_including_delay']) for r in rows],flush=True)
