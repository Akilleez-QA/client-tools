from pathlib import Path
import subprocess,tarfile,json
root=Path('C:/parser-integration-v3');root.mkdir(exist_ok=True)
with tarfile.open('C:/xml-pcre-next/parser-integration.tar') as t:t.extractall(root/'repo')
results=[]
for platform in ['Win32','x64']:
 for cfg in ['Release','Debug']:
  out=root/(platform+'-'+cfg)
  command=['C:/ci-dpvs-review/python/python.exe',str(root/'repo/tools/build-client-deps/build-parsers.py'),'--output',str(out),'--vcvars','C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat','--platform',platform,'--configuration',cfg,'--pcre-archive','C:/xml-pcre-next/pcre-4.1.tar.gz','--libxml-archive','C:/xml-pcre-next/libxml2-2.6.7.tar.gz']
  r=subprocess.run(command,capture_output=True,timeout=480);(root/(platform+'-'+cfg+'.log')).write_bytes(r.stdout+r.stderr);results.append(dict(platform=platform,cfg=cfg,exit=r.returncode,command=command));(root/'results.json').write_text(json.dumps(results,indent=2))
