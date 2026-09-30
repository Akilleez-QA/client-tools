from pathlib import Path
import subprocess
p=Path(__file__).resolve().parent;s=(p/'run2.py').read_text()
for mode in ['sample','stream']:
 for n in range(1,4):
  name='drain-'+mode+'-'+str(n)
  candidate=s.replace("base/'run2'","base/'"+name+"'").replace('vendor-miles-probe/probe.exe','vendor-miles-probe/probe-drain-isolated.exe')
  candidate=candidate.replace("sample.mp3'],env=env", "sample.mp3','"+mode+"'],env=env")
  path=p/(name+'.py');path.write_text(candidate)
  result=subprocess.run(['python',str(path)]);assert result.returncode==0
