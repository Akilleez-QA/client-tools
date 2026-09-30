#!/usr/bin/env python3
"""Proposed native object-only gate. Execute only after parent identity approval."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
ROOT=Path('C:/file-executor31')
SNAPSHOT=ROOT/'snapshot'
PROJECT=SNAPSHOT/'src/engine/client/library/clientAudio/build/win32'
OUT=ROOT/'results'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
UNITS=[('engine-worker','seam/file-executor31/EngineFileWorker.cpp',True),
       ('invocation-job','seam/file-executor31/FileInvocationJob.cpp',False),
       ('file-channel','seam/file-channel26/file_channel.cpp',False),
       ('canonical-services','seam/file-channel26/canonical_services.cpp',False),
       ('codec','seam/transport-candidate/codec.cpp',False)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'input-manifest.json').read_text())
for relative,expected in manifest['sha256'].items():
 if sha(ROOT/relative)!=expected:raise RuntimeError('Input identity mismatch: '+relative)
OUT.mkdir(exist_ok=False)
results=[]
def save():
 (OUT/'results.json').write_text(json.dumps({'builds':results,'expected_count':20,'policy':'stop at first failed compile or include/COFF check; no retry'},indent=2)+'\n')
for configuration in ['Debug','Release']:
 for platform,arch,machine in [('Win32','x86',0x14c),('x64','amd64',0x8664)]:
  setup=OUT/(configuration+'-'+platform+'-environment.cmd')
  setup.write_text('@echo off\ncall "'+str(VCVARS)+'" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n')
  p=subprocess.run(['cmd','/d','/c',str(setup)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
  if p.returncode:raise RuntimeError('vcvars failed; no retry')
  env={k.upper():v for k,v in os.environ.items()}
  for line in p.stdout.decode(errors='replace').splitlines():
   if '=' in line and not line.startswith('='):
    k,v=line.split('=',1);env[k.upper()]=v
  compiler=shutil.which('cl.exe',path=env['PATH'])
  if not compiler:raise RuntimeError('Native v120 compiler missing')
  audit=ROOT/'inputs'/('clientAudio-'+configuration+'-'+platform+'.audit.log')
  rows=[line.strip().split('|') for line in audit.read_text(encoding='utf-8-sig').splitlines() if line.strip().startswith('CL|')]
  row=next(row for row in rows if row[1].replace('\\','/').endswith('/Audio.cpp'))
  definitions=['/D'+x for x in row[6].split(';') if x]
  engine_includes=['/I'+x for x in row[7].split(';') if x]
  for unit,relative,engine in UNITS:
   directory=OUT/(configuration+'-'+platform+'-'+unit);directory.mkdir()
   source=ROOT/relative;obj=directory/(unit+'.obj');guard=directory/'require-v120.h'
   guard.write_text('#if !defined(_MSC_VER) || _MSC_VER != 1800\n#error Native VS2013 v120 required\n#endif\n#define EXEC31_TEXT_INNER(x) #x\n#define EXEC31_TEXT(x) EXEC31_TEXT_INNER(x)\n#pragma message("EXEC31 _MSC_FULL_VER=" EXEC31_TEXT(_MSC_FULL_VER))\n')
   flags=['/nologo','/c','/EHsc','/Y-','/Gm-','/Zc:wchar_t-','/Zc:forScope','/GR','/Gy','/fp:precise','/W4','/Zi','/FC','/showIncludes','/FI'+str(guard),'/Fd'+str(directory/(unit+'.pdb'))]
   flags+=['/MTd','/Od','/Ob1','/RTC1','/WX'] if configuration=='Debug' else ['/MT','/O2','/Ob1','/Oi','/Ot','/Oy','/GF','/WX-']
   flags+=definitions
   if engine:flags+=engine_includes
   command=[compiler]+flags+[str(source),'/Fo'+str(obj)]
   (directory/'command.json').write_text(json.dumps(command,indent=2)+'\n')
   record={'configuration':configuration,'platform':platform,'unit':unit,'engine_stlport':engine,'source':str(source),'source_sha256':sha(source),'compiler':compiler,'compiler_sha256':sha(Path(compiler)),'audit_sha256':sha(audit),'cwd':str(PROJECT),'command':command,'status':'pending'}
   results.append(record);save()
   try:
    p=subprocess.run(command,cwd=PROJECT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
    code,output=p.returncode,p.stdout
   except subprocess.TimeoutExpired as error:
    code,output=-999,(error.stdout or b'')+b'\nTIMEOUT\n'
   (directory/'compile.log').write_bytes(output)
   includes={}
   lines=output.decode(errors='replace').splitlines()
   for line in lines:
    m=re.match(r'^Note: including file:\s*(.+?)\s*$',line)
    if m:
     path=Path(m.group(1)).resolve();includes[str(path)]=sha(path)
   (directory/'actual-includes.json').write_text(json.dumps(includes,indent=2)+'\n')
   names=[x.replace('\\','/').lower() for x in includes]
   has_stlport=any('/stlport453/' in x for x in names)
   has_snapshot=any('/file-executor31/snapshot/' in x for x in names)
   has_adapter=any('/seam/file-channel26/' in x or '/seam/transport-candidate/' in x for x in names)
   include_boundary=(has_stlport and not has_adapter) if engine else (not has_stlport and not has_snapshot)
   record.update(exit_code=code,diagnostics=[x for x in lines if re.search(r'\b(?:warning|error|fatal error) [A-Z]\d+',x)],actual_include_count=len(includes),actual_includes_sha256=sha(directory/'actual-includes.json'),include_boundary_ok=include_boundary,status='compile-failed' if code else 'compiled')
   if not code:
    data=obj.read_bytes();actual_machine=struct.unpack_from('<H',data)[0]
    record.update(object_sha256=sha(obj),object_bytes=len(data),coff_machine=hex(actual_machine))
    if actual_machine!=machine:record['status']='wrong-object-machine'
    elif not include_boundary:record['status']='stdlib-boundary-failed'
   save();print(json.dumps({k:record[k] for k in ['configuration','platform','unit','status','exit_code','include_boundary_ok']}),flush=True)
   if record['status']!='compiled':sys.exit(1)
sys.exit(0)
