from pathlib import Path
import subprocess,json,hashlib
b=Path(__file__).resolve().parent
vm=Path('/home/akilleez/Work/swg-source-vm/winbuild')
scratch='C:/miles-preference-observation-20260930'
dll=Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0/Mss32.dll')
assert hashlib.sha256(dll.read_bytes()).hexdigest()=='0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe'
commands=[]
def run(args,name):
 commands.append(args)
 r=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
 (b/name).write_bytes(r.stdout);(b/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 if r.returncode:raise RuntimeError((name,r.returncode,r.stdout.decode(errors='replace')))
 return r
scp=['scp','-q','-i',str(vm/'ssh/id_ed25519'),'-P','2223','-o','UserKnownHostsFile='+str(vm/'ssh/known_hosts')]
run([str(vm/'winps.sh'),f"if(Test-Path '{scratch}'){{throw 'scratch exists'}}; New-Item -ItemType Directory '{scratch}'"],'create.log')
try:
 run(scp+[str(b/'probe.cpp'),str(b/'build.cmd'),str(dll),'builder@127.0.0.1:'+scratch+'/'],'upload.log')
 run([str(vm/'winps.sh'),f"Set-Location '{scratch}'; cmd /c build.cmd; exit $LASTEXITCODE"],'build.log')
 run([str(vm/'winps.sh'),f"Get-FileHash '{scratch}/probe.cpp','{scratch}/probe.exe','{scratch}/Mss32.dll','C:/client-next-build/src/external/3rd/library/miles/include/Mss.h','C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/bin/cl.exe' | Format-List"],'native-identities.log')
 for mode in ['inherited','pc24','pc64']:
  run([str(vm/'winps.sh'),f"Set-Location '{scratch}'; ./probe.exe '{scratch}/Mss32.dll' {mode}; exit $LASTEXITCODE"],mode+'.log')
finally:
 run([str(vm/'winps.sh'),f"Remove-Item -Recurse -Force '{scratch}'; Write-Output ('owned_scratch_exists='+(Test-Path '{scratch}'))"],'cleanup.log')
print('All three processes completed; inspect preference predictions and raw control-state transitions.')
