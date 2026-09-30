from pathlib import Path
import hashlib, tarfile, subprocess, sys
root=Path('C:/native-playback28')
archive=root/'source-v1.tar'
assert hashlib.sha256(archive.read_bytes()).hexdigest()=='80f9c63368bd6a1d3cfa736b85e20b6eb611bee9f39eb978a997e233542e8d3f'
with tarfile.open(archive) as t:
 for m in t.getmembers():
  assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
 t.extractall(root)
p=subprocess.run([sys.executable,str(root/'native-playback28/build-native.py'),'--approved-compile-only'])
raise SystemExit(p.returncode)
