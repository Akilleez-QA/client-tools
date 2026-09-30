from pathlib import Path
import subprocess,re,json,hashlib
root=Path('C:/integration-current-v2/workspace/repo/src/compile/x64');out=Path('C:/integration-stl-audit-v1');out.mkdir(exist_ok=True)
dump='C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/dumpbin.exe'
rows=[]
for p in sorted(root.glob('*/Debug/*.lib')):
 r=subprocess.run([dump,'/directives',str(p)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 text=r.stdout.decode(errors='replace'); names=sorted(set(re.findall(r'/DEFAULTLIB:(\S*stlport\S*)',text,re.I)))
 rows.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),exit=r.returncode,stlport_defaults=names))
(out/'Debug-directive-inventory.json').write_text(json.dumps(rows,indent=2));print(json.dumps(dict(libraries=len(rows),defaults=sorted(set(n for x in rows for n in x['stlport_defaults'])),failed=sum(x['exit']!=0 for x in rows)),indent=2))
