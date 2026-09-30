from pathlib import Path
import subprocess,json,hashlib
root=Path('C:/capture-poll-candidate-v2');records=[]
q=lambda x:'"'+str(x)+'"'
for config in ['Debug','Release']:
 for platform,arch in [('win32','x86'),('x64','x86_amd64')]:
  d=root/(config+'-'+platform);repo=Path('C:/integration-current-v1/workspace/repo' if platform=='win32' else 'C:/integration-current-v2/workspace/repo');original=repo/'src/compile'/platform/'clientUserInterface'/config/'clientUserInterface.lib';new=d/'clientUserInterface.lib'
  def run(command,name):
   bat=d/(name+'.cmd');bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\n'+command+'\nexit /b %errorlevel%\n');p=subprocess.run(['cmd','/c',str(bat)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/(name+'.log')).write_bytes(p.stdout);assert p.returncode==0,(name,p.stdout[-1000:]);return p.stdout.decode(errors='replace').splitlines()
  members=run('lib /nologo /list '+q(original),'list-before');matches=[x.strip() for x in members if x.strip().lower().replace('\\','/').endswith('/cuiiowin.obj') or x.strip().lower()=='cuiiowin.obj'];assert len(matches)==1,matches
  run('lib /nologo '+q(original)+' /remove:'+q(matches[0])+' /out:'+q(d/'without-cui.lib'),'remove')
  run('lib /nologo '+q(d/'without-cui.lib')+' '+q(d/'CuiIoWin.obj')+' /out:'+q(new),'replace')
  after=run('lib /nologo /list '+q(new),'list-after');assert sum(x.strip().lower().replace('\\','/').endswith('/cuiiowin.obj') or x.strip().lower()=='cuiiowin.obj' for x in after)==1
  records.append(dict(name=d.name,removed_member=matches[0],original=str(original),original_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),candidate=str(new),candidate_sha256=hashlib.sha256(new.read_bytes()).hexdigest(),object_sha256=hashlib.sha256((d/'CuiIoWin.obj').read_bytes()).hexdigest()))
(root/'repack-results.json').write_text(json.dumps(records,indent=2));print([(r['name'],r['candidate']) for r in records])
