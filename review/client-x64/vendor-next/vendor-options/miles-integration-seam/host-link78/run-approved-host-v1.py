from pathlib import Path
import subprocess,json,hashlib,sys
if sys.argv[1:]!=['--approved-host-link-only']:raise SystemExit('approved host-only link required')
r=Path(__file__).resolve().parent;out=r/'evidence-v1';out.mkdir(exist_ok=False)
vm=Path('/home/akilleez/Work/swg-source-vm/winbuild');product=Path('/home/akilleez/Work/swg-source/client-build-next')
pins={'run-host-link78.py':'c732083ad24e8902a2bfc2e7fc64bb13df64c51ce9760b000d9876e44d4fb139','pins.json':'fb1ec8493637f173fba0e5878050a6b886534d5645a57e23533d803105fce63e'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for n,h in pins.items():assert sha(r/n)==h
assert subprocess.check_output(['git','-C',str(product),'rev-parse','HEAD']).decode().strip()=='49d0eeed4ddaa177d7a93ea396c37c3d9b9942da'
assert not subprocess.check_output(['git','-C',str(product),'status','--porcelain=v1'])
commands=[]
def run(args,name,check=True):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
 (out/(name+'.log')).write_bytes(p.stdout);commands.append({'argv':args,'exit':p.returncode,'log':name+'.log'});(out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 print(name,'exit',p.returncode,flush=True)
 if check and p.returncode:raise RuntimeError(name+' failed, no retry')
 return p.returncode
run([str(vm/'winps.sh'),"$ErrorActionPreference='Stop'; if(Test-Path C:/host-link78){throw 'Destination exists'}; if(Get-Process link -ErrorAction SilentlyContinue){throw 'Linker already active'}; New-Item -ItemType Directory C:/host-link78"],'01-create')
scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
for n in pins:run(scp+[str(r/n),'builder@127.0.0.1:C:/host-link78/'+n],'02-upload-'+n)
collector=out/'collect.py';collector.write_text('''from pathlib import Path
import json,zipfile,hashlib
r=Path('C:/host-link78');out=r/'link-evidence-v1'
files=[p for p in out.iterdir() if p.is_file() and p.suffix in {'.json','.log'}]
with zipfile.ZipFile(r/'curated-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,str(p.relative_to(r)))
print(json.dumps({'sha256':hashlib.sha256((r/'curated-evidence.zip').read_bytes()).hexdigest(),'files':len(files)}))
''')
run(scp+[str(collector),'builder@127.0.0.1:C:/host-link78/collect.py'],'02-upload-collector')
verify="$ErrorActionPreference='Stop'; "+'; '.join("if((Get-FileHash 'C:/host-link78/"+n+"' -Algorithm SHA256).Hash.ToLower() -ne '"+h+"'){throw 'authored identity mismatch'}" for n,h in pins.items())
run([str(vm/'winps.sh'),verify],'03-verify')
rc=run([str(vm/'winps.sh'),"& C:/ci-dpvs-review/python/python.exe C:/host-link78/run-host-link78.py --approved-host-link-only; exit $LASTEXITCODE"],'04-link-once',False)
run([str(vm/'winps.sh'),"& C:/ci-dpvs-review/python/python.exe C:/host-link78/collect.py; exit $LASTEXITCODE"],'05-collect')
run(scp+['builder@127.0.0.1:C:/host-link78/curated-evidence.zip',str(out/'curated-evidence.zip')],'06-download')
for n,h in pins.items():assert sha(r/n)==h
assert not subprocess.check_output(['git','-C',str(product),'status','--porcelain=v1'])
(out/'local-receipt.json').write_text(json.dumps({'link_gate_exit':rc,'output_executed':False,'product_unchanged':True,'archive_sha256':sha(out/'curated-evidence.zip'),'inputs':pins},indent=2)+'\n')
raise SystemExit(rc)
