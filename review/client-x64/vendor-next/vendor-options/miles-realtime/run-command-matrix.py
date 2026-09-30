from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent;s=(p/'run2.py').read_text()
for mode in ['sample','stream']:
 for route in ['direct','controller']:
  name='command-'+route+'-'+mode;c=s.replace("base/'run2'","base/'"+name+"'")
  if route=='direct':
   c=c.replace('vendor-miles-probe/probe.exe','vendor-miles-probe/miles-command-host.exe').replace("sample.mp3'],env=env", "sample.mp3','"+mode+"'],env=env")
  else:
   a=c.index("player=subprocess.Popen(");b=c.index(",env=env,cwd=out",a);c=c[:a]+"player=subprocess.Popen(['wine',str(prefix/'drive_c/vendor-miles-probe/miles-controller.exe'),'"+mode+"']"+c[b:]
  q=p/(name+'.py');q.write_text(c);r=subprocess.run(['python',str(q)]);assert r.returncode==0
