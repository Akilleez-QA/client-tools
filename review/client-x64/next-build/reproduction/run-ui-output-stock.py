from pathlib import Path
import subprocess,json
root=Path('C:/client-next-build'); out=Path('C:/ui-output-stock-negative');out.mkdir(exist_ok=False);rows=[]
vc='C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat';proj=root/'src/external/3rd/library/ui/build/win32'
for platform,arch,directory in [('Win32','x86','win32')]:
 audit=Path('C:/client-next-results')/('ui-Release-'+platform+'.audit.log');line=next(l.strip() for l in audit.read_text().splitlines() if l.strip().startswith('CL|'));parts=line.split('|');d=out/platform;d.mkdir()
 flags=['/EHsc','/MT','/O2','/Gy','/Y-','/Zc:wchar_t-','/nologo']+['/D"'+v+'"' for v in parts[6].split(';') if v]+['/I"'+v+'"' for v in parts[7].split(';') if v]
 flags+=['/I"'+str(root/'src/external/3rd/library/ui/src/win32')+'"','C:/ui-output-probe.cpp','/Fo"'+str(d/'probe.obj')+'"','/Fe"'+str(d/'probe.exe')+'"','/link','"'+'C:/ci-link-proof-clean/build-tree/src/compile/win32/ui/Release/ui.lib'+'"','/OPT:REF','/OPT:ICF','/LIBPATH:C:/client-next-build/src/external/3rd/library/stlport453/lib/win32','/MAP:"'+str(d/'probe.map')+'"','/VERBOSE:LIB']
 flags=[v.replace(chr(34),'') for v in flags]
 rsp=d/'compile.rsp';rsp.write_text(subprocess.list2cmdline(flags))
 cmd=d/'compile.cmd';cmd.write_text('@echo off\ncall "'+vc+'" '+arch+' >nul\ncd /d "'+str(proj)+'"\ncl '+' '.join(flags)+'\nexit /b %errorlevel%\n')
 p=subprocess.run(['cmd','/c',str(cmd)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'compile.log').write_bytes(p.stdout);run=None
 if not p.returncode:
  q=subprocess.run([str(d/'probe.exe')],cwd=d,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'run.log').write_bytes(q.stdout);run=q.returncode
 rows.append([platform,p.returncode,run])
(out/'results.json').write_text(json.dumps(rows));print(rows)
