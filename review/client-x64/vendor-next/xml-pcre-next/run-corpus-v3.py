from pathlib import Path
import subprocess,json,difflib
root=Path('C:/pcre-corpus-v3');root.mkdir(exist_ok=True);results=[]
for platform,arch,variant in [('Win32','x86','candidate'),('x64','amd64','candidate'),('Win32','x86','stock')]:
 for cfg in ['Release','Debug']:
  out=root/(variant+'-'+platform+'-'+cfg);out.mkdir(exist_ok=True)
  src=Path('C:/pcre-native-v3')/(arch+'-'+cfg)/'pcre-4.1'
  provider=Path('C:/parser-integration-v3')/(platform+'-'+cfg)/'pcre.lib' if variant=='candidate' else Path('C:/xml-pcre-next/legacy-libpcre.a')
  driver=out/'pcretest.c';driver.write_text((src/'pcretest.c').read_text().replace('outfile = stdout;', 'outfile = stdout;\n_set_printf_count_output(1);', 1))
  flags='/nologo /DPCRE_STATIC /DSUPPORT_UTF8 /DHAVE_CONFIG_H /DPOSIX_MALLOC_THRESHOLD=10 '+('/MTd' if cfg=='Debug' else '/MT')
  batch=out/'build.cmd';batch.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+'\nif errorlevel 1 exit /b 1\ncl '+flags+' /I'+str(src)+' '+str(driver)+' '+str(provider)+' /Fepcretest.exe /link /STACK:8388608,4096\n')
  r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=out,capture_output=True,timeout=60);(out/'build.log').write_bytes(r.stdout+r.stderr)
  entry=dict(platform=platform,cfg=cfg,variant=variant,build_exit=r.returncode,tests=[],skips=[{'test':3,'reason':'Exact POSIX fr locale not established; no substitute locale requested'}]);results.append(entry)
  if r.returncode:continue
  for n in [1,2,4,5]:
   output=out/('output'+str(n)+'.txt');command=[str(out/'pcretest.exe')]+(['-i'] if n==2 else [])+[str(src/('testdata/testinput'+str(n))),str(output)]
   r=subprocess.run(command,cwd=out,capture_output=True,timeout=60)
   actual=output.read_bytes().replace(b'\r\n',b'\n');expected=(src/('testdata/testoutput'+str(n))).read_bytes().replace(b'\r\n',b'\n')
   equal=actual==expected
   if not equal:(out/('diff'+str(n)+'.txt')).write_text(''.join(difflib.unified_diff(expected.decode('latin1').splitlines(True),actual.decode('latin1').splitlines(True))),encoding='utf-8')
   entry['tests'].append(dict(test=n,exit=r.returncode,reference_equal=equal,output_bytes=len(actual)))
  (root/'results.json').write_text(json.dumps(results,indent=2))
