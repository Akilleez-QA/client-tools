#!/usr/bin/env python3
"""Prospective v120 Win32+AMD64 object-only gate; requires parent approval."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from symbol_parser import undefined_symbols,defined_symbols,has_required,no_miles_imports
if os.name!='nt' or sys.argv[1:]!=['--approved-five-objects']:
    raise SystemExit('Windows and explicit approved five-object invocation required')
ROOT=Path('C:/native-runtime58');OUT=ROOT/'results'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
UNITS={
 'x86':[('host-runtime','host/host-runtime50/host_file_runtime.cpp'),
        ('host-thunks','host/host-runtime50/host_sdk_callbacks.cpp'),
        ('host-install','host/host-runtime50/host_install.cpp')],
 'amd64':[('client-runtime','client/client-runtime53/client_file_runtime.cpp'),
          ('client-mapper','client/callback-control45/host_association_mapper.cpp')]}
ARCHES=[('x86',0x14c),('amd64',0x8664)]
REQUIRED_UNDEFINED={
 'host-runtime':['?snapshot@MilesHostContext@@','?resolve@FileTokens@MilesHostFiles49@@',
  '?beginSend@ReplyTransaction@MilesHostFiles49@@','?consume@ReplyTransaction@MilesHostFiles49@@',
  '?ack@ReplyTransaction@MilesHostFiles49@@','?observeAckWriteComplete@ReplyTransaction@MilesHostFiles49@@',
  '?result@ReplyTransaction@MilesHostFiles49@@','?send@Endpoint@MilesPipe@@','?pump@Endpoint@MilesPipe@@',
  '?encodeCall@MilesTransport@@','?decodeRequest@MilesFileChannel26@@'],
 'host-thunks':['__imp__AIL_set_file_callbacks@16','?invoke@Runtime@MilesHostRuntime50@@'],
 'host-install':['?decodeInstall@MilesFileProtocol48@@','?encodeInstallReply@MilesFileProtocol48@@',
  '?installSdkCallbacks@MilesHostRuntime50@@','??0Scope@MilesHostContext@@'],
 'client-runtime':['?create@EngineFileWorker@MilesFileExecutor30@@','?start@EngineFileWorker@MilesFileExecutor30@@',
  '?retain@MilesSelectedFileServices44@@','?receiveControl@HostAssociationMapper@MilesFileOwner36@@',
  '?publishCommand@HostAssociationMapper@MilesFileOwner36@@','?observeForwardReturn@HostAssociationMapper@MilesFileOwner36@@',
  '?nextUnqueuedReply@HostAssociationMapper@MilesFileOwner36@@','?markReplyQueued@HostAssociationMapper@MilesFileOwner36@@',
  '?send@Endpoint@MilesPipe@@','?pump@Endpoint@MilesPipe@@'],
 'client-mapper':['?receive@SessionFileOwner@MilesFileOwner36@@','?acknowledge@SessionFileOwner@MilesFileOwner36@@',
  '?poll@SessionFileOwner@MilesFileOwner36@@','?expectFileAck@MilesFileProtocol48@@',
  '?validateFileConsumptionAck@MilesFileProtocol48@@']}
REQUIRED_DEFINED={
 'host-runtime':['?invoke@Runtime@MilesHostRuntime50@@','?fatal@MilesHostRuntime50@@'],
 'host-thunks':['?installSdkCallbacks@MilesHostRuntime50@@'],
 'host-install':['?installAdmitted@MilesHostRuntime50@@'],
 'client-runtime':['?launch@Runtime@MilesClientRuntime53@@','?publish@Runtime@MilesClientRuntime53@@',
  '?prepare@Runtime@MilesClientRuntime53@@','?returned@Runtime@MilesClientRuntime53@@'],
 'client-mapper':['?nextUnqueuedReply@HostAssociationMapper@MilesFileOwner36@@',
  '?receiveControl@HostAssociationMapper@MilesFileOwner36@@']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(p):return str(p).replace('\\','/').lower()
m=json.loads((ROOT/'input-manifest.json').read_text())
for name,value in m['sha256'].items():
    if sha(ROOT/name)!=value:raise RuntimeError('Input identity mismatch: '+name)
expected_tools=json.loads((ROOT/'toolchain.json').read_text());OUT.mkdir(exist_ok=False)
r={'expected_objects':5,'linked':False,'executed':False,'sdk_thunk_abi_checked':False,'builds':[],
   'input_manifest_sha256':sha(ROOT/'input-manifest.json'),'tools':{},
   'policy':'one matrix, stop first compile/header/COFF/symbol failure; no retry',
   'header_hashes':'single-time include observations, not before/after header attestation',
   'inlining':'inherited native-host49 /Od /Ob0; preserve actual object references',
   'reused_objects':[]}
def save():(OUT/'results.json').write_text(json.dumps(r,indent=2)+'\n')
try:
    flags=json.loads((ROOT/'flags.json').read_text())
    for arch,machine in ARCHES:
        archout=OUT/arch;archout.mkdir()
        setup=archout/'environment.cmd';setup.write_text('@echo off\ncall "'+str(VCVARS)+'" '+arch+' >nul\nif errorlevel 1 exit /b %errorlevel%\nset\n')
        p=subprocess.run(['cmd','/d','/c',str(setup)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45)
        if p.returncode:raise RuntimeError('vcvars failed: '+arch)
        env={k.upper():v for k,v in os.environ.items()}
        for line in p.stdout.decode(errors='replace').splitlines():
            if '=' in line and not line.startswith('='):
                k,v=line.split('=',1);env[k.upper()]=v
        cl=shutil.which('cl.exe',path=env['PATH']);dumpbin=shutil.which('dumpbin.exe',path=env['PATH'])
        if not cl or not dumpbin:raise RuntimeError('Selected tools missing: '+arch)
        observed={str(p):sha(p) for p in [Path(cl),Path(dumpbin),VCVARS]};r['tools'][arch]=observed;save()
        if {norm(k):v for k,v in observed.items()}!={norm(k):v for k,v in expected_tools[arch].items()}:
            raise RuntimeError('Selected tool identity differs from read-only probe: '+arch)
        for name,rel in UNITS[arch]:
            out=archout/name;out.mkdir();source=ROOT/'candidate'/rel;obj=out/(name+'.obj')
            command=[cl]+flags+(['/I'+str(ROOT/'sdk')] if name=='host-thunks' else [])+['/FI'+str(ROOT/('require-v120-'+arch+'.h')),'/Fd'+str(out/(name+'.pdb')),str(source),'/Fo'+str(obj)]
            (out/'command.json').write_text(json.dumps(command,indent=2)+'\n')
            row={'architecture':arch,'unit':name,'source':rel,'command':command,'cwd':str(out),'status':'pending'};r['builds'].append(row);save()
            try:p=subprocess.run(command,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
            except subprocess.TimeoutExpired as error:
                (out/'compile.log').write_bytes(error.stdout or b'');row['status']='timeout';raise
            (out/'compile.log').write_bytes(p.stdout);lines=p.stdout.decode(errors='replace').splitlines();includes={}
            for line in lines:
                match=re.match(r'^Note: including file:\s*(.+?)\s*$',line)
                if match:
                    path=Path(match.group(1)).resolve();includes[str(path)]=sha(path)
            (out/'actual-includes.json').write_text(json.dumps(includes,indent=2)+'\n')
            paths={norm(x):h for x,h in includes.items()}
            sdkpath=norm(ROOT/'sdk/Mss.h')
            forbidden=[x for x in paths if '/stlport' in x or '/src/engine/' in x or '/snapshot/' in x or (x.endswith('/mss.h') and (name!='host-thunks' or x!=sdkpath))]
            branch='host' if arch=='x86' else 'client'
            required_headers=['candidate/'+branch+'/protocol-candidate/miles_wire.h',
                'candidate/'+branch+'/file-channel26/file_channel.h',
                'candidate/'+branch+'/callback-protocol48/file_protocol.h']
            if branch=='host':required_headers+=['candidate/host/host-runtime50/host_file_runtime.h']
            else:required_headers+=['candidate/client/callback-control45/host_association_mapper.h']
            if name=='host-thunks':required_headers+=['sdk/Mss.h']
            missing=[n for n in required_headers if paths.get(norm(ROOT/n))!=m['sha256'][n]]
            if not any('/vc/include/' in x and x.endswith('/memory') for x in paths):missing.append('actual MSVC modern <memory>')
            row.update(exit_code=p.returncode,diagnostics=[x for x in lines if re.search(r'\b(?:warning|error|fatal error) [A-Z]\d+',x)],
                forbidden_includes=forbidden,missing_pinned_includes=missing,actual_includes_sha256=sha(out/'actual-includes.json'))
            if p.returncode:row['status']='compile-failed';raise RuntimeError(arch+'/'+name+' compile failed')
            if forbidden or missing:row['status']='header-boundary-failed';raise RuntimeError(arch+'/'+name+' header mismatch')
            row.update(object_sha256=sha(obj),coff_machine=hex(struct.unpack_from('<H',obj.read_bytes())[0]))
            if row['coff_machine']!=hex(machine):row['status']='wrong-machine';raise RuntimeError('Wrong COFF machine')
            command=[dumpbin,'/symbols',str(obj)];(out/'symbols-command.json').write_text(json.dumps(command,indent=2)+'\n')
            p=subprocess.run(command,cwd=out,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=45);(out/'symbols.log').write_bytes(p.stdout)
            text=p.stdout.decode(errors='replace');undef=undefined_symbols(text);defined=defined_symbols(text)
            row['undefined_symbols']=undef;row['defined_symbols']=defined
            if p.returncode:raise RuntimeError('dumpbin failed')
            miles={symbol for symbol in undef if 'AIL_' in symbol}
            wanted={'__imp__AIL_set_file_callbacks@16'} if name=='host-thunks' else set()
            if miles!=wanted:raise RuntimeError('Exact SDK import set mismatch: '+repr(miles))
            if name=='host-thunks':r['sdk_thunk_abi_checked']=True
            if not has_required(undef,REQUIRED_UNDEFINED[name]) or not has_required(defined,REQUIRED_DEFINED[name]):
                row['status']='required-symbol-missing';raise RuntimeError(arch+'/'+name+' required native symbols missing')
            row['status']='compiled';save();print(json.dumps({'architecture':arch,'unit':name,'status':row['status']}),flush=True)
except Exception as error:r['failure']={'type':type(error).__name__,'message':str(error)}
finally:
    after_tools={arch:{n:sha(Path(n)) for n in toolset} for arch,toolset in expected_tools.items()}
    r['tools_after']=after_tools;r['tools_unchanged']=after_tools==expected_tools
    after={n:sha(ROOT/n) for n in m['sha256']};(OUT/'inputs-after.json').write_text(json.dumps(after,indent=2)+'\n')
    r['inputs_unchanged']=after==m['sha256']
    r['passed']=not r.get('failure') and r['inputs_unchanged'] and r['tools_unchanged'] and len(r['builds'])==5 and all(x['status']=='compiled' for x in r['builds'])
    save()
sys.exit(0 if r['passed'] else 1)
