from pathlib import Path
import hashlib, tarfile, subprocess, sys
root=Path('C:/pipe-native26')
archive=root/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='7ba7a8329a1074d321ae2ca16783ee87bda0a8065616549caf863a4e1dab74c8'
with tarfile.open(archive) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
 t.extractall(root)
p=subprocess.run([sys.executable,str(root/'pipe-native26/build-native.py'),'--approved-compile-only'])
raise SystemExit(p.returncode)
