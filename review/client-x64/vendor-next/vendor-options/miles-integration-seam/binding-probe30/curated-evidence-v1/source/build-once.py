"""Frozen one-CL v120 x86 build/link only. No PE execution, VM or runtime setup."""
from pathlib import Path
import hashlib,json,os,shutil,sys
if os.name!='nt' or sys.argv[1:]!=['--approved-build-only']:
    raise SystemExit('Requires Windows and separate parent-approved build-only invocation')
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
manifest=json.loads((root/'source-manifest.json').read_text())
for name,expected in manifest.items():
    if sha(root/name)!=expected:raise RuntimeError('frozen source mismatch: '+name)
pins=json.loads((root/'input-pins.json').read_text())
sdk=Path('C:/client-next-build/src/external/3rd/library/miles/include/Mss.h')
lib=Path('C:/client-next-build/src/external/3rd/library/miles/lib/win/Mss32.lib')
if sha(sdk)!=pins['sdk_header_sha256'] or sha(lib)!=pins['import_library_sha256']:
    raise RuntimeError('possessed SDK/import identity mismatch')
sys.path.insert(0,str(root/'helpers'))
from build_receipt import environment,identities,includes,run,exclusive_json
from receipt import machine
out=root/'native-build-v1';out.mkdir(exist_ok=False) # exactly one build attempt
receipt={'scope':'one v120 x86 build/link; no execution','cl_invocations':0,
         'manifest_sha256':sha(root/'source-manifest.json'),'sdk':identities([sdk,lib]),
         'sources_before':identities([root/p for p in manifest]),'executed':False}
try:
    vc=Path('C:/Program Files (x86)/Microsoft Visual Studio 12.0/VC/vcvarsall.bat')
    env=environment(vc,'x86',out)
    compiler=Path(shutil.which('cl.exe',path=env['PATH']))
    linker=Path(shutil.which('link.exe',path=env['PATH']))
    dumpbin=Path(shutil.which('dumpbin.exe',path=env['PATH']))
    receipt['tools']=identities([vc,compiler,linker,dumpbin])
    exe=out/'probe.exe'
    command=[str(compiler),'/nologo','/W4','/WX','/EHsc','/MT','/O2','/DWIN32',
             '/D_WIN32_WINNT=0x0601','/showIncludes','/I'+str(sdk.parent),
             str(root/'probe.cpp'),str(lib),'/Fe'+str(exe),'/link','/MACHINE:X86']
    receipt['cl_invocations']=1
    code,log=run(command,out,'compile-link',env);receipt['build_exit']=code
    headers=includes(log);receipt['actual_headers_after_compile']=identities(headers)
    if sdk.resolve() not in headers:raise RuntimeError('actual possessed Mss.h absent from include trace')
    if code:raise RuntimeError('build failed; no retry authorized')
    if machine(exe)!=0x14c:raise RuntimeError('output is not x86')
    receipt['output']={'sha256':sha(exe),'machine':machine(exe)}
    code,log=run([str(dumpbin),'/imports',str(exe)],out,'imports',env)
    receipt['imports_exit']=code
    if code:raise RuntimeError('import inspection failed')
finally:
    receipt['sources_after']=identities([root/p for p in manifest])
    receipt['sdk_after']=identities([sdk,lib])
    receipt['stable_pinned_inputs']=(receipt['sources_after']==receipt['sources_before'] and receipt['sdk_after']==receipt['sdk'])
    exclusive_json(out/'receipt.json',receipt)
if not receipt['stable_pinned_inputs']:raise RuntimeError('pinned build inputs changed')
