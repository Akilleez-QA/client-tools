from pathlib import Path
import json,zipfile,hashlib
r=Path('C:/host-link78');out=r/'link-evidence-v1'
files=[p for p in out.iterdir() if p.is_file() and p.suffix in {'.json','.log'}]
with zipfile.ZipFile(r/'curated-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files:z.write(p,str(p.relative_to(r)))
print(json.dumps({'sha256':hashlib.sha256((r/'curated-evidence.zip').read_bytes()).hexdigest(),'files':len(files)}))
