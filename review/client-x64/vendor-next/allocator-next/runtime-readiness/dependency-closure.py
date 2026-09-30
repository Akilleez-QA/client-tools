from pathlib import Path
import struct,json,hashlib,os
root=Path('C:/runtime-staging49d0-v1');system=Path(os.environ['WINDIR'])/'System32';assert struct.calcsize('P')==8

def pe(p):
 b=p.read_bytes();off=struct.unpack_from('<I',b,60)[0];machine,nsections=struct.unpack_from('<HH',b,off+4);opt=off+24;optsz=struct.unpack_from('<H',b,off+20)[0];magic=struct.unpack_from('<H',b,opt)[0];dd=opt+(112 if magic==0x20b else 96);sections=[]
 for i in range(nsections):
  q=opt+optsz+40*i;vs,va,rs,rp=struct.unpack_from('<IIII',b,q+8);sections.append((va,max(vs,rs),rp))
 def rva(v):
  for va,sz,rp in sections:
   if va<=v<va+sz:return rp+v-va
  raise ValueError((str(p),'RVA',v))
 def name(v):
  q=rva(v);return b[q:b.index(b'\0',q)].decode('ascii')
 imports=[]
 for idx,stride,isdelay in [(1,20,False),(13,32,True)]:
  addr,sz=struct.unpack_from('<II',b,dd+8*idx)
  if not addr:continue
  pos=rva(addr)
  for i in range(sz//stride):
   fields=struct.unpack_from('<'+'I'*(stride//4),b,pos+i*stride)
   if not any(fields):break
   if isdelay:assert fields[0]&1
   imports.append({'name':name(fields[1] if isdelay else fields[3]),'delay':isdelay})
 exports=[];addr,sz=struct.unpack_from('<II',b,dd)
 if addr:
  q=rva(addr);count=struct.unpack_from('<I',b,q+24)[0];names=struct.unpack_from('<I',b,q+32)[0]
  if count:
   qn=rva(names);exports=[name(struct.unpack_from('<I',b,qn+4*i)[0]) for i in range(count)]
 return {'machine':hex(machine),'sha256':hashlib.sha256(b).hexdigest(),'imports':imports,'exports':exports}
allrows=[]
for cfg in ['Release','Debug']:
 stage=root/cfg;todo=list(stage.glob('*.dll'));seen=set();rows=[]
 while todo:
  p=todo.pop();key=str(p).lower()
  if key in seen:continue
  seen.add(key);row={'path':str(p),**pe(p),'dependencies':[]};assert row['machine']=='0x8664'
  for dep in row['imports']:
   n=dep['name'];entry=dict(dep)
   if n.lower()=='dllexport.dll' and dep['delay']:entry['resolution']='game-host export redirect; not loaded in this audit'
   elif n.lower().startswith(('api-ms-win-','ext-ms-win-')):entry['resolution']='Windows API-set contract; no physical-file assumption'
   else:
    target=stage/n if(stage/n).exists() else system/n;entry['resolved_path']=str(target);entry['resolution']='file' if target.exists() else 'missing'
    if target.exists():todo.append(target)
   row['dependencies'].append(entry)
  # Keep runtime export evidence compact; only renderer entry point is relevant here.
  row['exports']=[e for e in row['exports'] if e=='GetApi'];rows.append(row)
 allrows.append({'configuration':cfg,'files':rows,'missing':[d for r in rows for d in r['dependencies'] if d['resolution']=='missing']})
(root/'dependency-closure.json').write_text(json.dumps(allrows,indent=2));print([(r['configuration'],len(r['files']),len(r['missing'])) for r in allrows])
