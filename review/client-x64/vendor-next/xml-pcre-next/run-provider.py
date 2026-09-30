import pathlib,subprocess,shutil,json
root=pathlib.Path('C:/xml-pcre-probe-v3');root.mkdir(exist_ok=True);results=[]
for arch in ['x86','amd64']:
 for cfg in ['Release','Debug']:
  cwd=root/(arch+'-'+cfg);cwd.mkdir(exist_ok=True)
  p=pathlib.Path('C:/pcre-native-v3')/(arch+'-'+cfg)/'pcre-4.1';x=pathlib.Path('C:/xml-pcre-next-v3')/(arch+'-'+cfg)/'libxml2-2.6.7';lib=x/'win32/bin.msvc'
  shutil.copy2(lib/'libxml2.dll',cwd/'libxml2.dll')
  commands=['call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch,'cl /nologo /DPCRE_STATIC '+('/MTd' if cfg=='Debug' else '/MT')+' /I'+str(p)+' /I'+str(x/'include')+' C:/xml-pcre-next/provider-probe.c '+str(p/'pcre.lib')+' '+str(lib/'libxml2.lib')+' /Feprobe.exe','probe.exe']
  batch=cwd/'run.cmd';batch.write_text('@echo off\n'+'\nif errorlevel 1 exit /b 1\n'.join(commands)+'\n');r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30);(cwd/'result.log').write_bytes(r.stdout)
  actual=(p/'testoutput1.actual').read_bytes().replace(b'\r\n',b'\n');expected=(p/'testdata/testoutput1').read_bytes().replace(b'\r\n',b'\n');results.append(dict(arch=arch,cfg=cfg,exit=r.returncode,pcre_test1_exact=actual==expected));(root/'results.json').write_text(json.dumps(results,indent=2))
