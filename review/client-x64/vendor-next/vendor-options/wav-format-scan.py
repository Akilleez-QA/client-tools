import json,struct,zlib,collections
from pathlib import Path
p=Path('/home/akilleez/Work/client-wire-validation/vendor-options');d=json.loads((p/'tre-media-inventory.json').read_text());counts=collections.Counter();examples={};errors=[];empty=[];subformats=collections.Counter()
for r in d['rows']:
 if not r['name'].endswith('.wav'):continue
 try:
  with open(r['tre'],'rb') as f:f.seek(r['offset']);b=f.read(r['packed'] if r['compression'] else r['size'])
  if r['compression']:b=zlib.decompress(b)
  if not b:empty.append(r);continue
  assert b[:4]==b'RIFF' and b[8:12]==b'WAVE'
  q=12
  while q+8<=len(b):
   tag,n=struct.unpack_from('<4sI',b,q)
   if tag==b'fmt ':
    fmt,ch,rate=struct.unpack_from('<HHI',b,q+8);bits=struct.unpack_from('<H',b,q+22)[0];key=f'tag={fmt},channels={ch},rate={rate},bits={bits}';counts[key]+=1;examples.setdefault(key,r)
    if fmt==65534:subformats[b[q+32:q+48].hex()]+=1
    break
   q+=8+n+(n&1)
  else:raise ValueError('no fmt')
 except Exception as e:errors.append([r['name'],str(e)])
(p/'wav-format-inventory.json').write_text(json.dumps(dict(counts=counts,examples=examples,errors=errors,empty=empty,extensible_subformats=subformats),indent=2));print(counts);print('errors',len(errors))
