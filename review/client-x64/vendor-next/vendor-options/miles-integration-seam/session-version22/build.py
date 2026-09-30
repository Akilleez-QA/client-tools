"""Native v120 resource component build; launches no PEs."""
from pathlib import Path
import sys, json, shutil, re, os, platform
root=Path('C:/session-version22')
sys.path.insert(0,str(root/'revision4-tools'))
from build_receipt import environment, identities, includes, run, exclusive_json, LIB_NAMES
from receipt import digest, machine
out=root/'build-v1'; out.mkdir(exist_ok=False)
vc=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
sdk=Path('C:/client-next-build/src/external/3rd/library/miles/include/Mss.h')
if digest(sdk)!='966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
    raise RuntimeError('private SDK identity mismatch')
sources=list((root/'session-version22').glob('*.cpp'))+list((root/'session-version22').glob('*.h'))
sources+=list((root/'transport-candidate').glob('*'))+list((root/'protocol-candidate').glob('*'))
builders=list((root/'revision4-tools').glob('*.py'))+list((root/'session-version22').glob('*.py'))
initial=identities(sources); builder_before=identities(builders); records=[]
for config in ['Debug','Release']:
 for arch in ['x86','amd64']:
  for kind in (['wire','host','poison'] if arch=='x86' else ['wire']):
   target=out/(arch+'-'+config+'-'+kind); target.mkdir(); env=environment(vc,arch,target)
   cl=Path(shutil.which('cl.exe',path=env['PATH'])); link=Path(shutil.which('link.exe',path=env['PATH']))
   files=['session-version22/session_version.cpp','transport-candidate/codec.cpp',
          'session-version22/'+('wire_test.cpp' if kind=='wire' else 'host_test.cpp')]
   if kind!='wire': files+=['session-version22/session_version_host.cpp']
   flags=[str(cl),'/nologo','/W4','/WX','/EHsc','/DWIN32','/D_WIN32_WINNT=0x0601',
          '/I'+str(sdk.parent),'/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2']
   if kind=='poison': flags+=['/DVERSION_POISON_CONTROL','/DMSS_VERSION="SV21_COMPILE_TIME_POISON"']
   command=flags+[str(root/x) for x in files]
   code,log=run(command+['/Zs','/showIncludes'],target,'headers',env)
   record=dict(config=config,arch=arch,kind=kind,discovery_exit=code)
   if code: records.append(record); continue
   headers=includes(log); tools={cl,link,vc}
   tools.update(cl.parent.glob('*.dll')); tools.update(cl.parent.glob('1033/*.dll'))
   tools.update((vc.parent/'bin').glob('*.dll')); tools.update((vc.parent.parent/'Common7/IDE').glob('mspdb*.dll'))
   libs=set()
   for directory in env['LIB'].split(';'):
    for name in LIB_NAMES:
     p=Path(directory)/(name+'.lib')
     if p.is_file(): libs.add(p.resolve())
   def snapshot(): return dict(sources=identities(sources),headers=identities(headers),tools=identities(tools),libraries=identities(libs))
   before=snapshot(); exe=target/'test.exe'
   command+=['/showIncludes','/Fe'+str(exe),'/link','/VERBOSE:LIB','user32.lib']
   code,log=run(command,target,'compile',env)
   output=dict(sha256=digest(exe),machine=machine(exe),path=str(exe)) if code==0 else None
   after=snapshot()
   searched={Path(m.group(1)).resolve() for line in log.splitlines()
       for m in [re.match(r'\s*Searching (.+\.lib):\s*$',line)] if m and Path(m.group(1)).is_file()}
   uncovered=sorted(str(p) for p in searched-libs)
   record.update(exit_code=code,before=before,after=after,output=output,
      inputs_unchanged=before==after and before['sources']==initial and includes(log)==headers and not uncovered,
      observed_link_library_paths=sorted(str(p) for p in searched),unrecorded_libraries=uncovered)
   records.append(record)
receipt=dict(schema='session-version22-build-v1',builds=records,builder_before=builder_before,
 builder_after=identities(builders),source_before=initial,source_after=identities(sources),
 python_sha256=digest(sys.executable),system=platform.platform(),scope='compile only; no PEs launched')
receipt['stable_matrix']=receipt['builder_before']==receipt['builder_after'] and receipt['source_before']==receipt['source_after']
p=out/'receipt.json'; exclusive_json(p,receipt); pin=digest(p); (out/'receipt.sha256').write_text(pin+'\n'); os.chmod(p,0o444)
print(json.dumps(dict(receipt_sha256=pin,stable_matrix=receipt['stable_matrix'],builds=[{k:r.get(k) for k in ['config','arch','kind','discovery_exit','exit_code','inputs_unchanged']} for r in records]),indent=2))
raise SystemExit(not receipt['stable_matrix'] or any(r.get('discovery_exit') or r.get('exit_code') or not r.get('inputs_unchanged') for r in records))
