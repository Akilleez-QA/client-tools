from pathlib import Path
import re,json,hashlib
r=Path(__file__).resolve().parent;s=r.parent;out=r/'tree';out.mkdir(exist_ok=False);origins={}
def take(rel):
 if rel in origins:return
 p=s/'version90/candidate'/rel
 if not p.is_file():p=s/'pipe-composition86/candidate'/rel
 kind='actual selected production'
 if rel=='client-runtime53/client_file_runtime.h':p=s/'portable-reply66/tree'/rel;kind='explicit Runtime66 dependency substitute'
 data=p.read_bytes();target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 origins[rel]={'source':str(p),'sha256':hashlib.sha256(data).hexdigest(),'kind':kind}
 for n in re.findall(r'^\s*#\s*include\s*"([^"]+)"',data.decode(),re.M):
  q=(target.parent/n).resolve();assert q.is_relative_to(out.resolve());take(str(q.relative_to(out.resolve())))
for rel in ['backend-boundary24/pipe/PipeCore.cpp','transport-candidate/codec.cpp','session-version22/session_version.cpp','startup-metadata-v4/metadata_wire.cpp','callback-reentry47/invocation_guard.cpp']:take(rel)
(r/'origins.json').write_text(json.dumps(origins,indent=2)+'\n')
