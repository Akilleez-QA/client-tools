#!/usr/bin/env python3
"""Reviewed object-only candidate; requires a separately authorized native gate."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
if os.name!='nt' or sys.argv[1:]!=['--approved-compile-only']:
 raise SystemExit('Requires Windows and explicit approved compile-only invocation')
ROOT=Path('C:/native-file-callbacks35')
SNAPSHOT=ROOT/'snapshot'
SOURCE=ROOT/'seam/native-file-callbacks35'
OUT=ROOT/'results'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'input-manifest.json').read_text())
for relative,expected in manifest['sha256'].items():
 if sha(ROOT/relative)!=expected:raise RuntimeError('Input identity mismatch: '+relative)
SDK=SNAPSHOT/'src/external/3rd/library/miles/include/Mss.h'
if sha(SDK)!='966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
 raise RuntimeError('Wrong possessed SDK header')
OUT.mkdir(exist_ok=False)
receipt={'expected_count':2,'linked':False,'executed':False,'builds':[],
 'input_manifest_sha256':sha(ROOT/'input-manifest.json'),
 'policy':'stop first unexpected failure; no retry',
 'header_attestation':'single-time during each compile, not before/after',
 'probe_limit':'extern declarations have original callback shapes; not actual Audio bodies/symbols'}
def save():(OUT/'results.json').write_text(json.dumps(receipt,indent=2)+'\n')
try:
 setup=OUT/'environment.cmd'
 setup.write_text('@echo off\ncall "'+str(VCVARS)+'" amd64 >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n')
 p=subprocess.run(['cmd','/d','/c',str(setup)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
 if p.returncode:raise RuntimeError('vcvars failed')
 env={k.upper():v for k,v in os.environ.items()}
 for line in p.stdout.decode(errors='replace').splitlines():
  if '=' in line and not line.startswith('='):
   k,v=line.split('=',1);env[k.upper()]=v
 compiler=shutil.which('cl.exe',path=env['PATH']);dumpbin=shutil.which('dumpbin.exe',path=env['PATH'])
 if not compiler or not dumpbin:raise RuntimeError('Native tools missing')
 receipt['tools']={str(p):sha(p) for p in [Path(compiler),Path(dumpbin),VCVARS]}
 audit=ROOT/'inputs/clientAudio-Debug-x64.audit.log'
 rows=[line.strip().split('|') for line in audit.read_text(encoding='utf-8-sig').splitlines() if line.strip().startswith('CL|')]
 row=next(row for row in rows if row[1].replace('\\','/').endswith('/Audio.cpp'))
 definitions=['/D'+x for x in row[6].split(';') if x]
 engine_includes=['/I'+x for x in row[7].split(';') if x]
 for name,engine in [('native_file_callbacks',False),('engine_header_probe',True)]:
  directory=OUT/name;directory.mkdir()
  source=SOURCE/(name+'.cpp');obj=directory/(name+'.obj')
  if engine:
   guard=directory/'require-v120.h'
   guard.write_text('#if !defined(_MSC_VER) || _MSC_VER != 1800 || !defined(_WIN64)\n#error Requires actual v120 Win64 test compilation\n#endif\n')
   flags=['/nologo','/c','/EHsc','/Y-','/Gm-','/Zc:wchar_t-','/Zc:forScope','/GR','/Gy','/fp:precise','/W4','/Zi','/FC','/showIncludes','/FI'+str(guard),'/Fd'+str(directory/(name+'.pdb')),'/MTd','/Od','/Ob1','/RTC1','/WX']+definitions+engine_includes
   cwd=SNAPSHOT/'src/engine/client/library/clientAudio/build/win32'
  else:
   flags=['/nologo','/c','/W4','/WX','/EHsc','/MT','/O2','/Y-','/DWIN32','/D_WIN32_WINNT=0x0601','/showIncludes','/I'+str(SDK.parent)]
   cwd=directory
  command=[compiler]+flags+[str(source),'/Fo'+str(obj)]
  (directory/'command.json').write_text(json.dumps(command,indent=2)+'\n')
  record={'unit':name,'command':command,'cwd':str(cwd),'status':'pending'}
  receipt['builds'].append(record);save()
  try:p=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
  except subprocess.TimeoutExpired as error:
   (directory/'compile.log').write_bytes(error.stdout or b'');record['status']='timeout';raise
  (directory/'compile.log').write_bytes(p.stdout)
  lines=p.stdout.decode(errors='replace').splitlines();includes={}
  for line in lines:
   m=re.match(r'^Note: including file:\s*(.+?)\s*$',line)
   if m:
    path=Path(m.group(1)).resolve();includes[str(path)]=sha(path)
  (directory/'actual-includes.json').write_text(json.dumps(includes,indent=2)+'\n')
  names=[x.replace('\\','/').lower() for x in includes]
  stlport=any('/stlport453/' in x for x in names)
  msvc_cpp=any('/vc/include/' in x and Path(x).suffix=='' for x in names)
  sdk_seen=str(SDK.resolve()) in includes
  # The native TU may see SDK only from the snapshot, never engine/STLport.
  other_snapshot=any('/snapshot/' in x and '/library/miles/include/' not in x for x in names)
  boundary=(stlport and not msvc_cpp and not sdk_seen) if engine else (sdk_seen and not stlport and not other_snapshot)
  record.update(exit_code=p.returncode,diagnostics=[x for x in lines if re.search(r'\b(?:warning|error|fatal error) [A-Z]\d+',x)],include_boundary_ok=boundary,actual_includes_sha256=sha(directory/'actual-includes.json'))
  if p.returncode:record['status']='compile-failed';raise RuntimeError(name+' compilation failed')
  machine=struct.unpack_from('<H',obj.read_bytes())[0]
  record.update(coff_machine=hex(machine),object_sha256=sha(obj))
  if machine!=0x8664 or not boundary:record['status']='boundary-or-machine-failed';raise RuntimeError(name+' boundary or machine failure')
  record['status']='compiled';save()
  if not engine:
   command=[dumpbin,'/symbols',str(obj)]
   (directory/'symbols-command.json').write_text(json.dumps(command,indent=2)+'\n')
   p=subprocess.run(command,cwd=directory,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
   (directory/'symbols.log').write_bytes(p.stdout)
   observed={line.split()[-1] for line in p.stdout.decode(errors='replace').splitlines() if 'UNDEF' in line and '__imp_AIL_' in line}
   record['undefined_miles_imports']=sorted(observed)
   if p.returncode or observed!={'__imp_AIL_set_file_callbacks'}:raise RuntimeError('Unexpected native import set')
  print(json.dumps(record),flush=True)
except Exception as error:
 receipt['failure']={'type':type(error).__name__,'message':str(error)}
finally:
 after={relative:sha(ROOT/relative) for relative in manifest['sha256']}
 (OUT/'inputs-after.json').write_text(json.dumps(after,indent=2)+'\n')
 receipt['all_staged_inputs_unchanged']=after==manifest['sha256']
 receipt['passed']=not receipt.get('failure') and receipt['all_staged_inputs_unchanged'] and len(receipt['builds'])==2 and all(x['status']=='compiled' for x in receipt['builds'])
 save()
sys.exit(0 if receipt['passed'] else 1)
