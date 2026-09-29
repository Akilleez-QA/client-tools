from pathlib import Path
import json,re,hashlib
root=Path(__file__).resolve().parent
native=root/'native'
def read(p):
 b=p.read_bytes();return b.decode('utf-16') if b.startswith(b'\xff\xfe') else b.decode('utf-8-sig')
results=[]
for v in ['c1','c2']:
 for plat in ['Win32','x64']:
  for cfg in ['Release','Debug']:
   tag=f'{v}-{plat}-{cfg}'; d=native/tag
   assert read(native/(tag+'.exit')).strip()=='0'
   for probe in ['project-stress','project-occlusion']:assert read(d/(probe+'.exit')).strip()=='0'
   stress=read(d/'project-stress.log'); occ=read(d/'project-occlusion.log')
   q=re.findall(r'^QUERY q=(\d+) sentinel=1 begin=1 end=1 invalid=0 ',stress,re.M)
   frames=re.findall(r'^mode=1 frame=(\d+) visible=319 begin=1 end=1 writes=1',occ,re.M)
   assert list(map(int,q))==list(range(192)); assert list(map(int,frames))==list(range(64))
   assert 'RESULT failures=0' in stress;assert 'SUMMARY firstHidden=0 reappeared=0 totalWrites=64 failures=0' in occ
   log=read(native/(tag+'.log'))
   results.append({'variant':v,'platform':plat,'configuration':cfg,'build_exit':0,'stress_queries':len(q),'occlusion_frames':len(frames),'dll_sha256':hashlib.sha256((d/'dpvs.dll').read_bytes()).hexdigest(),'warnings':re.findall(r'([0-9]+) Warning\(s\)',log),'errors':re.findall(r'([0-9]+) Error\(s\)',log)})
(root/'verified-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
