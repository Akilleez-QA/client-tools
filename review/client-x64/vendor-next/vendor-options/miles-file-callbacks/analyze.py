import json,re,collections,hashlib,struct,wave
from pathlib import Path
b=Path(__file__).resolve().parent
runs=[]
for h in (0,1):
 s=(b/f'run-b/handle{h}.log').read_text();main=int(re.search(r'main=(\d+)',s)[1])
 es=[]
 for line in s.splitlines():
  if line.startswith('seq='):
   e=dict(x.split('=',1) for x in line.split());es.append({k:v if k=='op' else int(v) for k,v in e.items()})
 files=[e for e in es if e['op'].split('-')[0] in ('open','read','seek','close')]
 eos=[e for e in es if e['op']=='eos-exit']
 runs.append(dict(handle=h,main=main,counts=dict(collections.Counter(e['op'] for e in es)),file_threads=sorted(set(e['tid'] for e in files)),foreign_file_threads=sorted(set(e['tid'] for e in files)-{main}),eos_threads=sorted(set(e['tid'] for e in eos)),all_foreign_threads=sorted(set(e['tid'] for e in es)-{main}),max_depth=max(e['depth'] for e in es),max_active=max(e['active'] for e in es),missing_phase=[e for e in es if e['phase']==1],read_bytes=sum(e['result'] for e in es if e['op']=='read-exit'),no_serve_callbacks=[e for e in es if e['phase']==3 and e['depth']>0]))
r=json.loads((b/'run-b/results.json').read_text())
for a,x in zip(runs,r['runs']):
 a['returncode']=x['returncode'];a['wall_seconds']=x['wall_seconds'];a['route_observations']=sum(bool(v['inputs']) for v in x['routing']);a['route_sink_indices']=sorted(set(i['sink'] for v in x['routing'] for i in v['inputs']))
with wave.open(str(b/'private-prefix-fcb-a/drive_c/fcb-private/sample.wav')) as w: pcm=dict(channels=w.getnchannels(),rate=w.getframerate(),frames=w.getnframes(),width=w.getsampwidth())
(b/'analysis.json').write_text(json.dumps(dict(pcm=pcm,runs=runs),indent=2))
paths=[b/p for p in ['PLAN.md','probe.cpp','Mss.h','build.cmd','build.ps1','probe.exe','run.py','run-initial.py','analyze.py']]
prefix=b/'private-prefix-fcb-a'
for d in ['fcb-private','windows/system32','windows/syswow64']:
 for n in (['probe.exe','Mss32.dll','sample.wav'] if d=='fcb-private' else ['ntdll.dll','kernel32.dll','winmm.dll','dsound.dll','mmdevapi.dll','winealsa.drv']):
  p=prefix/'drive_c'/d/n
  if p.exists():paths.append(p)
for n in ['/usr/bin/wine','/usr/bin/wineserver','/usr/lib/alsa-lib/libasound_module_pcm_pulse.so']:
 p=Path(n)
 if p.exists():paths.append(p)
(b/'hashes.json').write_text(json.dumps({str(p):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths},indent=2))
print(json.dumps([{k:v for k,v in x.items() if k not in ['no_serve_callbacks','missing_phase']} for x in runs],indent=2))
