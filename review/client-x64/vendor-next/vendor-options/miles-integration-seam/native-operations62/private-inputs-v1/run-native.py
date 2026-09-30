#!/usr/bin/env python3
"""Prospective v120 Win32+AMD64 object-only gate; requires parent approval."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,subprocess,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from symbol_parser import undefined_symbols,defined_symbols,has_required,no_miles_imports
if os.name!='nt' or sys.argv[1:]!=['--approved-two-objects']:
    raise SystemExit('Windows and explicit approved two-object invocation required')
ROOT=Path('C:/native-operations62');OUT=ROOT/'results'
VCVARS=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
UNITS={'amd64':[('plain-operations','plain_operations.cpp'),('native-calls','native/native_calls60.cpp')]}
ARCHES=[('amd64',0x8664)]
EXPECTED_MILES={'__imp_AIL_active_sample_count', '__imp_AIL_sample_position', '__imp_AIL_stop_sample', '__imp_AIL_set_stream_ms_position', '__imp_AIL_digital_latency', '__imp_AIL_set_sample_loop_block', '__imp_AIL_set_listener_3D_orientation', '__imp_AIL_set_sample_ms_position', '__imp_AIL_open_stream', '__imp_AIL_set_3D_rolloff_factor', '__imp_AIL_set_sample_3D_velocity_vector', '__imp_AIL_set_stream_loop_count', '__imp_AIL_file_type', '__imp_AIL_digital_CPU_percent', '__imp_AIL_set_sample_loop_count', '__imp_AIL_set_sample_file', '__imp_AIL_set_sample_position', '__imp_AIL_set_stream_loop_block', '__imp_AIL_unlock', '__imp_AIL_set_sample_volume_levels', '__imp_AIL_release_sample_handle', '__imp_AIL_set_room_type', '__imp_AIL_set_sample_reverb_levels', '__imp_AIL_sample_volume_levels', '__imp_AIL_WAV_info', '__imp_AIL_allocate_sample_handle', '__imp_AIL_start_stream', '__imp_AIL_set_listener_3D_velocity_vector', '__imp_AIL_stream_sample_handle', '__imp_AIL_sample_ms_position', '__imp_AIL_set_listener_3D_position', '__imp_AIL_set_sample_playback_rate', '__imp_AIL_sample_reverb_levels', '__imp_AIL_set_named_sample_file', '__imp_AIL_close_stream', '__imp_AIL_set_sample_3D_position', '__imp_AIL_lock', '__imp_AIL_sample_playback_rate', '__imp_AIL_room_type', '__imp_AIL_file_error', '__imp_AIL_end_sample', '__imp_AIL_set_sample_occlusion', '__imp_AIL_serve', '__imp_AIL_set_sample_3D_distances', '__imp_AIL_stream_ms_position', '__imp_AIL_stream_status', '__imp_AIL_get_timer_highest_delay', '__imp_AIL_sample_status', '__imp_AIL_start_sample', '__imp_AIL_set_sample_obstruction'}
DELEGATES=['WAV_info', 'active_sample_count', 'allocate_sample_handle', 'close_stream', 'digital_CPU_percent', 'digital_latency', 'end_sample', 'file_error', 'file_type', 'get_timer_highest_delay', 'lock', 'open_stream', 'release_sample_handle', 'room_type', 'sample_ms_position', 'sample_playback_rate', 'sample_position', 'sample_reverb_levels', 'sample_status', 'sample_volume_levels', 'serve', 'set_3D_rolloff_factor', 'set_listener_3D_orientation', 'set_listener_3D_position', 'set_listener_3D_velocity_vector', 'set_named_sample_file', 'set_room_type', 'set_sample_3D_distances', 'set_sample_3D_position', 'set_sample_3D_velocity_vector', 'set_sample_file', 'set_sample_loop_block', 'set_sample_loop_count', 'set_sample_ms_position', 'set_sample_obstruction', 'set_sample_occlusion', 'set_sample_playback_rate', 'set_sample_position', 'set_sample_reverb_levels', 'set_sample_volume_levels', 'set_stream_loop_block', 'set_stream_loop_count', 'set_stream_ms_position', 'start_sample', 'start_stream', 'stop_sample', 'stream_ms_position', 'stream_sample_handle', 'stream_status', 'unlock']
REQUIRED_UNDEFINED={'plain-operations':['?'+n+'@ClientMilesNativeCalls60@@' for n in DELEGATES]+['?requireFatalReporter@ClientMilesPrivate52@@','?fail@ClientMilesPrivate52@@'],'native-calls':list(EXPECTED_MILES)}
REQUIRED_DEFINED={'plain-operations':['?'+n+'@ClientMiles@@' for n in DELEGATES],'native-calls':['?'+n+'@ClientMilesNativeCalls60@@' for n in DELEGATES]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(p):return str(p).replace('\\','/').lower()
m=json.loads((ROOT/'input-manifest.json').read_text())
for name,value in m['sha256'].items():
    if sha(ROOT/name)!=value:raise RuntimeError('Input identity mismatch: '+name)
expected_tools=json.loads((ROOT/'toolchain.json').read_text());OUT.mkdir(exist_ok=False)
r={'expected_objects':2,'linked':False,'executed':False,'sdk_declaration_types_checked':False,'builds':[],
   'input_manifest_sha256':sha(ROOT/'input-manifest.json'),'tools':{},
   'policy':'one matrix, stop first compile/header/COFF/symbol failure; no retry',
   'header_hashes':'single-time include observations, not before/after header attestation',
   'inlining':'native54 modern /MT /O2 with explicit /Ob0; no warning or exception policy relaxation',
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
            command=[cl]+flags+(['/I'+str(ROOT/'sdk')] if name=='native-calls' else [])+['/FI'+str(ROOT/('require-v120-'+arch+'.h')),'/Fd'+str(out/(name+'.pdb')),str(source),'/Fo'+str(obj)]
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
            forbidden=[x for x in paths if '/stlport' in x or '/src/engine/' in x or '/snapshot/' in x or (x.endswith('/mss.h') and (name!='native-calls' or x!=sdkpath))]
            required_headers=['candidate/ClientMiles.h','candidate/private/native_calls60.h']
            if name=='plain-operations':required_headers+=['candidate/private/failure_boundary.h']
            if name=='native-calls':required_headers+=['sdk/Mss.h']
            missing=[n for n in required_headers if paths.get(norm(ROOT/n))!=m['sha256'][n]]
            if not any('/vc/include/' in x for x in paths):missing.append('actual MSVC includes')
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
            wanted=EXPECTED_MILES if name=='native-calls' else set()
            if miles!=wanted:raise RuntimeError('Exact SDK import set mismatch: '+repr(miles))
            if name=='plain-operations':
                observed_delegates={match.group(1) for symbol in undef for match in [re.match(r'^\?([^@]+)@ClientMilesNativeCalls60@@',symbol)] if match}
                if observed_delegates!=set(DELEGATES):raise RuntimeError('Exact private delegate reference set mismatch')
            if name=='native-calls':r['sdk_declaration_types_checked']=True
            if not has_required(undef,REQUIRED_UNDEFINED[name]) or not has_required(defined,REQUIRED_DEFINED[name]):
                row['status']='required-symbol-missing';raise RuntimeError(arch+'/'+name+' required native symbols missing')
            row['status']='compiled';save();print(json.dumps({'architecture':arch,'unit':name,'status':row['status']}),flush=True)
except Exception as error:r['failure']={'type':type(error).__name__,'message':str(error)}
finally:
    after_tools={arch:{n:sha(Path(n)) for n in toolset} for arch,toolset in expected_tools.items()}
    r['tools_after']=after_tools;r['tools_unchanged']=after_tools==expected_tools
    after={n:sha(ROOT/n) for n in m['sha256']};(OUT/'inputs-after.json').write_text(json.dumps(after,indent=2)+'\n')
    r['inputs_unchanged']=after==m['sha256']
    r['passed']=not r.get('failure') and r['inputs_unchanged'] and r['tools_unchanged'] and len(r['builds'])==2 and all(x['status']=='compiled' for x in r['builds'])
    save()
sys.exit(0 if r['passed'] else 1)
