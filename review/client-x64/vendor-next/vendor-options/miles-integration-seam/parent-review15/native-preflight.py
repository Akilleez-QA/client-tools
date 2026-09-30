from pathlib import Path
import tarfile,subprocess,json
b=Path('C:/miles-preflight-parent15')
with tarfile.open(b/'input.tar') as t:t.extractall(b)
source=b/'host-candidate/host_dispatch.cpp';original=source.read_text();needle='memset(&out,0,sizeof(out));'
assert needle in original
source_mutant=b/'host-candidate/host_dispatch_mutant.cpp';source_mutant.write_text(original.replace(needle,'/* negative control: output clear omitted */',1))
results=[]
for cfg in ['Debug','Release']:
 for variant in ['actual','mutant']:
  out=b/(cfg+'-'+variant);out.mkdir()
  flags='/nologo /EHsc /DWIN32 '+('/MTd /Od' if cfg=='Debug' else '/MT /O2')+' /IC:/client-next-build/src/external/3rd/library/miles/include '
  src=source if variant=='actual' else source_mutant
  cmd=out/'build.cmd';cmd.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul\nif errorlevel 1 exit /b 1\ncl '+flags+str(src)+' '+str(b/'host-candidate/preflight.cpp')+' C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib delayimp.lib /Fe'+str(out/'probe.exe')+' /link /DELAYLOAD:mss32.dll\nexit /b %errorlevel%\n')
  p=subprocess.run(['cmd','/c',str(cmd)],cwd=out,capture_output=True);(out/'build.log').write_bytes(p.stdout+p.stderr)
  row={'cfg':cfg,'variant':variant,'build_exit':p.returncode}
  if not p.returncode:
   p=subprocess.run([str(out/'probe.exe')],cwd=out,capture_output=True,timeout=15);(out/'run.log').write_bytes(p.stdout+p.stderr);row.update(run_exit=p.returncode,stdout=p.stdout.decode(errors='replace'))
  results.append(row)
(b/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
