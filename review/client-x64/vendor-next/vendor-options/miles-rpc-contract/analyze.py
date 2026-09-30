from pathlib import Path
import json,re,hashlib,struct
base=Path(__file__).resolve().parent;root=base/'run-b';result=json.loads((root/'results.json').read_text());assert result['defaults_unchanged'] and result['sink_removed']
records={}
for run in result['runs']:
 label=run['label'];text=(root/(label+'.log')).read_text();assert run['returncode']==0 and not run.get('timed_out');assert any(x['inputs'] for x in run['routing'])
 def row(line):return {k:int(v,16) if k in ['cw','sw','mx'] else int(v) for k,v in re.findall(r'(\w+)=(-?[0-9a-f]+)',line)}
 replies=[row(l) for l in text.splitlines() if l.startswith('reply ')];normal=[r for r in replies if r['kind']==0];notification=[r for r in replies if r['kind']==1];events=[row(l) for l in text.splitlines() if l.startswith('event ')];eos=[e for e in events if e['eos']==1]
 assert [r['id'] for r in normal]==list(range(1,67));assert len(notification)==len(eos)==1
 assert all(r['result']==(1 if r['id']==65 else 0) for r in normal)
 assert normal[63]['gen']==2 and normal[64]['gen']==2
 assert [e['seq'] for e in events]==list(range(133));assert all(events[i]['qpc']<=events[i+1]['qpc'] for i in range(132))
 expected=[1,2]+[v for _ in range(20) for v in [3,4,5]]+[6,7,4,8]
 for i in range(1,67):
  pair=[e for e in events if not e['eos'] and e['id']==i];assert len(pair)==2 and all(e['op']==expected[i-1] for e in pair)
 assert notification[0]['event']==eos[0]['seq'];event_index=replies.index(notification[0]);assert replies[event_index+1]['id']==notification[0]['id']
 done=[r for r in normal if r['status']==2];assert done
 positions=[r for r in normal if r['id'] in range(5,63,3)];assert positions[-1]['total']==positions[-1]['pos']==204
 frequency=int(re.search(r'frequency=(\d+)',text)[1]);assert frequency>0
 if label.startswith('controlled'):
  assert int(re.search(r'controller-frequency=(\d+)',text)[1])==frequency
  assert 'controller replies=66 events=1 host_exit=0 ok=1' in text
 rtts=[(r['end']-r['begin'])/frequency*1000 for r in normal if r['id']!=1]
 record=dict(first_done_id=done[0]['id'],first_done_next_position=normal[done[0]['id']]['pos'],eos_request_context=eos[0]['id'],eos_sequence=eos[0]['seq'],eos_thread=eos[0]['tid'],main_thread=events[0]['tid'],event_delivery_request=notification[0]['id'],eos_delivery_observation_ms=(notification[0]['end']-eos[0]['qpc'])/frequency*1000,noncreate_roundtrip_ms=dict(min=min(rtts),max=max(rtts)),create_ms=(normal[0]['end']-normal[0]['begin'])/frequency*1000,status_position_sequence=[(r['id'],r['status'],r['total'],r['pos']) for r in normal],response_count=len(normal),host_events=len(events),log_sha256=hashlib.sha256((root/(label+'.log')).read_bytes()).hexdigest())
 records[label]=record
comparisons=[]
for mode in ['sample','stream']:
 for n in [1,2]:
  a=records[f'direct-{mode}-{n}']['status_position_sequence'];b=records[f'controlled-{mode}-{n}']['status_position_sequence'];comparisons.append(dict(mode=mode,repeat=n,differences=[dict(direct=x,controlled=y) for x,y in zip(a,b) if x!=y]))
identity={}
for name in ['host.exe','controller.exe']:
 data=(base/name).read_bytes();machine=struct.unpack_from('<H',data,struct.unpack_from('<I',data,0x3c)[0]+4)[0];assert machine==(0x14c if name=='host.exe' else 0x8664);identity[name]=dict(sha256=hashlib.sha256(data).hexdigest(),machine=machine)
(base/'analysis.json').write_text(json.dumps(dict(runs=records,comparisons=comparisons,identity=identity),indent=2))
for name,r in records.items():print(name,{k:v for k,v in r.items() if k not in ['status_position_sequence','log_sha256']})
print('differing observations',[(c['mode'],c['repeat'],len(c['differences'])) for c in comparisons])
