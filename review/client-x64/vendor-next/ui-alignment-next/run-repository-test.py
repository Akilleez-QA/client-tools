from pathlib import Path
import json,subprocess,shutil
root=Path('C:/ui-alignment-repo-test-v3');root.mkdir()
repo=root/'source';ui=repo/'src/external/3rd/library/ui/src/shared/core';ui.mkdir(parents=True)
original=Path('C:/client-next-build/src/external/3rd/library/ui')
shutil.copy('C:/ui-alignment-candidate.cpp',ui/'UiMemoryBlockManager.cpp')
for name in ['UiReport.cpp','UILowerString.cpp']:shutil.copy(original/'src/shared/core'/name,ui/name)
results=[]
for config in ['Debug','Release']:
 for platform in ['Win32','x64']:
  name=config+'-'+platform
  row=next(l.strip().split('|') for l in (Path('C:/client-next-results')/('ui-'+name+'.audit.log')).read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|') and l.strip().split('|')[1].replace('\\','/').endswith('/UiMemoryBlockManager.cpp'))
  prev=json.loads(Path('C:/ui-alignment-candidate-v2/results.json').read_text())
  libs=next(r['link_inputs'] for r in prev if r['name']==name)
  inputs=dict(defines=[v for v in row[6].split(';') if v],include_dirs=[str(original/'src/shared'),str(original/'include'),str(original/'src/win32')]+[str((original/'build/win32'/v).resolve()) for v in row[7].split(';') if v],link_inputs=list(libs))
  manifest=root/(name+'.json');manifest.write_text(json.dumps(inputs,indent=2))
  p=subprocess.run(['C:/ci-dpvs-review/python/python.exe','C:/ui-memory-repository-test/run.py','--source',str(repo),'--vcvars','C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat','--inputs',str(manifest),'--configuration',config,'--platform',platform,'--out',str(root/name)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (root/(name+'.log')).write_bytes(p.stdout);results.append((name,p.returncode));print(name,p.returncode,flush=True)
(root/'summary.json').write_text(json.dumps(results));shutil.make_archive(str(root),'zip',root)
raise SystemExit(any(code for _,code in results))
