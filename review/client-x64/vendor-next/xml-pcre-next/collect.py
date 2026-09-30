from pathlib import Path
import zipfile,hashlib,json
out=Path('C:/xml-pcre-evidence.zip');manifest={}
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for dirname in ['xml-pcre-next-v3','pcre-native-v3','xml-pcre-probe-v3','xml-pcre-probe-legacy']:
  root=Path('C:/'+dirname)
  for p in root.rglob('*'):
   if p.is_file() and (p.name in ['results.json','build.log','result.log','config.h','xmlversion.h','config.msvc','chartables.c','testoutput1.actual'] or p.suffix in ['.lib','.dll','.exe']):
    if p.suffix in ['.lib','.dll','.exe']:manifest[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
    else:z.write(p,dirname+'/'+p.relative_to(root).as_posix())
 z.writestr('binary-hashes.json',json.dumps(manifest,indent=2))
