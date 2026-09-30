from pathlib import Path
import subprocess,json
root=Path('C:/parser-integration-reject-v1');root.mkdir(exist_ok=True);bad=root/'bad.tar.gz';bad.write_bytes(b'not the pinned source');results=[]
for name,value in [('mismatch',str(bad)),('missing',str(root/'missing.tar.gz'))]:
 out=root/name
 command=['C:/ci-dpvs-review/python/python.exe','C:/parser-integration-v3/repo/tools/build-client-deps/build-parsers.py','--output',str(out),'--vcvars','C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat','--platform','x64','--configuration','Release','--pcre-archive',value,'--libxml-archive','C:/xml-pcre-next/libxml2-2.6.7.tar.gz']
 r=subprocess.run(command,capture_output=True,timeout=20);results.append(dict(case=name,exit=r.returncode,output_created=out.exists(),stderr=r.stderr.decode(errors='replace')))
(root/'results.json').write_text(json.dumps(results,indent=2))
assert all(x['exit']!=0 and not x['output_created'] for x in results)
