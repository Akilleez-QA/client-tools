"""Explicit receipt/DLL launch checks; resource probe and pure consumer only."""
from pathlib import Path
import sys,json,subprocess
root=Path('C:/session-version22')
sys.path.insert(0,str(root/'revision4-tools'))
from receipt import digest,machine
from build_receipt import exclusive_json
def require(condition,reason):
 if not condition: raise RuntimeError(reason)
require(len(sys.argv)==2,'external receipt pin required')
build=root/'build-v1'; receipt_path=build/'receipt.json'
require(digest(receipt_path)==sys.argv[1],'receipt digest mismatch')
r=json.loads(receipt_path.read_text()); require(r['stable_matrix'],'unstable matrix')
require(r['builder_before']==r['builder_after'] and r['source_before']==r['source_after'],'changed matrix inputs')
expected={(a,c,k) for c in ['Debug','Release'] for a in ['x86','amd64'] for k in (['wire','host','poison'] if a=='x86' else ['wire'])}
require(len(r['builds'])==len(expected) and {(x['arch'],x['config'],x['kind']) for x in r['builds']}==expected,'matrix mismatch')
dlls=[root/'private/first/Mss32.dll',root/'private/second/Mss32.dll']; dllhash='0785b5f2aa81e68c41778bea1aa92ed545e2392827d90745838af2b14f6954fe'
require(digest(__file__)==r['builder_before'][str(Path(__file__).resolve())],'launcher differs from build receipt')
out=root/'runtime-v1'; out.mkdir(exist_ok=False)
records=[]
def execute(record,arguments,suffix=''):
 require(record['discovery_exit']==0 and record['exit_code']==0 and record['inputs_unchanged'],'build failure')
 require(record['before']==record['after'] and not record['unrecorded_libraries'],'changed build inputs')
 require(record['before']['headers'] and record['before']['tools'],'missing provenance')
 p=Path(record['output']['path']); expected_machine=0x14c if record['arch']=='x86' else 0x8664
 require(machine(p)==record['output']['machine']==expected_machine,'PE machine mismatch')
 require(digest(p)==record['output']['sha256'],'prelaunch PE mismatch')
 require(all(digest(d)==dllhash for d in dlls),'prelaunch original DLL copy mismatch')
 name=record['arch']+'-'+record['config']+'-'+record['kind']+suffix
 work=out/name; work.mkdir(); command=[str(p)]+arguments
 pre=dict(name=name,argv=command,exe_sha256=digest(p),dll_sha256={str(d):digest(d) for d in dlls},receipt_sha256=sys.argv[1])
 exclusive_json(work/'launch.json',pre)
 result=subprocess.run(command,cwd=work,capture_output=True,timeout=30)
 (work/'run.log').write_bytes(result.stdout+result.stderr)
 result_record=dict(pre,exit_code=result.returncode,post_exe_sha256=digest(p),post_dll_sha256={str(d):digest(d) for d in dlls})
 records.append(result_record); exclusive_json(work/'result.json',result_record)
 print(name+' exit='+str(result.returncode)+' '+result.stdout.decode(errors='replace').strip())
 require(result.returncode==0,'runtime failure: '+name)
 require(digest(p)==record['output']['sha256'] and all(digest(d)==dllhash for d in dlls),'runtime identity changed')
 return work
for record in r['builds']:
 if record['kind']=='wire': execute(record,[])
for config in ['Debug','Release']:
 consumer=next(x for x in r['builds'] if x['arch']=='amd64' and x['config']==config)
 for kind in ['host','poison']:
  host=next(x for x in r['builds'] if x['kind']==kind and x['config']==config)
  work=execute(host,[str(d) for d in dlls])
  consumed=execute(consumer,[str(work/'version-reply.bin'),str(work/'macro-oracle.bin')],'-consume-'+kind)
  require((consumed/'consumer-copy.bin').read_bytes()==(work/'macro-oracle.bin').read_bytes(),'x64 byte equality failure')
  require((work/'macro-oracle.bin').read_bytes().endswith(b'\0'),'missing expected NUL')
  records[-1]['resource_text']=list((work/'macro-oracle.bin').read_bytes())
exclusive_json(out/'results.json',dict(receipt_sha256=sys.argv[1],records=records,launcher_sha256=digest(__file__),passed=True,
 scope='native x86 direct-held-handle resource query, single-basename macro oracle, duplicate-basename data mappings; native x64 file-backed consume; no live pipe/product'))
