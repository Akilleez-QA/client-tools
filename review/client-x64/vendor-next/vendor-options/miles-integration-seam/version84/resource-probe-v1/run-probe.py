"""Prospective one-build/one-run observation. Requires separately reviewed tool pins."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
if os.name!='nt' or len(sys.argv)!=3 or sys.argv[1]!='--approved-api-probe':
 raise SystemExit('Windows, approval flag and reviewed tool-pins.json path required')
b=Path(__file__).resolve().parent
pins_path=Path(sys.argv[2]).resolve();pins=json.loads(pins_path.read_text())
# tools: cl, rc, link; files includes every tool and explicitly selected library.
# env must be captured from the reviewed x86 v120 environment; no setup commands here.
manifest=json.loads((b/'manifest.json').read_text())['sha256']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
tracked={str(b/n):h for n,h in manifest.items()};tracked.update(pins['files']);tracked[str(pins_path)]=sha(pins_path)
def verify():
 actual={p:sha(p) for p in tracked}
 if actual!=tracked:raise RuntimeError('Frozen input changed')
 return actual
out=b/'evidence-v1';out.mkdir(exist_ok=False)
r={'target_runs':0,'passed':False,'scope':'own-resource LoadStringA observation only'}
def save():(out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
def run(cmd,label):
 (out/(label+'-command.json')).write_text(json.dumps(cmd,indent=2)+'\n')
 p=subprocess.run(cmd,cwd=out,env=pins['env'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
 (out/(label+'.log')).write_bytes(p.stdout);r[label+'_exit']=p.returncode;save()
 if p.returncode:raise RuntimeError(label+' failed; no retry')
try:
 (out/'before.json').write_text(json.dumps(verify(),indent=2)+'\n')
 for tool in ['cl','rc','link']:
  if pins['tools'][tool] not in pins['files']:raise RuntimeError('Unpinned tool')
 for lib in pins['libraries']:
  if lib not in pins['files']:raise RuntimeError('Unpinned library')
 run([pins['tools']['rc'],'/nologo','/fo',str(out/'probe.res'),str(b/'probe.rc')],'resource')
 run([pins['tools']['cl'],'/nologo','/c','/W4','/WX','/MTd','/EHsc','/Y-','/showIncludes',str(b/'probe.cpp'),'/Fo'+str(out/'probe.obj')],'compile')
 run([pins['tools']['link'],'/NOLOGO','/WX','/MACHINE:X86','/SUBSYSTEM:CONSOLE','/INCREMENTAL:NO','/NODEFAULTLIB','/OUT:'+str(out/'probe.exe'),str(out/'probe.obj'),str(out/'probe.res')]+pins['libraries'],'link')
 r['exe_sha256']=sha(out/'probe.exe');r['target_runs']=1;save()
 run([str(out/'probe.exe')],'observation')
 r['passed']=True
except Exception as e:r['failure']=str(e)
finally:
 try:(out/'after.json').write_text(json.dumps(verify(),indent=2)+'\n');r['inputs_unchanged']=True
 except Exception as e:r['inputs_unchanged']=False;r['passed']=False;r['after_failure']=str(e)
 save()
sys.exit(0 if r['passed'] else 1)
