from pathlib import Path
import hashlib, tarfile, subprocess, sys
root=Path('C:/pipe-live27')
archive=root/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='05554849a747140ef3e9d5d3ef8431f3303ae668ece4066ae1de9854675aa7b5'
with tarfile.open(archive) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
 t.extractall(root)
p=subprocess.run([sys.executable,str(root/'pipe-live27/build-live27.py'),'--approved-build-only'])
raise SystemExit(p.returncode)
