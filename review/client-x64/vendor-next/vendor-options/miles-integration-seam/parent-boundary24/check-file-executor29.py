from pathlib import Path
import hashlib,json,re
b=Path(__file__).resolve().parent.parent/'file-executor29';p=b/'native-evidence-v1/curated'
def require(x,m):
 if not x:raise RuntimeError(m)
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(v):return str(v).replace('\\','/').lower()
before=json.loads((p/'before.json').read_text());after=json.loads((p/'after.json').read_text());inputs=json.loads((b/'native-inputs/input-manifest.json').read_text())
require(h(b/'native-inputs/input-manifest.json')==before['manifest']==after['manifest']=='a02c162efe3dfd320f50cc4e0d8f56f236b99d770904c3c22e988e5dc48b135d','manifest')
require(before['sha256']==after['sha256']==inputs['sha256'],'input identities')
require(not after['input_mismatches'] and not after['actual_include_mismatches'],'changed inputs')
require(h(b/'run-native.py')==before['driver']==after['driver'],'driver')
r=json.loads((p/'results/results.json').read_text())['builds'];require(len(r)==8,'matrix size');seen=set()
for x in r:
 k=(x['configuration'],x['platform'],x['mode']);require(k not in seen,'duplicate config');seen.add(k)
 d=p/'results'/('-'.join(k));cmd=json.loads((d/'command.json').read_text());log=(d/'compile.log').read_text();inc=json.loads((d/'actual-includes.json').read_text())
 require(x['exit_code']==0 and x['status']=='compiled' and not x['diagnostics'],'compile')
 require('/c' in x['command'] and '/EHsc' in x['command'] and '/Y-' in x['command'],'flags')
 require(not re.search(r'\b(?:warning|error) C\d+',log),'diagnostic')
 require(h(d/'actual-includes.json')==x['actual_includes_sha256'] and len(inc)==x['actual_include_count'],'include receipt')
 require(any(norm(v).endswith('/miles/include/mss.h') for v in inc),'actual sdk include')
 rel=norm(x['source']).removeprefix('c:/file-executor29/')
 match={norm(v):a for v,a in before['sha256'].items()};require(match[rel]==x['source_sha256'],'source receipt')
 require(x['coff_machine']==('0x14c' if x['platform']=='Win32' else '0x8664'),'object machine')
require(seen=={(c,a,m) for c in ['Debug','Release'] for a in ['Win32','x64'] for m in ['baseline','candidate']},'matrix contents')
result={'scope':'Parent raw source/input/commands/log/include/receipt attribution; not another compiler run or independent COFF read','passed':True,'object_compilations':8,'zero_compiler_diagnostics':True,'original_input_count':len(inputs['sha256']),'manifest_sha256':before['manifest'],'actual_header_identity_stable':True,'no_link_or_runtime':True}
(b/'parent-build-attribution.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
