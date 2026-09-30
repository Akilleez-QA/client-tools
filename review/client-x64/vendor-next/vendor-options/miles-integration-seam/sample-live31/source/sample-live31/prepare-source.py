"""Successor31: exact reviewed C4389 cast plus fresh path labels; no compiler invocation."""
from pathlib import Path
import hashlib,json,tarfile
b=Path(__file__).resolve().parent
old=b.parent/'sample-live30'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if h(old/'source-manifest.json')!='8fe8d03927c6e389c8bb648fbe4800408552c6223cd0fb136483b807d3a3eded':raise RuntimeError('frozen30 manifest')
manifest=json.loads((old/'source-manifest.json').read_text())
stage=b/'private-source-v1';stage.mkdir(exist_ok=False)
deltas=[]
for name,pin in manifest.items():
    source=old/'private-source-v1'/name
    if h(source)!=pin:raise RuntimeError('frozen30 input '+name)
    newname=name.replace('sample-live30','sample-live31').replace('build-live30.py','build-live31.py').replace('run-live30.py','run-live31.py')
    original=source.read_text();text=original
    if name=='startup-bridge23/reply.h':
        needle='r.resource.kind != (sampleAllocation ? MilesWire::OwnedSample : MilesWire::Driver)'
        if text.count(needle)!=1:raise RuntimeError('exact signedness correction target')
        text=text.replace(needle,'r.resource.kind != static_cast<uint32_t>(sampleAllocation ? MilesWire::OwnedSample : MilesWire::Driver)')
    if name.startswith('sample-live30/'):
        text=text.replace('sample-live30','sample-live31').replace('build-live30.py','build-live31.py').replace('run-live30.py','run-live31.py').replace('live30-private','live31-private').replace('swg_live30_','swg_live31_')
        if name.endswith('/prepare-source.py'):text=Path(__file__).read_text()
    target=stage/newname;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    if name!=newname or text!=original:deltas.append({'before':name,'after':newname,'before_sha256':pin,'after_sha256':h(target)})
    if newname.startswith('sample-live31/') and not newname.endswith('/prepare-source.py'):
        (b/Path(newname).name).write_text(text)
lineage='''# Successor31 source lineage

Parent explicitly approved exactly the reply resource-kind signedness correction after frozen30 failed v120 C4389 under /WX. The expression now casts the existing conditional enum to uint32_t, matching r.resource.kind; wire constants remain2/1 and behavior is unchanged. Fresh directory, runner, builder, sink and private runtime path labels select31. All780-request counts/status/admission and lifetime assertions are unchanged. Frozen30 source and failed receipt5b142ad2... are preserved. No warning suppression, callback/binding/query/playback expansion or runtime authorization. The parent preauthorized ONE fresh build for this exact successor; no automatic repair/retry after it.
'''
(b/'LINEAGE.md').write_text(lineage);(stage/'sample-live31/LINEAGE.md').write_text(lineage)
(b/'delta.json').write_text(json.dumps(deltas,indent=2)+'\n');(stage/'sample-live31/delta.json').write_bytes((b/'delta.json').read_bytes())
entries={str(p.relative_to(stage)):h(p) for p in sorted(stage.rglob('*')) if p.is_file()}
with (b/'source-manifest.json').open('x') as f:json.dump(entries,f,indent=2);f.write('\n')
with tarfile.open(b/'source-v1.tar','x') as t:
    for name in entries:t.add(stage/name,arcname=name,recursive=False)
    t.add(b/'source-manifest.json',arcname='source-manifest.json',recursive=False)
print(json.dumps({'source':h(b/'source-v1.tar'),'manifest':h(b/'source-manifest.json'),'files':len(entries)},indent=2))
