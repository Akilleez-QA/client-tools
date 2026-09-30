import pathlib,tarfile,subprocess,json
root=pathlib.Path('C:/pcre-native-v3');root.mkdir(exist_ok=True);results=[]
for arch in ['x86','amd64']:
 for cfg in ['Release','Debug']:
  target=root/(arch+'-'+cfg);target.mkdir(exist_ok=True)
  with tarfile.open('C:/xml-pcre-next/pcre-4.1.tar.gz') as t:t.extractall(target)
  cwd=target/'pcre-4.1';s=(cwd/'config.in').read_text().replace('HAVE_STRERROR 0','HAVE_STRERROR 1').replace('HAVE_MEMMOVE  0','HAVE_MEMMOVE  1');(cwd/'config.h').write_text(s)
  (cwd/'pcre.h').write_text((cwd/'pcre.in').read_text().replace('@PCRE_MAJOR@','4').replace('@PCRE_MINOR@','1').replace('@PCRE_DATE@','12-Mar-2003'))
  flags='/nologo /DPCRE_STATIC /DSUPPORT_UTF8 /DHAVE_CONFIG_H /DPOSIX_MALLOC_THRESHOLD=10 '+('/MTd /Od /D_DEBUG' if cfg=='Debug' else '/MT /O2 /DNDEBUG')
  commands=['call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch,'cl '+flags+' dftables.c /Fedftables.exe','dftables.exe > chartables.c','cl '+flags+' /c maketables.c get.c study.c pcre.c pcreposix.c','lib /nologo /OUT:pcre.lib maketables.obj get.obj study.obj pcre.obj pcreposix.obj','cl '+flags+' pcretest.c pcre.lib /Fepcretest.exe','pcretest.exe testdata/testinput1 testoutput1.actual']
  batch=target/'build.cmd';batch.write_text('@echo off\n'+'\nif errorlevel 1 exit /b 1\n'.join(commands)+'\n')
  r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  (target/'build.log').write_bytes(r.stdout);results.append(dict(arch=arch,cfg=cfg,exit=r.returncode,commands=commands));(root/'results.json').write_text(json.dumps(results,indent=2))
