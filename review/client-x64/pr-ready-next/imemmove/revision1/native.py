from pathlib import Path
import subprocess,json,sys
root=Path('C:/pr-imemmove18-v1');rows=[]
for variant in ['candidate','baseline']:
 for bits,arch in [(32,'x86'),(64,'amd64')]:
  for cfg in ['Debug','Release']:
   name='%s-%s-%s'%(variant,bits,cfg);out=root/'results'/name
   cmd=['C:/ci-dpvs-review/python/python.exe',str(root/'tools/run.py'),'--checkout',str(root/variant),'--out',str(out),'--bits',str(bits),'--configuration',cfg]
   if variant=='baseline':cmd+=['--baseline']
   if variant=='baseline' and bits==64:cmd+=['--expect-ambiguity']
   batch=root/(name+'.cmd');batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\nif errorlevel 1 exit /b 1\n'+subprocess.list2cmdline(cmd)+'\nexit /b %errorlevel%\n')
   run=subprocess.run(['cmd','/d','/c',str(batch)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
   (root/(name+'.log')).write_bytes(run.stdout);rows.append(dict(name=name,exit=run.returncode))
(root/'matrix.json').write_text(json.dumps(rows,indent=2));sys.exit(0 if all(x['exit']==0 for x in rows) else 1)
