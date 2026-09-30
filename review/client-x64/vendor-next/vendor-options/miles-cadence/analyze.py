from pathlib import Path
import json,re,hashlib,struct
b=Path(__file__).resolve().parent
r=json.loads((b/'run-a/results.json').read_text());rows=[]
for run in r['runs']:
 p=b/'run-a'/ (run['label']+'.log');s=p.read_text();main=int(re.search(r'main=(\d+)',s)[1]);freq=int(re.search(r'frequency=(\d+)',s)[1]);es=[]
 for line in s.splitlines():
  if line.startswith('seq='):
   d=dict(x.split('=',1) for x in line.split());es.append({k:v if k=='op' else int(v,16 if k in ['cw','sw','mxcsr'] else 10) for k,v in d.items()})
 assert [e['seq'] for e in es]==list(range(len(es)))
 assert all(a['qpc']<=c['qpc'] for a,c in zip(es,es[1:]))
 assert 'overflow=0 eos=1 rc=0' in s and run['returncode']==0 and not run.get('timed_out')
 serve=[e for e in es if e['op']=='serve-enter'];status=[e for e in es if e['op']=='status-return'];positions=[e for e in es if e['op']=='position-return'];eos=[e for e in es if e['op']=='eos'];assert len(eos)==1
 assert all(e['tid']==main for e in es if e['op']!='eos')
 intervals=[(c['qpc']-a['qpc'])*1000/freq for a,c in zip(serve,serve[1:])];assert min(intervals)>=50
 for op in ['status-enter','status-return','position-return']:
  v=[e for e in es if e['op']==op];assert len(v)==len(serve)
  assert all((c['qpc']-a['qpc'])*1000/freq>=50 for a,c in zip(v,v[1:]))
 first=next(e for e in status if e['status']==2);pos=next(e for e in positions if e['seq']>first['seq'])
 hold=next(e for e in es if e['op']=='hold-start');release=next(e for e in es if e['op']=='release-enter');retention=(release['qpc']-hold['qpc'])*1000/freq;assert retention>=500
 routes=[i for snap in run['routing'] for i in snap['inputs']];assert routes and all(i['sink']==r['sink']['index'] for i in routes)
 # Save all route snapshots; detect any observed probe producer on a different sink.
 off=[i for snap in run['routing'] for i in snap['all_inputs'] if 'probe' in i.get('properties',{}).get('application.name','').lower() and i['sink']!=r['sink']['index']];assert not off
 prev=es[eos[0]['seq']-1];nxt=es[eos[0]['seq']+1]
 rows.append(dict(label=run['label'],main=main,eos=eos[0],eos_neighbors=[prev,nxt],first_done=first,first_done_position=pos,observed_gap=any(e['status']==2 and e['flag']==0 for e in status),cadence_ms=[min(intervals),max(intervals)],retention_ms=retention,wall_seconds=run['wall_seconds'],events=len(es),route_snapshots=sum(bool(x['inputs']) for x in run['routing'])))
old=[]
for p in sorted((b.parent/'miles-realtime').glob('*/probe.log')):
 if not (p.parent.name.startswith('drain-') or p.parent.name.startswith('command-')):continue
 s=p.read_text();main=int(re.search(r'event=entry tick=\d+ thread=(\d+)',s)[1]);m=re.search(r'event=(sample|stream)-eos tick=(\d+) thread=(\d+) cw=(\w+) mxcsr=(\w+)',s)
 old.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),main=main,eos_thread=int(m[3]),cw=m[4],mxcsr=m[5],same_thread=main==int(m[3])))
for handle in [0,1]:
 p=b.parent/f'miles-file-callbacks/run-b/handle{handle}.log';s=p.read_text();main=int(re.search(r'main=(\d+)',s)[1]);line=next(l for l in s.splitlines() if 'op=eos-exit' in l);tid=int(re.search(r'tid=(\d+)',line)[1]);old.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),main=main,eos_thread=tid,same_thread=main==tid))
assert r['defaults_unchanged'] and r['sink_removed'] and r['private_wineserver_stop']==0
out=dict(runs=rows,old_log_correction=old,first_done_positions_identical={mode:len(set((x['first_done_position']['total'],x['first_done_position']['pos']) for x in rows if x['label'].startswith(mode)))==1 for mode in ['sample','stream']},all_checks_passed=True)
(b/'analysis.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
