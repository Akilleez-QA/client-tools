import re,json,hashlib,struct,subprocess
from pathlib import Path
out=Path(__file__).resolve().parent
source=Path('/home/akilleez/Work/swg-source/client-build-next/src/external/3rd/library/vivoxSharedWrapper/Vivox.cpp')
imports=list(dict.fromkeys(re.findall(r'^\s*IMPORT_FN\((\w+)\)',source.read_text(),re.M)))
roots=[Path('/home/akilleez/Work/swg-source-vm/client/SWGSource Client v3.0'),Path('/home/akilleez/Work/swg-source/whitengold/exe/win32')];rows=[]
for root in roots:
 names={p.name.lower():p for p in root.iterdir() if p.is_file()};todo=['vivoxsdk.dll','vivoxplatform.dll','swgvoiceservice.exe'];seen=set()
 while todo:
  name=todo.pop(0)
  if name in seen:continue
  seen.add(name);p=names.get(name)
  if not p:rows.append(dict(root=str(root),name=name,found=False));continue
  b=p.read_bytes();off=struct.unpack_from('<I',b,60)[0];machine=struct.unpack_from('<H',b,off+4)[0]
  pe=subprocess.check_output(['objdump','-p',str(p)],text=True);(out/(root.name+'-'+p.name+'.pe.txt')).write_text(pe)
  deps=re.findall(r'DLL Name: (\S+)',pe);exports=set(re.findall(r'^\s*\[\s*\d+\]\s+(?:\+base\[\s*\d+\]\s+\w+\s+)?(\w+)\s*$',pe,re.M))
  row=dict(root=str(root),name=p.name,found=True,machine=hex(machine),sha256=hashlib.sha256(b).hexdigest(),imports=deps,local_dependencies=[d for d in deps if d.lower() in names]);rows.append(row)
  if name=='vivoxsdk.dll':row['wrapper_exports']={n:n in exports for n in imports}
  todo += [d.lower() for d in deps if d.lower() in names]
(out/'binary-inventory.json').write_text(json.dumps(dict(wrapper_source=str(source),wrapper_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),wrapper_import_count=len(imports),binaries=rows),indent=2));(out/'exports.inc').write_text('\n'.join('"'+n+'",' for n in imports));print(len(imports));print([(r['name'],r.get('machine'),[k for k,v in r.get('wrapper_exports',{}).items() if not v]) for r in rows])
