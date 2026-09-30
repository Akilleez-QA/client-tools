import pathlib,tarfile,subprocess,json,os
root=pathlib.Path('C:/xml-pcre-next-v3');root.mkdir(exist_ok=True)
results=[]
for arch in ['x86','amd64']:
 for cfg in ['Release','Debug']:
  target=root/(arch+'-'+cfg);target.mkdir(exist_ok=True)
  with tarfile.open('C:/xml-pcre-next/libxml2-2.6.7.tar.gz') as t:t.extractall(target)
  cwd=target/'libxml2-2.6.7/win32'
  make=cwd/'Makefile.msvc';make.write_text(make.read_text().replace('/OPT:NOWIN98',''))
  flags='ftp=no http=no html=yes c14n=no docb=no iconv=no sax1=yes legacy=no '
  flags+='xml_debug=yes mem_debug=yes cruntime=/MTd debug=yes' if cfg=='Debug' else 'xml_debug=no mem_debug=no cruntime=/MT debug=no'
  command='call "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' && cscript //nologo configure.js '+flags+' && nmake /f Makefile.msvc libxml'
  # libxml target builds genuine DLL/import library; no static-consumer edits.
  batch=target/'build.cmd';batch.write_text('@echo off\n'+command+'\n')
  r=subprocess.run(['cmd','/d','/c',str(batch)],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  (target/'build.log').write_bytes(r.stdout);results.append(dict(arch=arch,configuration=cfg,exit=r.returncode,command=command));(root/'results.json').write_text(json.dumps(results,indent=2))
