"""Apply isolated review overlays and run authored scripted tests only. No vendor/native runtime."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
base=Path(__file__).resolve().parent; root=base.parent
out=base/'evidence-portable-v2';out.mkdir(exist_ok=False)
stage=base/'private-stage-v2';stage.mkdir(exist_ok=False)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
seeds=['backend-boundary24/tests/adapter_test.cpp','backend-boundary24/sample/startup_calls.cpp',
       'backend-boundary24/pipe/ClientMilesPipe.cpp','startup-bridge23/backend.h',
       'startup-bridge23/reply.h','native-startup25/ClientMilesStartup.h',
       'native-startup25/native/native_startup25.cpp','native-startup25/sample/install_order.cpp',
       'native-startup25/build-native.py','backend-boundary24/native/native_miles64.cpp',
       'transport-candidate/codec.cpp','session-version22/session_version.cpp',
       'startup-metadata-v4/metadata_wire.cpp','host-candidate/host_dispatch.cpp',
       'live-bridge-candidate/revision4-tools/build_receipt.py',
       'live-bridge-candidate/revision4-tools/receipt.py']
seeds += [str(p.relative_to(root)) for p in (base/'tests').glob('*.cpp')]
inputs={};queue=[root/n for n in seeds]
while queue:
    p=queue.pop().resolve(); n=str(p.relative_to(root))
    if n in inputs:continue
    inputs[n]=digest(p)
    dest=stage/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    for target in re.findall(r'^\s*#include\s+"([^"]+)"',p.read_text(),re.M):
        dependency=(p.parent/target).resolve()
        if dependency.is_file() and dependency.is_relative_to(root):queue.append(dependency)
(base/'input-manifest.json').write_text(json.dumps(inputs,indent=2)+'\n')
commands=[]
def run(args,name,expected=0):
    commands.append(args);p=subprocess.run(args,cwd=stage,text=True,capture_output=True,timeout=60)
    (out/(name+'.log')).write_text(p.stdout+p.stderr)
    (out/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
    if expected==0 and p.returncode:raise RuntimeError(name+': '+p.stderr)
    return p
authored=[base/'check-portable.py']+list((base/'patches').glob('*.patch'))
original_authored={str(p):digest(p) for p in authored}
result={'native_execution':False,'vendor_execution':False,'tests_only':True,'authored_before':original_authored}
try:
    for p in sorted((base/'patches').glob('*.patch')):
        run(['patch','--batch','--forward','--fuzz=0','-p1','-i',str(p)],p.stem)
    compiler=str(Path(shutil.which('g++')).resolve())
    flags=[compiler,'-std=c++11','-Wall','-Wextra','-Werror','-pedantic','-g','-fsanitize=address,undefined']
    dependencies=['backend-boundary24/pipe/ClientMilesPipe.cpp','transport-candidate/codec.cpp',
                  'session-version22/session_version.cpp','startup-metadata-v4/metadata_wire.cpp']
    run(flags+['pipe-startup26/tests/seven_operations.cpp']+dependencies+['-o',str(stage/'seven-test')],'seven-build')
    p=run([str(stage/'seven-test')],'seven-run');result['seven_stdout']=p.stdout
    run(flags+['backend-boundary24/tests/adapter_test.cpp','backend-boundary24/sample/startup_calls.cpp']+
        dependencies+['-o',str(stage/'baseline-test')],'baseline-build')
    p=run([str(stage/'baseline-test')],'baseline-run');result['baseline_stdout']=p.stdout
    run(flags+['-DPIPE26_TEST_ONLY','pipe-startup26/tests/sample_fix.cpp',
               'native-startup25/sample/install_order.cpp','-o',str(stage/'sample-test')],'sample-build')
    p=run([str(stage/'sample-test')],'sample-run');result['sample_stdout']=p.stdout
    p=run(flags+['pipe-startup26/tests/unimplemented_callbacks.cpp']+dependencies+
          ['-o',str(stage/'must-not-link')],'callbacks-negative-link',expected=1)
    if not p.returncode or 'ClientMiles::set_file_callbacks' not in p.stderr:
        raise RuntimeError('missing callback implementation not distinguished by link failure')
    result['callbacks_unimplemented_link_exit']=p.returncode
    result['staged_sources']={str(p.relative_to(stage)):digest(p) for p in stage.rglob('*')
                             if p.is_file() and p.suffix in ('.h','.cpp','.py')}
except Exception as e:result['failure']=str(e)
result['original_inputs_unchanged']=all(digest(root/n)==h for n,h in inputs.items())
result['authored_after']={str(p):digest(p) for p in authored}
result['passed']=not result.get('failure') and result['original_inputs_unchanged'] and result['authored_before']==result['authored_after']
(out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('staged_sources','authored_before','authored_after')},indent=2))
raise SystemExit(not result['passed'])
