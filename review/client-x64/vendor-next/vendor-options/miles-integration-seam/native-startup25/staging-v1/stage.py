from pathlib import Path
import hashlib, tarfile, subprocess, sys
root=Path('C:/native-startup25')
archive=root/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='7090ee3e90f6af53e4e49125d195cd90a271d8e7961c3190a56b94952dcdd9ce'
with tarfile.open(archive) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
 t.extractall(root)
p=subprocess.run([sys.executable,str(root/'native-startup25/build-native.py'),'--approved-compile-only'])
raise SystemExit(p.returncode)
