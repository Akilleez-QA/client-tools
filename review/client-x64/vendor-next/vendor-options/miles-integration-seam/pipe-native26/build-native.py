"""Prospective parent-approved v120 x86/x64 object gate; never links or runs produced code."""
from pathlib import Path
import json, os, re, shutil, struct, sys
if os.name != 'nt' or sys.argv[1:] != ['--approved-compile-only']:
    raise SystemExit('Windows and explicit parent-approved compile-only invocation required')
root=Path('C:/pipe-native26');base=root/'pipe-native26'
sys.path.insert(0,str(root/'live-bridge-candidate/revision4-tools'))
from build_receipt import environment, identities, includes, run, exclusive_json
from receipt import digest
out=root/'native-v1';out.mkdir(exist_ok=False)
sdk=Path('C:/client-next-build/src/external/3rd/library/miles/include/Mss.h').resolve()
manifest=json.loads((base/'source-manifest.json').read_text())
files=[root/n for n in manifest]
result={'schema':'pipe-native26-object-gate-v1','linked':False,'executed':False,'groups':[],
        'python_sha256':digest(sys.executable)}
seven=['set_listener_3D_position','set_listener_3D_velocity_vector','set_listener_3D_orientation',
       'set_3D_rolloff_factor','serve','room_type','set_room_type']
groups=[('x86',0x14c,['pipe-native26/native/host_composition.cpp','host-candidate/host_dispatch.cpp']),
        ('amd64',0x8664,['backend-boundary24/pipe/ClientMilesPipe.cpp','backend-boundary24/pipe/LiveChannel.cpp',
                        'backend-boundary24/native/native_miles64.cpp','native-startup25/native/native_startup25.cpp',
                        'native-startup25/sample/install_order.cpp','native-startup25/tests/portable_contract.cpp'])]
try:
    for n,h in manifest.items():
        if digest(root/n)!=h:raise RuntimeError('source identity mismatch: '+n)
    result['inputs_before']=identities(files)
    if digest(sdk)!='966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':
        raise RuntimeError('private SDK identity mismatch')
    vc=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
    recorded={p.resolve() for p in files}
    for architecture,machine,sources in groups:
        dest=out/architecture;dest.mkdir()
        row={'architecture':architecture,'expected_machine':machine};result['groups'].append(row)
        env=environment(vc,architecture,dest)
        compiler=Path(shutil.which('cl.exe',path=env['PATH']))
        dumpbin=Path(shutil.which('dumpbin.exe',path=env['PATH']))
        tools={compiler,dumpbin,vc}
        tools.update(compiler.parent.glob('*.dll'));tools.update(compiler.parent.glob('1033/*.dll'))
        tools.update((vc.parent/'bin').glob('*.dll'));tools.update((vc.parent.parent/'Common7/IDE').glob('mspdb*.dll'))
        command=[str(compiler),'/nologo','/W4','/WX','/EHsc','/MT','/O2','/DWIN32',
                 '/D_WIN32_WINNT=0x0601','/I'+str(sdk.parent)]+[str(root/n) for n in sources]
        code,log=run(command+['/Zs','/showIncludes'],dest,'headers',env);row['discovery_exit']=code
        if code:raise RuntimeError(architecture+' header discovery failed')
        headers=includes(log)
        row['expected_sdk_includes']=bool(headers) and sdk in {p.resolve() for p in headers}
        if not row['expected_sdk_includes']:raise RuntimeError(architecture+' missing actual SDK include evidence')
        unrecorded=[]
        for p in headers:
            try:p.resolve().relative_to(root.resolve())
            except ValueError:continue
            if p.resolve() not in recorded:unrecorded.append(str(p))
        row['unrecorded_local_headers']=unrecorded
        if unrecorded:raise RuntimeError('unrecorded local include')
        row['before']={'inputs':identities(files),'headers':identities(headers),'tools':identities(tools)}
        code,log=run(command+['/c','/showIncludes'],dest,'objects',env);row['compile_exit']=code
        row['after']={'inputs':identities(files),'headers':identities(headers),'tools':identities(tools)}
        row['inputs_unchanged']=row['before']==row['after'] and includes(log)==headers
        if code:raise RuntimeError(architecture+' object compilation failed')
        if not row['inputs_unchanged']:raise RuntimeError(architecture+' input identities changed')
        row['objects']=[]
        for n in sources:
            p=dest/(Path(n).stem+'.obj');data=p.read_bytes()
            actual=struct.unpack('<H',data[:2])[0]
            row['objects'].append({'path':str(p),'sha256':digest(p),'machine':actual})
            if actual!=machine:raise RuntimeError('wrong COFF machine: '+str(p))
        def symbols(stem):
            code,text=run([str(dumpbin),'/symbols',str(dest/(stem+'.obj'))],dest,stem+'-symbols',env)
            if code:raise RuntimeError('dumpbin failed for '+stem)
            return text.splitlines()
        def imported(lines,name,x86=False):
            token='__imp__AIL_'+name+'@' if x86 else '__imp_AIL_'+name
            return any('UNDEF' in s and token in s for s in lines)
        def facade(lines,name,undefined):
            return any(('UNDEF' in s)==undefined and '?'+name+'@ClientMiles@@' in s for s in lines)
        if architecture=='x86':
            dispatch=symbols('host_dispatch');composition=symbols('host_composition')
            row['seven_real_imports']=all(imported(dispatch,n,True) for n in seven)
            row['composition_dispatch_reference']=any('UNDEF' in s and '?dispatch@MilesHost@@' in s for s in composition)
            row['symbol_oracle']=row['seven_real_imports'] and row['composition_dispatch_reference']
        else:
            pipe=symbols('ClientMilesPipe');native=symbols('native_startup25');sample=symbols('install_order')
            row['seven_facade_definitions']=all(facade(pipe,n,False) for n in seven)
            row['no_pipe_callback_definition']=not facade(pipe,'set_file_callbacks',False)
            row['eight_native_imports']=all(imported(native,n) for n in seven+['set_file_callbacks'])
            row['sample_callback_unresolved']=facade(sample,'set_file_callbacks',True)
            row['symbol_oracle']=all(row[n] for n in ['seven_facade_definitions','no_pipe_callback_definition',
                                                       'eight_native_imports','sample_callback_unresolved'])
        if not row['symbol_oracle']:raise RuntimeError(architecture+' symbol oracle failed')
except Exception as error:
    result['failure']={'type':type(error).__name__,'message':str(error)}
finally:
    result['inputs_after']=identities([p for p in files if p.is_file()])
    result['stable_inputs']=result.get('inputs_before')==result['inputs_after']
    result['no_binary_image_or_library_output']=not any(p.suffix.lower() in ('.exe','.dll','.lib') for p in out.rglob('*'))
    result['passed']=(not result.get('failure') and result['stable_inputs'] and
                      result['no_binary_image_or_library_output'] and len(result['groups'])==2 and
                      sum(len(g.get('objects',[])) for g in result['groups'])==8)
    exclusive_json(out/'receipt.json',result)
    (out/'receipt.sha256').write_text(digest(out/'receipt.json')+'\n')
    print(json.dumps({k:result.get(k) for k in ['passed','failure','linked','executed','stable_inputs']},indent=2))
raise SystemExit(not result['passed'])
