from pathlib import Path
import subprocess,os,json,re,shutil,hashlib
b=Path('C:/miles-engine-fixture-v1');b.mkdir(exist_ok=True)
r=Path('C:/integration-current-v2/workspace/repo');pr=r/'src/engine/client/library/clientAudio/build/win32';app=r/'src/game/client/application/SwgClient/build/win32'
setup=b/'env.cmd';setup.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" x86 >nul\nset\n')
e=os.environ.copy()
for l in subprocess.check_output(['cmd','/c',str(setup)],text=True).splitlines():
 if '=' in l and not l.startswith('='):k,v=l.split('=',1);e[k.upper()]=v
text=next((r/'src/compile/win32/clientAudio/Release').rglob('CL.command.1.tlog')).read_text(encoding='utf-16')
row=next(l for l in text.splitlines() if l.startswith('/c ') and 'AUDIO.CPP' in l and 'FIRSTCLIENT' not in l)
inc=re.findall(r'/I(?:"([^"]+)"|(\S+))',row)
flags=['/I'+str((pr/(a or c)).resolve()) for a,c in inc]
flags+=['/D'+v for v in re.findall(r'/D (\S+)',row)]
cl=shutil.which('cl.exe',path=e['PATH']);link=shutil.which('link.exe',path=e['PATH'])
cmd=[cl,'/nologo','/c','/EHsc','/MT','/O2','/Gy','/Zc:wchar_t-']+flags+[str(b/'probe.cpp'),'/Fo'+str(b/'probe.obj')]
(b/'compile-command.json').write_text(json.dumps(cmd,indent=2));x=subprocess.run(cmd,cwd=pr,env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(b/'compile.log').write_bytes(x.stdout)
if x.returncode:raise SystemExit(x.returncode)
log=Path('C:/integration-current-head-v2/results/Win32-Release.log').read_text(errors='replace')
line=next(l for l in reversed(log.splitlines()) if 'link.exe ' in l)
libpaths=['/LIBPATH:'+str((app/(a or c)).resolve()) for a,c in re.findall(r'/LIBPATH:(?:"([^"]+)"|(\S+))',line)]
# Actual product dependency list only; do not reuse product entry objects or permissive link flags.
libs=[]
for a,c in re.findall(r'"([^"\n]+\.(?:lib|a))"|(?<!\S)([^\s"]+\.(?:lib|a))(?=\s|$)',line,re.I):
 value=a or c
 if not value.startswith('/'):libs.append(value)
cmd=[link,'/nologo','/OPT:REF','/SAFESEH:NO','/SUBSYSTEM:CONSOLE','/NODEFAULTLIB:libc','/NODEFAULTLIB:MSVCRT',str(b/'probe.obj')]+libpaths+libs+['/OUT:'+str(b/'probe.exe'),'/MAP:'+str(b/'probe.map'),'/VERBOSE:LIB']
(b/'link-command.json').write_text(json.dumps(cmd,indent=2));x=subprocess.run(cmd,cwd=app,env=e,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(b/'link.log').write_bytes(x.stdout)
(b/'results.json').write_text(json.dumps({'compile':0,'link':x.returncode,'source_sha256':hashlib.sha256((b/'probe.cpp').read_bytes()).hexdigest()},indent=2));raise SystemExit(x.returncode)
