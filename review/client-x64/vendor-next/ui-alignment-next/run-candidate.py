from pathlib import Path
import subprocess,json,hashlib,struct,zipfile
out=Path('C:/ui-alignment-candidate-v1');out.mkdir(exist_ok=False)
a=Path('C:/client-next-build/src/external/3rd/library/ui')
project=a/'build/win32' 
libs=json.loads(Path('C:/allocator-next/core-libraries-all.json').read_text())
q=lambda p:'"'+str(p)+'"'
results=[]
for config in ['Debug','Release']:
 for platform,arch,machine in [('Win32','x86',0x14c),('x64','amd64',0x8664)]:
  name=config+'-'+platform;d=out/name;d.mkdir()
  audit=Path('C:/client-next-results')/('ui-'+name+'.audit.log')
  row=next(l.strip().split('|') for l in audit.read_text(encoding='utf-8-sig').splitlines() if l.strip().startswith('CL|') and l.strip().split('|')[1].replace('\\','/').endswith('/UiMemoryBlockManager.cpp'))
  defs=['/D'+q(v) for v in row[6].split(';') if v];incs=['/I'+q(a/'src/shared'),'/I'+q(a/'include'),'/I'+q(a/'src/win32')]+['/I'+q(v.replace(chr(92),'/')) for v in row[7].split(';') if v]
  common=['/nologo','/EHsc','/Y-','/Zc:wchar_t-','/Gy','/MTd' if config=='Debug' else '/MT','/Od' if config=='Debug' else '/O2']+defs+incs
  commands=[];sources=[Path('C:/ui-alignment-candidate.cpp'),a/'src/shared/core/UiReport.cpp',Path('C:/ui-alignment-probe.cpp')]
  for i,source in enumerate(sources):
   rsp=d/(str(i)+'.rsp');rsp.write_text(' '.join(common+['/c',q(source),'/Fo'+q(d/(str(i)+'.obj'))]));commands+=['cl @'+q(rsp),'if errorlevel 1 exit /b %errorlevel%']
  library=next(Path(p) for p in libs[name] if 'stlport' in p.lower())
  lcd=json.loads((Path('C:/vendor-lcd-integration/real-wrapper-v4')/name/'link.command.json').read_text())
  extra=[x for x in lcd[1:] if (x.lower().endswith('.lib') or (x.lower().endswith('.obj') and ('allocator-minimum-v1' in x or 'MemoryManager.obj' in x)))]
  commands+=['link /nologo /OPT:REF /NODEFAULTLIB:stlport_vc71_static.lib /NODEFAULTLIB:stlport_vc71_stldebug_static.lib '+ ' '.join(q(d/(str(i)+'.obj')) for i in range(3))+' '+ ' '.join(q(x) for x in extra)+' /OUT:'+q(d/'probe.exe')+' /MAP:'+q(d/'probe.map'),'exit /b %errorlevel%']
  bat=d/'build.cmd';bat.write_text('@echo off\ncall "C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat" '+arch+' >nul\n'+'\n'.join(commands))
  p=subprocess.run(['cmd','/c',str(bat)],cwd=project,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'build.log').write_bytes(p.stdout)
  result=dict(name=name,link_inputs={x:hashlib.sha256(Path(x).read_bytes()).hexdigest() for x in extra if Path(x).is_file()},compile=p.returncode,library=str(library),library_sha256=hashlib.sha256(library.read_bytes()).hexdigest(),sources={str(s):hashlib.sha256(s.read_bytes()).hexdigest() for s in sources})
  if not p.returncode:
   exe=d/'probe.exe';bits=exe.read_bytes();pe=struct.unpack_from('<I',bits,0x3c)[0];result['machine']=struct.unpack_from('<H',bits,pe+4)[0]
   run=subprocess.run([str(exe)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30);(d/'run.log').write_bytes(run.stdout);result.update(run=run.returncode,output=run.stdout.decode(errors='replace'))
   result['passed']=result['machine']==machine and run.returncode==0 and result['output'].strip()=='PASS: 3129 UI alignment checks'
  results.append(result)
(out/'results.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2));raise SystemExit(0 if all(r.get('passed') for r in results) else 1)
