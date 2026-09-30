#!/usr/bin/env python3
"""Proposed v120 AMD64 object-only gate; execute only after root identity approval."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
if os.name!='nt' or sys.argv[1:]!=['--approved-compile-only']:
 raise SystemExit('Windows and explicit approved compile-only invocation required')
ROOT=Path('C:/native38-owner');OUT=ROOT/'results'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
UNITS=[('owner','file-owner36/session_file_owner.cpp'),('actual-job','file-executor33/FileInvocationJob.cpp'),('file-channel','file-channel26/file_channel.cpp'),('codec','transport-candidate/codec.cpp'),('coordinator','session-file-admission34/coordinator.cpp'),('host-context','host-callback-context41/call_context.cpp')]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((ROOT/'input-manifest.json').read_text())
for n,v in m['sha256'].items():
 if sha(ROOT/n)!=v:raise RuntimeError('Input identity mismatch: '+n)
OUT.mkdir(exist_ok=False)
r={'expected_objects':len(UNITS),'linked':False,'executed':False,'builds':[],
 'input_manifest_sha256':sha(ROOT/'input-manifest.json'),
 'policy':'stop first compile/header/COFF/import failure; no retry',
 'header_hashes':'single-time compile observations, not before/after header attestation'}
def save():(OUT/'results.json').write_text(json.dumps(r,indent=2)+'\n')
try:
 setup=OUT/'environment.cmd';setup.write_text('@echo off\ncall "'+str(VCVARS)+'" amd64 >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n')
 p=subprocess.run(['cmd','/d','/c',str(setup)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
 if p.returncode:raise RuntimeError('vcvars failed')
 env={k.upper():v for k,v in os.environ.items()}
 for line in p.stdout.decode(errors='replace').splitlines():
  if '=' in line and not line.startswith('='):
   k,v=line.split('=',1);env[k.upper()]=v
 cl=shutil.which('cl.exe',path=env['PATH']);dumpbin=shutil.which('dumpbin.exe',path=env['PATH'])
 if not cl or not dumpbin:raise RuntimeError('Native tools missing')
 r['tools']={str(p):sha(p) for p in [Path(cl),Path(dumpbin),VCVARS]}
 flags=json.loads((ROOT/'flags.json').read_text())
 for name,rel in UNITS:
  out=OUT/name;out.mkdir();source=ROOT/'candidate'/rel;obj=out/(name+'.obj')
  command=[cl]+flags+['/FI'+str(ROOT/'require-v120.h'),'/Fd'+str(out/(name+'.pdb')),str(source),'/Fo'+str(obj)]
  (out/'command.json').write_text(json.dumps(command,indent=2)+'\n')
  row={'unit':name,'source':rel,'command':command,'cwd':str(out),'status':'pending'};r['builds'].append(row);save()
  try:p=subprocess.run(command,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
  except subprocess.TimeoutExpired as error:
   (out/'compile.log').write_bytes(error.stdout or b'');row['status']='timeout';raise
  (out/'compile.log').write_bytes(p.stdout);lines=p.stdout.decode(errors='replace').splitlines();includes={}
  for line in lines:
   match=re.match(r'^Note: including file:\s*(.+?)\s*$',line)
   if match:
    path=Path(match.group(1)).resolve();includes[str(path)]=sha(path)
  (out/'actual-includes.json').write_text(json.dumps(includes,indent=2)+'\n')
  paths=[x.replace('\\','/').lower() for x in includes]
  forbidden=[x for x in paths if '/stlport' in x or '/src/engine/' in x or '/snapshot/' in x or x.endswith('/mss.h')]
  row.update(exit_code=p.returncode,diagnostics=[x for x in lines if re.search(r'\b(?:warning|error|fatal error) [A-Z]\d+',x)],forbidden_includes=forbidden,actual_includes_sha256=sha(out/'actual-includes.json'))
  if p.returncode:row['status']='compile-failed';raise RuntimeError(name+' compile failed')
  if forbidden:row['status']='header-boundary-failed';raise RuntimeError(name+' header boundary failed')
  row.update(object_sha256=sha(obj),coff_machine=hex(struct.unpack_from('<H',obj.read_bytes())[0]))
  if row['coff_machine']!='0x8664':row['status']='wrong-machine';raise RuntimeError('Wrong COFF machine')
  command=[dumpbin,'/symbols',str(obj)];(out/'symbols-command.json').write_text(json.dumps(command,indent=2)+'\n')
  p=subprocess.run(command,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45);(out/'symbols.log').write_bytes(p.stdout)
  undef=[line.split()[-1] for line in p.stdout.decode(errors='replace').splitlines() if 'UNDEF' in line and '|' in line]
  row['undefined_symbols']=undef
  if p.returncode:raise RuntimeError('dumpbin failed')
  if any('AIL_' in x for x in undef):raise RuntimeError('Unexpected direct SDK reference')
  required={'owner':['?enqueueAdmitted@FileInvocationJob@MilesFileExecutor30@@'],
            'actual-job':['?submit@EngineFileWorker@MilesFileExecutor30@@','?canonicalServices@MilesFileChannel26@@']}.get(name,[])
  if any(not any(x.startswith(fragment) for x in undef) for fragment in required):
   row['status']='required-reference-missing';raise RuntimeError(name+' actual dependency reference missing')
  row['status']='compiled';save();print(json.dumps({'unit':name,'status':row['status'],'exit_code':row['exit_code']}),flush=True)
except Exception as error:r['failure']={'type':type(error).__name__,'message':str(error)}
finally:
 after={n:sha(ROOT/n) for n in m['sha256']};(OUT/'inputs-after.json').write_text(json.dumps(after,indent=2)+'\n')
 r['inputs_unchanged']=after==m['sha256'];r['passed']=not r.get('failure') and r['inputs_unchanged'] and len(r['builds'])==len(UNITS) and all(x['status']=='compiled' for x in r['builds']);save()
sys.exit(0 if r['passed'] else 1)
