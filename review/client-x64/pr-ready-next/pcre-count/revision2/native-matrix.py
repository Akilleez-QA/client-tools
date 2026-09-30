from pathlib import Path
import subprocess,json,sys
root=Path('C:/pr-pcre18-revision2'); results=[]
for platform,arch,bits,variant in [('Win32','x86',32,'source'),('x64','amd64',64,'source'),('Win32','x86',32,'original')]:
 for cfg in ['Debug','Release']:
  out=root/'results'/(variant+'-'+platform+'-'+cfg);out.mkdir(parents=True,exist_ok=True)
  include=Path('C:/pcre-native-v3')/(arch+'-'+cfg)/'pcre-4.1'
  lib=Path('C:/parser-integration-v3')/(platform+'-'+cfg)/'pcre.lib' if variant=='source' else Path('C:/xml-pcre-next/legacy-libpcre.a')
  command=['C:/ci-dpvs-review/python/python.exe',str(root/'tools/test-pcre-capture-count/run.py'),'--checkout',str(root),'--include-dir',str(include),'--library',str(lib),'--bits',str(bits),'--configuration',cfg,'--out',str(out)]
  batch=out/'run.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\nif errorlevel 1 exit /b 1\n'+subprocess.list2cmdline(command)+'\nexit /b %errorlevel%\n')
  done=subprocess.run(['cmd','/d','/c',str(batch)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
  (out/'runner.log').write_bytes(done.stdout);results.append(dict(case=out.name,exit=done.returncode))
(root/'matrix.json').write_text(json.dumps(results,indent=2))
sys.exit(0 if all(x['exit']==0 for x in results) else 1)
