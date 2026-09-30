from pathlib import Path
import re,json,hashlib
r=Path(__file__).resolve().parent;s=r.parent;base=s/'pipe-composition77/candidate';overlay=s/'text-controls81/candidate';out=r/'tree';out.mkdir(exist_ok=False);origins={}
stub=s/'portable-reply66/tree/client-runtime53/client_file_runtime.h'
def take(rel):
 if rel in origins:return
 source=overlay/rel if (overlay/rel).is_file() else base/rel
 kind='actual production source'
 if rel=='client-runtime53/client_file_runtime.h':source=stub;kind='explicit unavailable Runtime substitute from66'
 data=source.read_bytes();p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 origins[rel]={'source':str(source),'sha256':hashlib.sha256(data).hexdigest(),'kind':kind}
 for n in re.findall(r'^\s*#\s*include\s*"([^"]+)"',data.decode(),re.M):
  q=(p.parent/n).resolve();assert q.is_relative_to(out.resolve());take(str(q.relative_to(out.resolve())))
for rel in ['backend-boundary24/pipe/PipeCore.cpp','transport-candidate/codec.cpp','session-version22/session_version.cpp','startup-metadata-v4/metadata_wire.cpp','callback-reentry47/invocation_guard.cpp']:take(rel)
(r/'origins.json').write_text(json.dumps(origins,indent=2)+'\n');print(len(origins))
