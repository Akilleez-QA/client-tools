#!/usr/bin/env python3
"""Prospective v120 Win32+AMD64 object-only gate; requires parent approval."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from symbol_parser import undefined_symbols,defined_symbols,has_required,no_miles_imports
if os.name!='nt' or sys.argv[1:]!=['--approved-six-objects']:
    raise SystemExit('Windows and explicit approved six-object invocation required')
ROOT=Path('C:/native-host49');OUT=ROOT/'results'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
UNITS=[('file-tokens','host-file-consumption49/file_tokens.cpp'),
       ('reply-transaction','host-file-consumption49/reply_transaction.cpp'),
       ('file-protocol','callback-protocol48/file_protocol.cpp')]
ARCHES=[('x86',0x14c),('amd64',0x8664)]
REQUIRED_UNDEFINED={
 'file-tokens':[],
 'reply-transaction':['?reserveOpen@FileTokens@MilesHostFiles49@@','?cancelOpen@FileTokens@MilesHostFiles49@@',
  '?resolve@FileTokens@MilesHostFiles49@@','?publishOpen@FileTokens@MilesHostFiles49@@',
  '?beginClose@FileTokens@MilesHostFiles49@@','?finishClose@FileTokens@MilesHostFiles49@@',
  '?decodeReply@MilesFileChannel26@@','?copyRead@MilesFileChannel26@@',
  '?expectFileAck@MilesFileProtocol48@@','?encodeFileConsumptionAck@MilesFileProtocol48@@'],
 'file-protocol':['?encodeCallInto@MilesTransport@@','?decodeCall@MilesTransport@@',
  '?encodeResultInto@MilesTransport@@','?decodeResult@MilesTransport@@',
  '?valid@Request@MilesFileChannel26@@','?header@Request@MilesFileChannel26@@']}
REQUIRED_DEFINED={
 'file-tokens':['?reserveOpen@FileTokens@MilesHostFiles49@@','?publishOpen@FileTokens@MilesHostFiles49@@',
  '?resolve@FileTokens@MilesHostFiles49@@','?finishClose@FileTokens@MilesHostFiles49@@',
  '?reserve@ResourceRegistry@MilesTransport@@','?publish@ResourceRegistry@MilesTransport@@',
  '?cancel@ResourceRegistry@MilesTransport@@','?resolve@ResourceRegistry@MilesTransport@@',
  '?beginClose@ResourceRegistry@MilesTransport@@','?retire@ResourceRegistry@MilesTransport@@'],
 'reply-transaction':['?consume@ReplyTransaction@MilesHostFiles49@@','?ack@ReplyTransaction@MilesHostFiles49@@',
  '?observeAckWriteComplete@ReplyTransaction@MilesHostFiles49@@','?result@ReplyTransaction@MilesHostFiles49@@'],
 'file-protocol':['?encodeInstall@MilesFileProtocol48@@','?decodeInstallReply@MilesFileProtocol48@@',
  '?encodeFileConsumptionAck@MilesFileProtocol48@@','?validateFileConsumptionAck@MilesFileProtocol48@@',
  '?decodeStreamAliasSuccess@MilesFileProtocol48@@']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(p):return str(p).replace('\\','/').lower()
m=json.loads((ROOT/'input-manifest.json').read_text())
for name,value in m['sha256'].items():
    if sha(ROOT/name)!=value:raise RuntimeError('Input identity mismatch: '+name)
expected_tools=json.loads((ROOT/'toolchain.json').read_text());OUT.mkdir(exist_ok=False)
r={'expected_objects':6,'linked':False,'executed':False,'sdk_thunk_abi_checked':False,'builds':[],
   'input_manifest_sha256':sha(ROOT/'input-manifest.json'),'tools':{},
   'policy':'one matrix, stop first compile/header/COFF/symbol failure; no retry',
   'header_hashes':'single-time include observations, not before/after header attestation',
   'inlining':'/Ob0 replaces native47 /Ob1 to expose used inline registry definitions',
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
        for name,rel in UNITS:
            out=archout/name;out.mkdir();source=ROOT/'candidate'/rel;obj=out/(name+'.obj')
            command=[cl]+flags+['/FI'+str(ROOT/('require-v120-'+arch+'.h')),'/Fd'+str(out/(name+'.pdb')),str(source),'/Fo'+str(obj)]
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
            forbidden=[x for x in paths if '/stlport' in x or '/src/engine/' in x or '/snapshot/' in x or x.endswith('/mss.h')]
            required_headers=['transport-candidate/resource_registry.h','protocol-candidate/miles_wire.h']
            if name!='file-tokens':required_headers+=['file-channel26/file_channel.h','callback-protocol48/file_protocol.h']
            missing=[n for n in required_headers if paths.get(norm(ROOT/'candidate'/n))!=m['sha256']['candidate/'+n]]
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
            if not no_miles_imports(undef):raise RuntimeError('Unexpected Miles SDK reference')
            if not has_required(undef,REQUIRED_UNDEFINED[name]) or not has_required(defined,REQUIRED_DEFINED[name]):
                row['status']='required-symbol-missing';raise RuntimeError(arch+'/'+name+' required native symbols missing')
            row['status']='compiled';save();print(json.dumps({'architecture':arch,'unit':name,'status':row['status']}),flush=True)
except Exception as error:r['failure']={'type':type(error).__name__,'message':str(error)}
finally:
    after_tools={arch:{n:sha(Path(n)) for n in toolset} for arch,toolset in expected_tools.items()}
    r['tools_after']=after_tools;r['tools_unchanged']=after_tools==expected_tools
    after={n:sha(ROOT/n) for n in m['sha256']};(OUT/'inputs-after.json').write_text(json.dumps(after,indent=2)+'\n')
    r['inputs_unchanged']=after==m['sha256']
    r['passed']=not r.get('failure') and r['inputs_unchanged'] and r['tools_unchanged'] and len(r['builds'])==6 and all(x['status']=='compiled' for x in r['builds'])
    save()
sys.exit(0 if r['passed'] else 1)
