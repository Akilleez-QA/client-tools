from pathlib import Path
import hashlib, tarfile, subprocess, sys
root=Path('C:/borrowed-native33')
archive=root/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='d86bd0d81598c1ef4dbef1969bd0a6463f8cabdb7856a4e28c2d4420f8e8460f'
with tarfile.open(archive) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
 t.extractall(root)
p=subprocess.run([sys.executable,str(root/'borrowed-native33/build-native.py'),'--approved-compile-only'])
raise SystemExit(p.returncode)
