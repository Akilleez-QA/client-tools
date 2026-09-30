from pathlib import Path
import subprocess,json,hashlib
b=Path(__file__).resolve().parent
vm=Path('/home/akilleez/Work/swg-source-vm/winbuild')
scratch='C:/miles-generation-live-20260930'
commands=[]
def run(args,name):
 commands.append(args)
 r=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
 (b/name).write_bytes(r.stdout)
 (b/'native-commands.json').write_text(json.dumps(commands,indent=2))
 if r.returncode:raise RuntimeError((name,r.returncode,r.stdout.decode(errors='replace')))
 return r
scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
run([str(vm/'winps.sh'),f"if (Test-Path '{scratch}') {{ throw 'scratch exists' }}; New-Item -ItemType Directory '{scratch}'"],'native-create.log')
try:
 run(scp+[str(b/n) for n in ['probe.cpp','Mss.h','build.cmd']]+['builder@127.0.0.1:'+scratch+'/'],'native-upload.log')
 run([str(vm/'winps.sh'),f"Set-Location '{scratch}'; cmd /c build.cmd; exit $LASTEXITCODE"],'build.log')
 run([str(vm/'winps.sh'),f"Get-FileHash '{scratch}/probe.cpp','{scratch}/host.exe','{scratch}/controller.exe','C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/cl.exe','C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/x86_amd64/cl.exe' | Format-List"],'native-identities.log')
 for name in ['host.exe','controller.exe']:
  run(scp+['builder@127.0.0.1:'+scratch+'/'+name,str(b/name)],'native-download-'+name+'.log')
finally:
 run([str(vm/'winps.sh'),f"Remove-Item -Recurse -Force '{scratch}'; Write-Output ('owned_native_scratch_exists=' + (Test-Path '{scratch}'))"],'native-cleanup.log')
