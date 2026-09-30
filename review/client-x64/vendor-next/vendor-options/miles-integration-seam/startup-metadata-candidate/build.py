from pathlib import Path
import sys,subprocess,json,shutil,hashlib
root=Path('C:/startup-metadata-v2')
sys.path.insert(0,str(root/'live-bridge-candidate/revision4-tools'))
from build_receipt import environment,identities,includes,run,exclusive_json,LIB_NAMES
from receipt import digest,machine
out=root/'build';out.mkdir(exist_ok=False)
vc=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat');sdk=Path('C:/client-next-build/src/external/3rd/library/miles')
builder_before=digest(__file__)
records=[]
for config in ['Debug','Release']:
 for arch in ['x86','amd64']:
  for kind in (['wire','host'] if arch=='x86' else ['wire']):
   target=out/(arch+'-'+config+'-'+kind);target.mkdir();env=environment(vc,arch,target)
   cl=Path(shutil.which('cl.exe',path=env['PATH']));link=Path(shutil.which('link.exe',path=env['PATH']))
   source=['startup-metadata-candidate/metadata_wire.cpp','transport-candidate/codec.cpp','startup-metadata-candidate/'+('wire_test.cpp' if kind=='wire' else 'host_test.cpp')]
   if kind=='host':source+=['startup-metadata-candidate/metadata_host.cpp']
   flags=[str(cl),'/nologo','/W4','/WX','/EHsc','/DWIN32','/D_WIN32_WINNT=0x0601','/I'+str(sdk/'include'),'/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2']
   command=flags+[str(root/x) for x in source]
   code,log=run(command+['/Zs','/showIncludes'],target,'headers',env);record=dict(config=config,arch=arch,kind=kind,discovery_exit=code)
   if code:records.append(record);continue
   headers=includes(log);tools={cl,link,vc};tools.update(cl.parent.glob('*.dll'));tools.update(cl.parent.glob('1033/*.dll'));tools.update((vc.parent/'bin').glob('*.dll'));tools.update((vc.parent.parent/'Common7/IDE').glob('mspdb*.dll'))
   libs=set()
   for directory in env['LIB'].split(';'):
    for name in LIB_NAMES:
     p=Path(directory)/(name+'.lib')
     if p.is_file():libs.add(p.resolve())
   if kind=='host':libs.add(sdk/'lib/win/Mss32.lib')
   def snapshot():return dict(sources=identities(root/x for x in source),headers=identities(headers),tools=identities(tools),libraries=identities(libs))
   before=snapshot();exe=target/'test.exe';command+=['/showIncludes','/Fe'+str(exe)]
   if kind=='host':command.append(str(sdk/'lib/win/Mss32.lib'))
   command+=['/link','/VERBOSE:LIB'];code,log=run(command,target,'compile',env)
   output=dict(sha256=digest(exe),machine=machine(exe),path=str(exe)) if code==0 else None
   after=snapshot();record.update(exit_code=code,before=before,after=after,inputs_unchanged=before==after and includes(log)==headers,output=output)
   if kind=='wire' and code==0:
    assert digest(exe)==output['sha256'];p=subprocess.run([str(exe)],capture_output=True,timeout=30);(target/'run.log').write_bytes(p.stdout+p.stderr);record['run_exit']=p.returncode
   records.append(record)
receipt=dict(schema='startup-metadata-build-v1',builds=records,builder_before=builder_before,builder_after=digest(__file__),runtime_scope='wire tests only; host PE not launched')
p=out/'receipt.json';exclusive_json(p,receipt);print(json.dumps({'receipt_sha256':digest(p),'builds':[{k:r.get(k) for k in ['config','arch','kind','discovery_exit','exit_code','run_exit','inputs_unchanged']} for r in records]},indent=2));(out/'receipt.sha256').write_text(digest(p)+'\n')
raise SystemExit(any(r.get('discovery_exit') or r.get('exit_code') or not r.get('inputs_unchanged') or r.get('run_exit',0) for r in records))
