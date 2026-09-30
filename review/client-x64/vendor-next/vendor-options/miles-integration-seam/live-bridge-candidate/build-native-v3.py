from pathlib import Path
import subprocess,json,hashlib
r=Path('C:/miles-live-bridge-v3b');results=[]
common=['transport-candidate/codec.cpp','pipe-transport-candidate/endpoint.cpp','coordinator-candidate/coordinator.cpp']
for cfg in ['Debug','Release']:
 for arch in ['x86','amd64']:
  out=r/(arch+'-'+cfg);out.mkdir(exist_ok=True);cmd=out/'build.cmd';exe=out/('host.exe' if arch=='x86' else 'controller.exe')
  sources=['live-bridge-candidate/bridge.cpp']+common+(['host-candidate/host_dispatch.cpp','host-candidate/retained_buffers.cpp','buffer-upload-candidate/buffer_upload.cpp'] if arch=='x86' else [])
  command='cl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /IC:/client-next-build/src/external/3rd/library/miles/include '+('/MTd /Od ' if cfg=='Debug' else '/MT /O2 ')+' '.join('"'+str(r/s)+'"' for s in sources)+(' C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib' if arch=='x86' else '')+' /Fe"'+str(exe)+'"'
  cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\nif errorlevel 1 exit /b 1\ncd /d "'+str(out)+'"\n'+command+'\n')
  p=subprocess.run(['cmd','/d','/c',str(cmd)],capture_output=True,timeout=90);(out/'compile.log').write_bytes(p.stdout+p.stderr);results.append(dict(config=cfg,arch=arch,exit=p.returncode))
  if p.returncode==0:
   for name,extra in [('repairs',['live-bridge-candidate/repair-tests.cpp']+common),('retained',['host-candidate/retained_buffers_test.cpp','host-candidate/retained_buffers.cpp']),('payload',['live-bridge-candidate/payload-allocation-test.cpp','host-candidate/retained_buffers.cpp']),('payload-old',['live-bridge-candidate/payload-allocation-test.cpp','live-bridge-candidate/retained-v2-control.cpp'])]:
    test=out/(name+'.exe');testcmd=out/(name+'.cmd')
    testcmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\ncd /d "'+str(out)+'"\ncl /nologo /EHsc /W4 /WX /DWIN32 /D_WIN32_WINNT=0x0601 /I"'+str(r/'host-candidate')+'" '+('/MTd /Od ' if cfg=='Debug' else '/MT /O2 ')+' '.join('"'+str(r/x)+'"' for x in extra)+' /Fe"'+str(test)+'"\n')
    q=subprocess.run(['cmd','/d','/c',str(testcmd)],capture_output=True,timeout=90);(out/(name+'-build.log')).write_bytes(q.stdout+q.stderr)
    rec=dict(config=cfg,arch=arch,test=name,compile=q.returncode)
    if q.returncode==0:
     run=subprocess.run([str(test)],capture_output=True,timeout=30);(out/(name+'-run.log')).write_bytes(run.stdout+run.stderr);rec['run']=run.returncode;rec['expected_run']=1 if name=='payload-old' else 0
    results.append(rec)
(r/'build-results.json').write_text(json.dumps({'results':results,'source_sha256':{str(p.relative_to(r)):hashlib.sha256(p.read_bytes()).hexdigest() for d in ['live-bridge-candidate','host-candidate','transport-candidate','pipe-transport-candidate','protocol-candidate','coordinator-candidate','buffer-upload-candidate'] for p in (r/d).glob('*') if p.is_file()}},indent=2));print(results)
raise SystemExit(any(x.get('exit',0) or x.get('compile',0) or ('expected_run' in x and x['run']!=x['expected_run']) for x in results))
