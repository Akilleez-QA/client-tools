import os,subprocess,shutil,json,hashlib,re
from pathlib import Path
root=Path('C:/client-next-build');out=Path('C:/vendor-reachability/trackir-candidate-v2');out.mkdir(parents=True,exist_ok=False)
items=[('clientGame','ClientHeadTracking.cpp')]
results=[]
for config in ['Release','Debug']:
 for platform,arch in [('Win32','x86'),('x64','amd64')]:
  d=out/(config+'-'+platform);d.mkdir();bat=d/'env.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n');v=subprocess.run(['cmd','/d','/c',str(bat)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);assert v.returncode==0;env={k.upper():v for k,v in os.environ.items()}
  for l in v.stdout.decode(errors='replace').splitlines():
   if '=' in l and not l.startswith('='):k,val=l.split('=',1);env[k.upper()]=val
  cl=shutil.which('cl.exe',path=env['PATH']);dumpbin=shutil.which('dumpbin.exe',path=env['PATH'])
  for project,name in items:
   audit=Path('C:/client-next-results')/(project+'-'+config+'-'+platform+'.audit.log');rows=[l.strip().split('|') for l in audit.read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|')];row=next(x for x in rows if x[1].replace('\\','/').endswith('/'+name));projectdir=next(root.glob('src/**/'+project+'/build/win32'));source=(projectdir/row[1]).resolve();assert source.is_file(),source
   source=Path('C:/vendor-reachability/ClientHeadTracking.cpp')
   flags=['/nologo','/EHsc','/Y-','/Zc:wchar_t-','/MTd' if config=='Debug' else '/MT']+['/D'+x for x in row[6].split(';') if x]+['/I'+x for x in row[7].split(';') if x]
   record=dict(project=project,source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),config=config,platform=platform,defines=row[6],audit_sha256=hashlib.sha256(audit.read_bytes()).hexdigest())
   for phase,extra in [('preprocess',['/P','/Fi'+str(d/(name+'.i'))]),('compile',['/c','/Fo'+str(d/(name+'.obj'))])]:
    cmd=[cl]+flags+extra+[str(source)];(d/(name+'.'+phase+'.command.json')).write_text(json.dumps(cmd));v=subprocess.run(cmd,cwd=projectdir,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180);(d/(name+'.'+phase+'.log')).write_bytes(v.stdout);record[phase]=v.returncode
   if record['compile']==0:
    v=subprocess.run([dumpbin,'/symbols','/directives',str(d/(name+'.obj'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,timeout=60);(d/(name+'.symbols.txt')).write_bytes(v.stdout)
   for version,header,status,frame,iodata,pitch,yaw in [('legacy',root/'src/external/3rd/library/trackIR/include/NPClient.h','wNPStatus','wPFrameSignature','dwNPIOData','fNPPitch','fNPYaw'),('official',Path('C:/vendor-reachability/NPClient-current.h'),'Status','FrameSignature','IOData','Pitch','Yaw')]:
    probe=d/(version+'.cpp');probe.write_text('#include <windows.h>\n#include <stddef.h>\n#include <stdio.h>\n#include "'+header.as_posix()+'"\nint main(){printf("%u %u %u %u %u %u %u %u\\n",(unsigned)sizeof(TRACKIRDATA),(unsigned)sizeof(SIGNATUREDATA),(unsigned)offsetof(TRACKIRDATA,'+status+'),(unsigned)offsetof(TRACKIRDATA,'+frame+'),(unsigned)offsetof(TRACKIRDATA,'+iodata+'),(unsigned)offsetof(TRACKIRDATA,'+pitch+'),(unsigned)offsetof(TRACKIRDATA,'+yaw+'),(unsigned)sizeof(PF_NP_REGISTERWINDOWHANDLE));return 0;}\n')
    cmd=[cl,'/nologo','/EHsc','/MT',str(probe),'/Fo'+str(d/(version+'.obj')),'/Fe'+str(d/(version+'.exe'))];v=subprocess.run(cmd,cwd=d,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120);(d/(version+'.compile.log')).write_bytes(v.stdout);record[version+'_compile']=v.returncode
    if v.returncode==0:
     v=subprocess.run([str(d/(version+'.exe'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30);(d/(version+'.run.log')).write_bytes(v.stdout);record[version+'_layout']=v.stdout.decode().strip();record[version+'_run']=v.returncode
   results.append(record);(out/'results.json').write_text(json.dumps(results,indent=2));print(config,platform,name,record['preprocess'],record['compile'],flush=True)
