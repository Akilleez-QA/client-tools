"""Collect text receipts only. Does not run test/vendor executables."""
from pathlib import Path
import tarfile,hashlib
r=Path('C:/session-version21')
files=[p for d in ['build-v1','build-v2','runtime-v2'] for p in (r/d).rglob('*')
       if p.is_file() and p.suffix in ['.json','.log','.cmd','.sha256']]
files += [r/'wrong-pin.stdout',r/'wrong-pin.stderr']
with tarfile.open(r/'evidence-v2.tar','x') as t:
 for p in files:t.add(p,arcname=str(p.relative_to(r)))
print('Text evidence files:',len(files))
print(hashlib.sha256((r/'evidence-v2.tar').read_bytes()).hexdigest())
