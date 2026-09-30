#!/usr/bin/env python3
"""Prospective single approved v120 object gate. No link or target execution."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
from symbol_parser import undefined_symbols
if os.name!='nt' or sys.argv[1:]!=['--approved-35-objects']:
 raise SystemExit('Windows and separately approved 35-object invocation required')
ROOT=Path('C:/native77');INPUT=ROOT/'inputs';OUT=ROOT/'results'
REUSED=Path('C:/native-file-callbacks35');SNAPSHOT=REUSED/'snapshot'
SDK=SNAPSHOT/'src/external/3rd/library/miles/include/Mss.h'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(p):return str(Path(p).resolve()).replace('\\','/').lower()
def verify(root,expected):
 actual={n:sha(root/n) for n in expected}
 if actual!=expected:raise RuntimeError('Identity mismatch at '+str(root))
 return actual
manifest=json.loads((ROOT/'input-manifest.json').read_text())['sha256']
verify(ROOT,manifest)
reused=json.loads((INPUT/'reused35-manifest.json').read_text())['sha256']
if sha(REUSED/'input-manifest.json')!=sha(INPUT/'reused35-manifest.json'):
 raise RuntimeError('Reused35 manifest changed')
verify(REUSED,reused)
if len(reused)!=9536 or sha(SDK)!='966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
 raise RuntimeError('Wrong SDK/snapshot')
toolsets=json.loads((INPUT/'toolchain.json').read_text())
alltools={k:v for values in toolsets.values() for k,v in values.items()};verify(Path('.'),alltools)
units=json.loads((INPUT/'units.json').read_text())
if len(units)!=35 or sum(u['arch']=='x86' for u in units)!=18:raise RuntimeError('Wrong matrix')
OUT.mkdir(exist_ok=False)
receipt={'expected_new_objects':35,'linked':False,'executed':False,'builds':[],
 'input_manifest':sha(ROOT/'input-manifest.json'),'reused35_manifest':sha(INPUT/'reused35-manifest.json'),
 'reused35_count':len(reused),'tools_before':alltools,
 'header_hash_timing':'system headers observed once per reached compilation; no before/after system header attestation',
 'scope':'actual selected client17/host18 production objects; external engine worker implementation remains unlinked'}
def save():(OUT/'results.json').write_text(json.dumps(receipt,indent=2)+'\n')
required={
 'backend-boundary24/pipe/LiveChannel.cpp':['?validateReply@Session@ClientMilesPipe@@','?publish@Runtime@MilesClientRuntime53@@','?returned@Runtime@MilesClientRuntime53@@'],
 'client-runtime53/client_file_runtime.cpp':['?create@EngineFileWorker@MilesFileExecutor30@@','?start@EngineFileWorker@MilesFileExecutor30@@','?receiveControl@HostAssociationMapper@MilesFileOwner36@@'],
 'file-executor33/FileInvocationJob.cpp':['?submit@EngineFileWorker@MilesFileExecutor30@@','?invokeOnAdmittedExecutor@Invocation@MilesFileChannel26@@'],
 'host-runtime50/host_file_runtime.cpp':['?decodeRequest@MilesFileChannel26@@','?snapshot@MilesHostContext@@'],
 'host-runtime50/host_sdk_callbacks.cpp':['?invoke@Runtime@MilesHostRuntime50@@'],
 'file-channel26/file_channel.cpp':['??0Scope@MilesCallbackGuard47@@']
}
try:
 p=subprocess.run(['tasklist','/FI','IMAGENAME eq cl.exe','/FO','CSV','/NH'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=30)
 (OUT/'compiler-slot.log').write_bytes(p.stdout)
 if p.returncode or b'cl.exe' in p.stdout.lower():raise RuntimeError('Compiler slot unavailable')
 environments={}
 for u in units:
  arch=u['arch']
  if arch not in environments:
   setup=OUT/('environment-'+arch+'.cmd');setup.write_text('@echo off\ncall "'+str(VCVARS)+'" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n')
   p=subprocess.run(['cmd','/d','/c',str(setup)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
   (OUT/('environment-'+arch+'.log')).write_bytes(p.stdout)
   if p.returncode:raise RuntimeError('vcvars failed')
   env={k.upper():v for k,v in os.environ.items()}
   for line in p.stdout.decode(errors='replace').splitlines():
    if '=' in line and not line.startswith('='):
     k,v=line.split('=',1);env[k.upper()]=v
   compiler=shutil.which('cl.exe',path=env['PATH']);dumpbin=shutil.which('dumpbin.exe',path=env['PATH'])
   if not compiler or not dumpbin:raise RuntimeError('Missing tools')
   if {norm(x):sha(Path(x)) for x in [compiler,dumpbin,str(VCVARS)]}!={norm(x):v for x,v in toolsets[arch].items()}:raise RuntimeError('Resolved tools differ')
   environments[arch]=(env,compiler,dumpbin)
  env,compiler,dumpbin=environments[arch]
  target=OUT/u['name'];target.mkdir();obj=target/(u['name']+'.obj')
  flags=['/nologo','/c','/W4','/WX','/EHsc','/Y-','/showIncludes','/MTd','/Od','/Ob0','/DWIN32','/D_WIN32_WINNT=0x0601','/FI'+str(INPUT/('require-'+arch+'.h'))]
  if u['sdk']:flags+=['/I'+str(SDK.parent)]
  command=[compiler]+flags+[str(INPUT/'candidate'/u['source']),'/Fo'+str(obj)]
  record={'unit':u['name'],'source':u['source'],'arch':arch,'command':command,'cwd':str(target),'status':'pending'}
  receipt['builds'].append(record);save();(target/'command.json').write_text(json.dumps(command,indent=2)+'\n')
  try:p=subprocess.run(command,cwd=target,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
  except subprocess.TimeoutExpired as e:(target/'compile.log').write_bytes(e.stdout or b'');raise
  (target/'compile.log').write_bytes(p.stdout);lines=p.stdout.decode(errors='replace').splitlines();includes={};ancestry=[];stack=[]
  for line in lines:
   match=re.match(r'^Note: including file:(\s+)(.+?)\s*$',line)
   if match:
    depth=len(match.group(1));path=Path(match.group(2)).resolve();key=norm(path);includes[key]=sha(path)
    while stack and stack[-1][0]>=depth:stack.pop()
    ancestry.append({'path':key,'depth':depth,'ancestors':[x[1] for x in stack]});stack.append((depth,key))
  (target/'actual-includes.json').write_text(json.dumps(includes,indent=2)+'\n');(target/'include-ancestry.json').write_text(json.dumps(ancestry,indent=2)+'\n')
  record.update(exit_code=p.returncode,diagnostics=[x for x in lines if re.search(r'\b(?:warning|error|fatal error) [A-Z]\d+',x)])
  if p.returncode:record['status']='compile-failed';raise RuntimeError(u['name']+' compile failed')
  machine=struct.unpack_from('<H',obj.read_bytes())[0];record.update(machine=hex(machine),object_sha256=sha(obj))
  if machine!={'x86':0x14c,'amd64':0x8664}[arch] or record['diagnostics']:raise RuntimeError('Machine/diagnostic concern')
  # Actual selected headers, including73 registry wherever transitive, must match.
  for rel in u['quoted_headers']:
   if includes.get(norm(INPUT/'candidate'/rel))!=manifest['inputs/candidate/'+rel]:raise RuntimeError('Pinned local header absent: '+rel)
  if (norm(SDK) in includes)!=u['sdk']:raise RuntimeError('SDK inclusion partition mismatch')
  if any('/stlport453/' in x or '/src/engine/' in x or ('/snapshot/' in x and '/library/miles/include/' not in x) for x in includes):raise RuntimeError('Engine/STLport/unapproved snapshot header')
  command=[dumpbin,'/symbols',str(obj)];(target/'symbols-command.json').write_text(json.dumps(command,indent=2)+'\n')
  p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env,timeout=45);(target/'symbols.log').write_bytes(p.stdout)
  symbols=undefined_symbols(p.stdout.decode(errors='replace'));record['undefined_symbols']=symbols
  if p.returncode:raise RuntimeError('dumpbin failure')
  ail=[s for s in symbols if 'AIL_' in s];names=[]
  for symbol in ail:
   m=re.fullmatch(r'__imp__(AIL_\w+)@(\d+)',symbol)
   if not m:raise RuntimeError('Unexpected AIL import decoration: '+symbol)
   names.append(m.group(1))
  if set(names)!=set(u['exact_ail_names']):raise RuntimeError('Exact AIL import name set differs')
  record['ail_imports']=ail
  if u['source']=='backend-boundary24/pipe/ClientMilesPipe.cpp':
   expected=json.loads((INPUT/'public-delegates.json').read_text())
   observed={m.group(1) for x in symbols for m in [re.match(r'^\?([^@]+)@ClientMilesPipeCore57@@',x)] if m}
   if observed!=set(expected):raise RuntimeError('Guarded public delegate set differs')
   for prefix in ['?requireFatalReporter@ClientMilesPrivate52@@','?fail@ClientMilesPrivate52@@','?requireForwardAllowed@MilesCallbackGuard47@@']:
    if not any(x.startswith(prefix) for x in symbols):raise RuntimeError('Public guard dependency absent')
  if any(not any(x.startswith(prefix) for x in symbols) for prefix in required.get(u['source'],[])):raise RuntimeError('Required real dependency absent')
  if any('canonicalServices' in x for x in symbols):raise RuntimeError('Unexpected canonical service fallback')
  record['status']='compiled';save()
except Exception as e:receipt['failure']={'type':type(e).__name__,'message':str(e)}
finally:
 for label,root,expected in [('inputs_after',ROOT,manifest),('reused35_after',REUSED,reused),('tools_after',Path('.'),alltools)]:
  try:actual=verify(root,expected);receipt[label+'_unchanged']=True
  except Exception as e:actual={'error':str(e)};receipt[label+'_unchanged']=False
  (OUT/(label+'.json')).write_text(json.dumps(actual,indent=2)+'\n')
 receipt['passed']=not receipt.get('failure') and all(receipt[k+'_unchanged'] for k in ['inputs_after','reused35_after','tools_after']) and len(receipt['builds'])==35 and all(x['status']=='compiled' for x in receipt['builds'])
 save()
sys.exit(0 if receipt['passed'] else 1)
