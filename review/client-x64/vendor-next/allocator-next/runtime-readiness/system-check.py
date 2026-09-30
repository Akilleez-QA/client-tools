from pathlib import Path
import json,hashlib,struct,os
out=Path('C:/runtime-readiness-v3');root=Path('C:/integration-current-v2/workspace/repo');system=Path(os.environ['WINDIR'])/('System32' if struct.calcsize('P')==8 else 'Sysnative');rows=[]
for n in ['d3d9.dll','d3dx9_43.dll','ddraw.dll','kernel32.dll','user32.dll']:
 p=system/n;row={'name':n,'native_system_path':str(p),'exists':p.exists()}
 if p.exists():
  b=p.read_bytes();off=struct.unpack_from('<I',b,60)[0];row.update(machine=hex(struct.unpack_from('<H',b,off+4)[0]),sha256=hashlib.sha256(b).hexdigest())
 rows.append(row)
(out/'system-resolution.json').write_text(json.dumps({'python_bits':struct.calcsize('P')*8,'checks':rows,'dev_x64_exists':(root/'dev/x64').exists(),'product_xml_deployed':{cfg:(root/'src/compile/x64/SwgClient'/cfg/'libxml2.dll').exists() for cfg in ['Release','Debug']}},indent=2));print(rows)
