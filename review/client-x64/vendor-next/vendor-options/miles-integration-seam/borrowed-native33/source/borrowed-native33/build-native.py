"""Prepared11-TU common-sample v120 gate; no link or produced-code execution."""
from pathlib import Path
import os,sys,json,hashlib,shutil,struct
if os.name!='nt' or sys.argv[1:]!=['--approved-compile-only']:
    raise SystemExit('Windows and separate parent compile-only approval required')
root=Path('C:/borrowed-native33');base=root/'borrowed-native33'
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest=json.loads((root/'source-manifest.json').read_text())
for n,v in manifest.items():
    if h(root/n)!=v:raise RuntimeError('source identity mismatch '+n)
sdk=Path('C:/client-next-build/src/external/3rd/library/miles/include/Mss.h')
if h(sdk)!='966e1e81046851295079e9709f9f358286c823e4403ec6b0ca972b5059725e6e':raise RuntimeError('SDK pin mismatch')
sys.path.insert(0,str(root/'live-bridge-candidate/revision4-tools'))
from build_receipt import environment,identities,includes,run,exclusive_json
out=root/'native-v1';out.mkdir(exist_ok=False)
inputs=[root/n for n in manifest]
initial=identities(inputs)
result={'schema':'common-sample-object-receipt33','linked':False,'executed':False,'before':initial,'records':[],'python_sha256':h(sys.executable)}
try:
    vc=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
    env=environment(vc,'amd64',out)
    cl=Path(shutil.which('cl.exe',path=env['PATH']));dump=Path(shutil.which('dumpbin.exe',path=env['PATH']))
    tools={cl,dump,vc};tools.update(cl.parent.glob('*.dll'));tools.update(cl.parent.glob('1033/*.dll'));tools.update((vc.parent/'bin').glob('*.dll'));tools.update((vc.parent.parent/'Common7/IDE').glob('mspdb*.dll'))
    expected=json.loads((base/'expected.json').read_text())
    for index,item in enumerate(expected):
        directory=out/('%02d'%index);directory.mkdir()
        obj=directory/'unit.obj';record={'source':item['source']};result['records'].append(record)
        command=[str(cl),'/nologo','/W4','/WX','/EHsc','/MT','/O2','/DWIN32','/D_WIN32_WINNT=0x0601','/I'+str(sdk.parent),str(root/item['source'])]
        code,log=run(command+['/Zs','/showIncludes'],directory,'headers',env);record['discovery_exit']=code
        if code:raise RuntimeError('first header failure '+item['source'])
        headers=includes(log)
        if not headers or (item['sdk'] and sdk.resolve() not in headers):raise RuntimeError('missing required include evidence')
        before={'headers':identities(headers),'tools':identities(tools),'inputs':identities(inputs)};record['before']=before
        code,log=run(command+['/c','/showIncludes','/Fo'+str(obj)],directory,'object',env);record['compile_exit']=code
        record['after']={'headers':identities(headers),'tools':identities(tools),'inputs':identities(inputs)}
        record['stable']=before==record['after'] and includes(log)==headers
        if code or not record['stable']:raise RuntimeError('first compile/identity failure '+item['source'])
        record['object']={'sha256':h(obj),'machine':struct.unpack('<H',obj.read_bytes()[:2])[0]}
        if record['object']['machine']!=0x8664:raise RuntimeError('not AMD64 COFF')
        code,symbols=run([str(dump),'/symbols',str(obj)],directory,'symbols',env);record['symbols_exit']=code
        imports={line.split()[-1] for line in symbols.splitlines() if 'UNDEF' in line and '__imp_AIL_' in line}
        record['imports']=sorted(imports);record['exact_imports']=imports==set(item['imports'])
        if code or not record['exact_imports']:raise RuntimeError('unexpected actual SDK imports '+item['source'])
        if item['common_sample']:
            record['common_sample_symbols']='Sample@' in symbols and 'OwnedSample@' not in symbols
            if not record['common_sample_symbols']:raise RuntimeError('common pointee symbol check '+item['source'])
        if item['source']=='native-borrowed32/call_shapes.cpp':
            refs=['stream_sample_handle','set_sample_volume_levels','sample_volume_levels','set_sample_reverb_levels','set_sample_playback_rate','sample_playback_rate']
            undefined='\n'.join(line for line in symbols.splitlines() if 'UNDEF' in line)
            record['six_shared_references']=all('?'+name+'@ClientMiles@@' in undefined for name in refs)
            if not record['six_shared_references']:raise RuntimeError('borrowed caller reference missing')
except Exception as error:result['failure']={'type':type(error).__name__,'message':str(error)}
finally:
    result['after']=identities(inputs)
    result['stable']=initial==result['after']
    result['no_link_output']=not any(p.suffix.lower() in ['.exe','.dll','.lib'] for p in out.rglob('*') if p.is_file())
    result['passed']=not result.get('failure') and result['stable'] and result['no_link_output'] and len(result['records'])==11
    exclusive_json(out/'receipt.json',result)
    (out/'receipt.sha256').write_text(h(out/'receipt.json')+'\n')
    print(json.dumps({'passed':result['passed'],'receipt':h(out/'receipt.json'),'failure':result.get('failure')},indent=2))
raise SystemExit(not result['passed'])
