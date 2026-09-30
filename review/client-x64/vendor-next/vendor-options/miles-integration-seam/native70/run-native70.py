#!/usr/bin/env python3
"""One explicitly approved compile-only gate. No link, target execution or retry."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
from symbol_parser import undefined_symbols
if os.name!='nt' or sys.argv[1:]!=['--approved-twelve-objects']:
 raise SystemExit('Windows and separate approval required')
ROOT=Path('C:/native70');INPUT=ROOT/'inputs';OUT=ROOT/'results'
REUSED=Path('C:/native-file-callbacks35');SNAPSHOT=REUSED/'snapshot'
SDK=SNAPSHOT/'src/external/3rd/library/miles/include/Mss.h'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root,expected):
 actual={name:sha(root/name) for name in expected}
 if actual!=expected:raise RuntimeError('Input mismatch at '+str(root))
 return actual
manifest=json.loads((ROOT/'input-manifest.json').read_text())['sha256']
verify(ROOT,manifest)
reused=json.loads((INPUT/'reused35-manifest.json').read_text())['sha256']
if sha(REUSED/'input-manifest.json')!=sha(INPUT/'reused35-manifest.json'):
 raise RuntimeError('Reused35 manifest identity differs')
verify(REUSED,reused)
if len(reused)!=9536 or sha(SDK)!='966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
 raise RuntimeError('Wrong SDK or reused snapshot')
tools=json.loads((INPUT/'tools35.json').read_text());verify(Path('.'),tools)
OUT.mkdir(exist_ok=False)
receipt={'expected_new_objects':12,'linked':False,'executed':False,'builds':[],
 'input_manifest':sha(ROOT/'input-manifest.json'),'reused35_manifest':sha(INPUT/'reused35-manifest.json'),
 'reused35_count':len(reused),'tools_before':tools,'header_hash_timing':'single-time at each include observation',
 'scope':'nine production objects, two include orders, one actual engine header probe; no Audio adoption'}
def save():(OUT/'results.json').write_text(json.dumps(receipt,indent=2)+'\n')
def norm(path):return str(Path(path).resolve()).replace('\\','/').lower()
try:
 # No simultaneous native compiler. This queries processes; it does not kill any.
 p=subprocess.run(['tasklist','/FI','IMAGENAME eq cl.exe','/FO','CSV','/NH'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
 (OUT/'compiler-slot.log').write_bytes(p.stdout)
 if p.returncode or b'cl.exe' in p.stdout.lower():raise RuntimeError('Compiler slot unavailable')
 setup=OUT/'environment.cmd';setup.write_text('@echo off\ncall "'+str(VCVARS)+'" amd64 >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n')
 p=subprocess.run(['cmd','/d','/c',str(setup)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
 if p.returncode:raise RuntimeError('vcvars failed')
 env={k.upper():v for k,v in os.environ.items()}
 for line in p.stdout.decode(errors='replace').splitlines():
  if '=' in line and not line.startswith('='):
   k,v=line.split('=',1);env[k.upper()]=v
 compiler=shutil.which('cl.exe',path=env['PATH']);dumpbin=shutil.which('dumpbin.exe',path=env['PATH'])
 if not compiler or not dumpbin:raise RuntimeError('Missing tools')
 if {norm(p):sha(Path(p)) for p in [compiler,dumpbin,str(VCVARS)]}!={norm(p):v for p,v in tools.items()}:
  raise RuntimeError('Resolved tool identity mismatch')
 rows=[line.strip().split('|') for line in (REUSED/'inputs/clientAudio-Debug-x64.audit.log').read_text(encoding='utf-8-sig').splitlines() if line.strip().startswith('CL|')]
 row=next(x for x in rows if x[1].replace('\\','/').endswith('/Audio.cpp'))
 defs=['/D'+x for x in row[6].split(';') if x];inc=['/I'+x for x in row[7].split(';') if x]
 baseline={norm(p):h for p,h in json.loads((INPUT/'baseline35-includes.json').read_text()).items()}
 units=[('plain_startup', 'candidate/plain_startup.cpp'), ('failure_boundary', 'candidate/private/failure_boundary.cpp'), ('native_startup_calls', 'candidate/native/native_startup_calls.cpp'), ('plain_operations', 'candidate/plain_operations.cpp'), ('native_operations', 'candidate/native/native_calls60.cpp'), ('plain_file_setter', 'candidate/plain_file_setter.cpp'), ('native_file_setter', 'candidate/native/native_file_setter67.cpp'), ('plain_callbacks', 'candidate/plain_callbacks.cpp'), ('native_callbacks', 'candidate/native/native_callbacks70.cpp'), ('plain_first', 'plain_first.cpp'), ('sdk_first', 'sdk_first.cpp'), ('engine_plain_probe', 'engine_plain_probe.cpp')]
 expectations=json.loads((INPUT/"symbol-expectations.json").read_text())
 for name,rel in units:
  target=OUT/name;target.mkdir();obj=target/(name+'.obj');engine=name=='engine_plain_probe';native=name in expectations['imports'] or name in ['plain_first','sdk_first']
  flags=['/nologo','/c','/W4','/WX','/EHsc','/Y-','/showIncludes','/FI'+str(INPUT/'require-v120.h')]
  if engine:
   flags+=['/Gm-','/Zc:wchar_t-','/Zc:forScope','/GR','/Gy','/fp:precise','/Zi','/FC','/Fd'+str(target/(name+'.pdb')),'/MTd','/Od','/Ob1','/RTC1']+defs+inc
   cwd=SNAPSHOT/'src/engine/client/library/clientAudio/build/win32'
  else:
   flags+=['/MT','/O2','/Ob0','/DWIN32','/D_WIN32_WINNT=0x0601']
   if native:flags+=['/I'+str(SDK.parent)]
   cwd=target
  command=[compiler]+flags+[str(INPUT/rel),'/Fo'+str(obj)]
  record={'unit':name,'command':command,'cwd':str(cwd),'status':'pending'};receipt['builds'].append(record);save()
  (target/'command.json').write_text(json.dumps(command,indent=2)+'\n')
  try:p=subprocess.run(command,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
  except subprocess.TimeoutExpired as e:(target/'compile.log').write_bytes(e.stdout or b'');raise
  (target/'compile.log').write_bytes(p.stdout)
  lines=p.stdout.decode(errors='replace').splitlines();includes={};ancestry=[];stack=[]
  for line in lines:
   match=re.match(r'^Note: including file:(\s+)(.+?)\s*$',line)
   if match:
    depth=len(match.group(1));path=Path(match.group(2)).resolve();key=norm(path);includes[key]=sha(path)
    while stack and stack[-1][0]>=depth:stack.pop()
    ancestry.append({'path':key,'depth':depth,'ancestors':[a[1] for a in stack]});stack.append((depth,key))
  (target/'actual-includes.json').write_text(json.dumps(includes,indent=2)+'\n')
  (target/'include-ancestry.json').write_text(json.dumps(ancestry,indent=2)+'\n')
  record.update(exit_code=p.returncode,diagnostics=[x for x in lines if re.search(r'\b(?:warning|error|fatal error) [A-Z]\d+',x)])
  if p.returncode:record['status']='compile-failed';raise RuntimeError(name+' compile failed')
  machine=struct.unpack_from('<H',obj.read_bytes())[0];record.update(machine=hex(machine),object_sha256=sha(obj))
  if machine!=0x8664 or record['diagnostics']:raise RuntimeError('Machine or diagnostics failure')
  stl=any('/stlport453/' in x for x in includes);sdk=norm(SDK) in includes
  if engine:
   forbidden=[x for x in includes if '/library/miles/' in x or '/candidate/private/' in x or '/candidate/native/' in x]
   changed=[x for x in includes if x in baseline and includes[x]!=baseline[x]]
   new=[a for a in ancestry if a['path'] not in baseline]
   # All new includes must be the authored forced guard/plain facade or descend
   # from that facade. Inherited MSVC C++ headers are allowed with identical hash.
   allowed={norm(INPUT/'require-v120.h'),norm(INPUT/'candidate/ClientMiles.h')}
   unattributed=[a for a in new if a['path'] not in allowed and norm(INPUT/'candidate/ClientMiles.h') not in a['ancestors']]
   (target/'baseline35-comparison.json').write_text(json.dumps({'overlap':sorted(set(includes)&set(baseline)),'changed':changed,'added':new,'unattributed':unattributed,'forbidden':forbidden},indent=2)+'\n')
   if not stl or sdk or forbidden or changed or unattributed:raise RuntimeError('Engine boundary or attribution concern')
  elif stl or sdk!=native or any('/snapshot/' in x and '/library/miles/include/' not in x for x in includes):raise RuntimeError('Modern boundary concern')
  command=[dumpbin,'/symbols',str(obj)];(target/'symbols-command.json').write_text(json.dumps(command,indent=2)+'\n')
  p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,timeout=45);(target/'symbols.log').write_bytes(p.stdout)
  symbols=undefined_symbols(p.stdout.decode(errors='replace'));miles={s for s in symbols if 'AIL_' in s};record['undefined_symbols']=symbols
  if p.returncode or miles!=set(expectations['imports'].get(name,[])):raise RuntimeError('Unexpected actual AIL imports')
  required={'failure_boundary':['abort'],'engine_plain_probe':['?startup@ClientMiles@@','?set_file_callbacks@ClientMiles@@','?register_EOS_callback@ClientMiles@@','?register_stream_callback@ClientMiles@@']}.get(name,[])
  if name in expectations['delegates']:
   spec=expectations['delegates'][name]
   observed={match.group(1) for s in symbols for match in [re.match(r'^\?([^@]+)@'+spec['namespace']+r'@@',s)] if match}
   if observed!=set(spec['names']):raise RuntimeError('Exact private delegate set mismatch: '+name)
   required+=['?requireFatalReporter@ClientMilesPrivate52@@','?fail@ClientMilesPrivate52@@']
  if any(not any(s.startswith(prefix) or s=='__imp_'+prefix for s in symbols) for prefix in required):raise RuntimeError('Required dependency absent')
  # Every production/public TU and both include probes must see the new facade.
  needed=['candidate/private/failure_boundary.h'] if name=='failure_boundary' else ['candidate/ClientMiles.h']
  if native:needed+=['candidate/native/native_types70.h'] if name not in ['native_file_setter'] else ['candidate/private/native_file_setter67.h']
  if any(includes.get(norm(INPUT/n))!=manifest['inputs/'+n] for n in needed):raise RuntimeError('Missing pinned authored header: '+name)
  record['status']='compiled';save()
except Exception as e:receipt['failure']={'type':type(e).__name__,'message':str(e)}
finally:
 for label,root,expected in [('inputs_after',ROOT,manifest),('reused35_after',REUSED,reused),('tools_after',Path('.'),tools)]:
  try:actual=verify(root,expected);receipt[label+'_unchanged']=True
  except Exception as e:actual={'error':str(e)};receipt[label+'_unchanged']=False
  (OUT/(label+'.json')).write_text(json.dumps(actual,indent=2)+'\n')
 receipt['passed']=not receipt.get('failure') and all(receipt[k+'_unchanged'] for k in ['inputs_after','reused35_after','tools_after']) and len(receipt['builds'])==12 and all(x['status']=='compiled' for x in receipt['builds'])
 save()
sys.exit(0 if receipt['passed'] else 1)
