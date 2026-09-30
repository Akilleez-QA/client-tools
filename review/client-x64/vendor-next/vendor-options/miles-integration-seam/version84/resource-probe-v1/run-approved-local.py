#!/usr/bin/env python3
"""Prospective authorized staging/build/API observation; no default execution."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile
if sys.argv[1:]!=['--approved-single-api-run']:raise SystemExit('Separate parent approval required')
b=Path(__file__).resolve().parent;vm=Path('/home/akilleez/Work/swg-source-vm/winbuild')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((b/'manifest.json').read_text())
for name,h in m['sha256'].items():
 if sha(b/name)!=h:raise RuntimeError('Input changed: '+name)
pins=b/'private/tool-pins.json'
if sha(pins)!=m['private_tool_pins_sha256']:raise RuntimeError('Private pins changed')
o=b/'local-evidence-v1';o.mkdir(exist_ok=False);o.chmod(0o700)
commands=[]
def run(args,label,check=True):
 commands.append({'label':label,'argv':args});(o/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 with (o/(label+'.log')).open('wb') as f:p=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=300)
 commands[-1]['exit_code']=p.returncode;(o/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 if check and p.returncode:raise RuntimeError(label+' failed; no retry')
 return p.returncode
archive=o/'private-inputs.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for name in list(m['sha256'])+['manifest.json']:z.write(b/name,name)
 z.write(pins,'tool-pins.json')
archive.chmod(0o600)
ps=vm/'winps.sh'
run([str(ps),"$ErrorActionPreference='Stop'; if(Test-Path 'C:/resource-probe84'){throw 'Destination exists'}; if(Get-Process cl,link,rc -ErrorAction SilentlyContinue){throw 'Build slot busy'}; New-Item -ItemType Directory 'C:/resource-probe84'"],'01-create')
scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
run(scp+[str(archive),'builder@127.0.0.1:C:/resource-probe84/private-inputs.zip'],'02-upload')
script="$ErrorActionPreference='Stop'; if((Get-FileHash 'C:/resource-probe84/private-inputs.zip' -Algorithm SHA256).Hash.ToLower() -ne '"+sha(archive)+"'){throw 'Archive mismatch'}; Expand-Archive 'C:/resource-probe84/private-inputs.zip' 'C:/resource-probe84'; if((Get-FileHash 'C:/resource-probe84/manifest.json' -Algorithm SHA256).Hash.ToLower() -ne '"+sha(b/'manifest.json')+"'){throw 'Manifest mismatch'}; if((Get-FileHash 'C:/resource-probe84/tool-pins.json' -Algorithm SHA256).Hash.ToLower() -ne '"+sha(pins)+"'){throw 'Pins mismatch'}"
run([str(ps),script],'03-stage')
code=run([str(ps),"& C:/ci-dpvs-review/python/python.exe C:/resource-probe84/run-probe.py --approved-api-probe C:/resource-probe84/tool-pins.json; exit $LASTEXITCODE"],'04-single-probe',False)
run([str(ps),"& C:/ci-dpvs-review/python/python.exe C:/resource-probe84/collect-text.py; exit $LASTEXITCODE"],'05-collect')
run(scp+['builder@127.0.0.1:C:/resource-probe84/curated-text.zip',str(o/'curated-text.zip')],'06-download')
changed=[n for n,h in m['sha256'].items() if sha(b/n)!=h]
(o/'local-after.json').write_text(json.dumps({'gate_exit':code,'changed':changed,'private_pins_unchanged':sha(pins)==m['private_tool_pins_sha256'],'curated_zip_sha256':sha(o/'curated-text.zip'),'runner_invocations':1},indent=2)+'\n')
if changed or sha(pins)!=m['private_tool_pins_sha256']:raise SystemExit(1)
raise SystemExit(code)
