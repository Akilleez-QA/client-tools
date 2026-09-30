from pathlib import Path
import subprocess,json,difflib
root=Path('C:/regex-count-next');root.mkdir(exist_ok=True);results=[]
for platform,arch,variant in [('Win32','x86','candidate'),('x64','amd64','candidate'),('Win32','x86','stock')]:
 for cfg in ['Release','Debug']:
  out=root/(variant+'-'+platform+'-'+cfg);out.mkdir(exist_ok=True)
  src=Path('C:/pcre-native-v3')/(arch+'-'+cfg)/'pcre-4.1'
  provider=Path('C:/parser-integration-v3')/(platform+'-'+cfg)/'pcre.lib' if variant=='candidate' else Path('C:/xml-pcre-next/legacy-libpcre.a')
  driver=out/'pcretest.c';driver.write_bytes(Path('C:/regex-count-probe.c').read_bytes())
  flags='/nologo /DPCRE_STATIC /DSUPPORT_UTF8 /DHAVE_CONFIG_H /DPOSIX_MALLOC_THRESHOLD=10 '+('/MTd' if cfg=='Debug' else '/MT')
  batch=out/'build.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\nif errorlevel 1 exit /b 1\ncl '+flags+' /I'+str(src)+' '+str(driver)+' '+str(provider)+' /Fepcretest.exe\n')
  r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=out,capture_output=True,timeout=60);(out/'build.log').write_bytes(r.stdout+r.stderr)
  entry=dict(platform=platform,cfg=cfg,variant=variant,build_exit=r.returncode,tests=[],skips=[{'test':3,'reason':'Exact POSIX fr locale not established; no substitute locale requested'}]);results.append(entry)
  if r.returncode:continue
  r=subprocess.run([str(out/'pcretest.exe')],cwd=out,capture_output=True,timeout=30)
  (out/'run.log').write_bytes(r.stdout+r.stderr);entry['run_exit']=r.returncode
  (root/'results.json').write_text(json.dumps(results,indent=2))
