from pathlib import Path
import hashlib, tarfile, subprocess, sys
root=Path('C:/sample-live31')
archive=root/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='835bac7d1352c3e205bf52d673c0b824270baedf9ec84c0ae6de1413f7c11bda'
with tarfile.open(archive) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
 t.extractall(root)
p=subprocess.run([sys.executable,str(root/'sample-live31/build-live31.py'),'--approved-build-only'])
raise SystemExit(p.returncode)
