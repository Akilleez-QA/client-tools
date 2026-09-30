from pathlib import Path
import re,subprocess,json,hashlib
root=Path('C:/capture-poll-candidate-v2');root.mkdir()
repo=Path('C:/integration-current-v1/workspace/repo');project=repo/'src/engine/client/library/clientUserInterface/build/win32';source=Path('C:/capture-poll-CuiIoWin.cpp');results=[]
q=lambda x:'"'+str(x)+'"'
for config in ['Debug','Release']:
 for platform,arch in [('win32','x86'),('x64','x86_amd64')]:
  repo=Path('C:/integration-current-v1/workspace/repo' if platform=='win32' else 'C:/integration-current-v2/workspace/repo')
  project=repo/'src/engine/client/library/clientUserInterface/build/win32'
  name=config+'-'+platform;d=root/name;d.mkdir()
  logs=list((repo/'src/compile'/platform/'clientUserInterface'/config).rglob('cl.command.1.tlog'));assert len(logs)==1
  lines=logs[0].read_text(encoding='utf-16').splitlines();cmd=next(lines[i+1] for i,l in enumerate(lines) if l.startswith('^') and l.upper().endswith('CUIIOWIN.CPP'))
  (d/'original-command.txt').write_text(cmd)
  cmd=re.sub(r'/Fo(?:"[^"]*"|\S+)',lambda m:'/Fo'+q(d/'CuiIoWin.obj'),cmd,flags=re.I)
  cmd=re.sub(r'/Fd(?:"[^"]*"|\S+)',lambda m:'/Fd'+q(d/'CuiIoWin.pdb'),cmd,flags=re.I)
  cmd=re.sub(r'(?i)[QR]:\\REPO\\\S*CUIIOWIN.CPP',lambda m:q(source),cmd)
  cmd=re.sub(r'(?i)/Gm\b','/Gm-',cmd)
  cmd=re.sub(r'(?i)/Fp(?:"[^"]*"|\S+)','',cmd)
  cmd=re.sub(r'(?i)/Yu(?:"[^"]*"|\S+)','/Y-',cmd)
  # No tracked dependency/output files are written into the product tree.
  assert '/Fo'+q(d/'CuiIoWin.obj') in cmd and str(source) in cmd
  (d/'compile.rsp').write_text(cmd)
  bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\ncl @'+q(d/'compile.rsp')+'\nexit /b %errorlevel%\n')
  p=subprocess.run(['cmd','/c',str(bat)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(p.stdout)
  result=dict(name=name,compile_exit=p.returncode,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),metadata_sha256=hashlib.sha256(logs[0].read_bytes()).hexdigest())
  results.append(result);print(name,p.returncode,flush=True)
(root/'results.json').write_text(json.dumps(results,indent=2))
raise SystemExit(any(r['compile_exit'] for r in results))
