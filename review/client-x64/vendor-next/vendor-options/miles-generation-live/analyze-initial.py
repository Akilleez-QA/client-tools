"""Unchanged guard oracle for guarded and diagnostic-bypass logs.
--validate LOG exits 1 on guard violations, including expected mutant failures.
Default checks the entire six-run experiment, including discrimination/cleanup.
"""
from pathlib import Path
import json,re,hashlib,struct,sys
B=Path(__file__).resolve().parent
OPS=[1,2]+[v for _ in range(20) for v in [3,4,5]]+[6,7,1,4,4,7,8]
GENS=[1]*64+[2,1,2,2,3]
def row(line):
 d=dict(re.findall(r'(\w+)=([^\s]+)',line))
 return {k:(v if k in ['phase','loaded','mode'] else int(v,16) if k in ['cw','sw','mx','handle'] else int(v)) for k,v in d.items()}
def eos_context(e,pairs):
 """Check active window only for active callbacks; BETWEEN uses adjacent boundaries."""
 last=e['observed_last_id'];active=e['active_id'];t=e['qpc']
 assert e['observed_last_op']==OPS[last-1]
 if active:
  assert active==last and e['active_op']==OPS[active-1]
  assert pairs[active][0]['qpc']<=t<=pairs[active][1]['qpc']
  location='ACTIVE'
 else:
  assert e['active_op']==0 and pairs[last][1]['qpc']<=t
  if last<69:assert t<=pairs[last+1][0]['qpc']
  location='BETWEEN'
 return location

def analyze(path):
 text=path.read_text();lines=text.splitlines()
 replies=[row(l) for l in lines if l.startswith('reply ')]
 normal=[r for r in replies if r['kind']==0];notifications=[r for r in replies if r['kind']==1]
 events=[row(l) for l in lines if l.startswith('event ')]
 audit=[row(l) for l in lines if l.startswith('audit ')]
 summaries=[row(l) for l in lines if l.startswith('summary ')];assert len(summaries)==1
 summary=summaries[0]
 assert [r['id'] for r in normal]==list(range(1,70))
 assert [e['seq'] for e in events]==list(range(139))
 assert all(a['qpc']<=b['qpc'] for a,b in zip(events,events[1:]))
 assert len(audit)==138
 pairs={};audits={}
 for i,(op,gen) in enumerate(zip(OPS,GENS),1):
  pair=[e for e in events if not e['eos'] and e['active_id']==i]
  assert len(pair)==2 and all(e['active_op']==op and e['observed_last_id']==i for e in pair)
  pairs[i]=pair
  a,z=audit[(i-1)*2:i*2];audits[i]=(a,z)
  assert a['phase']=='begin' and z['phase']=='end'
  assert all(v['id']==i and v['op']==op and v['request_gen']==gen for v in [a,z])
  assert pair[0]['qpc']<=a['qpc']<=z['qpc']<=pair[1]['qpc']
  if i>1:
   prev=audits[i-1][1]
   assert all(a[k]==prev[k] for k in ['current_gen','handle','lifetime','vendor','statuscalls','creates','releases','starts'])
  expected_gen=1 if i<=64 else 2 if i<=68 else 3
  assert a['current_gen']==expected_gen
  assert normal[i-1]['gen']==(expected_gen+1 if op==7 else expected_gen)
  if op==1:
   assert a['handle']==0 and a['lifetime']==0 and z['handle']!=0 and z['lifetime']==gen
  elif op==7:
   assert a['handle']!=0 and a['lifetime']==gen and z['handle']==0 and z['lifetime']==0
  elif op!=8:
   assert a['handle']!=0 and z['handle']==a['handle'] and a['lifetime']==z['lifetime']==expected_gen
  delta=z['vendor']-a['vendor'];sd=z['statuscalls']-a['statuscalls']
  if i!=66:
   expected= (4 if 'sample' in path.name else 3) if op==1 else 0 if op==8 else 1
   assert delta==expected and sd==(1 if op==4 else 0)
   assert normal[i-1]['result']==0
  assert z['creates']-a['creates']==(1 if op==1 else 0)
  assert z['releases']-a['releases']==(1 if op==7 else 0)
  assert z['starts']-a['starts']==(1 if op==2 else 0)
 assert summary['ok']==1 and summary['generation']==3 and summary['live']==0
 assert summary['creates']==summary['releases']==2 and summary['starts']==1
 assert summary['events']==139 and summary['eos']==1
 assert summary['vendor']==audits[69][1]['vendor'] and summary['statuscalls']==audits[69][1]['statuscalls']
 assert any(r['status']==2 for r in normal[:62]);assert normal[61]['total']==normal[61]['pos']==204
 assert normal[66]['status']>=0
 requests=[row(l) for l in lines if l.startswith('request ')]
 if requests:
  assert [(r['id'],r['op'],r['generation']) for r in requests]==[(i,op,gen) for i,(op,gen) in enumerate(zip(OPS,GENS),1)]
  assert 'controller replies=69 events=1 host_exit=0 ok=1 oracle=' in text
 eos=[e for e in events if e['eos']];assert len(eos)==len(notifications)==1
 e=eos[0];n=notifications[0];assert n['event']==e['seq'] and n['end']>=e['qpc']
 idx=replies.index(n);assert replies[idx+1]['id']==n['id'] and replies[idx+1]['kind']==0
 freq=int(re.search(r'frequency=(\d+)',text)[1]);assert freq>0
 if requests:assert int(re.search(r'controller-frequency=(\d+)',text)[1])==freq
 context=eos_context(e,pairs)
 a,z=audits[66];violations=[]
 if normal[65]['result']!=1:violations.append('stale request accepted')
 if z['vendor']!=a['vendor']:violations.append('stale request called vendor')
 if z['statuscalls']!=a['statuscalls']:violations.append('stale request called STATUS')
 return dict(violations=violations,accepted=not violations,summary=summary,
  stale=dict(request_generation=a['request_gen'],live_generation=a['current_gen'],handle=a['handle'],lifetime=a['lifetime'],result=normal[65]['result'],status=normal[65]['status'],vendor_delta=z['vendor']-a['vendor'],status_delta=z['statuscalls']-a['statuscalls']),
  current=dict(request_generation=audits[67][0]['request_gen'],status=normal[66]['status'],vendor_delta=audits[67][1]['vendor']-audits[67][0]['vendor']),
  eos=dict(location=context,active_command=e['active_id'],observed_last_command=e['observed_last_id'],sequence=e['seq'],thread=e['tid'],main_thread=events[0]['tid'],on_main_thread=e['tid']==events[0]['tid'],cw=e['cw'],sw=e['sw'],mx=e['mx'],delivery_request=n['id'],since_first_command_ms=(e['qpc']-events[0]['qpc'])/freq*1000,since_observed_last_begin_ms=(e['qpc']-pairs[e['observed_last_id']][0]['qpc'])/freq*1000,since_observed_last_end_ms=(e['qpc']-pairs[e['observed_last_id']][1]['qpc'])/freq*1000,delivery_observation_ms=(n['end']-e['qpc'])/freq*1000),
  getter_vector=[(r['id'],r['status'],r['total'],r['pos']) for r,op in zip(normal,OPS) if op in [4,5]],
  log_sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def main():
 if len(sys.argv)==3 and sys.argv[1]=='--validate':
  r=analyze(Path(sys.argv[2]));print(json.dumps(r,indent=2));return 0 if r['accepted'] else 1
 root=B/'rawlogs';result=json.loads((root/'results.json').read_text())
 assert not result.get('failure') and len(result['runs'])==6
 assert result['defaults_unchanged'] and result['sink_removed'] and result['private_wineserver_stop']==result['private_wineserver_wait']==0
 assert 'owned_native_scratch_exists=False' in (B/'native-cleanup.log').read_text()
 records={}
 for run in result['runs']:
  label=run['label'];mutant=label.startswith('mutant')
  assert run['returncode']==(9 if mutant else 0) and not run.get('timed_out')
  assert any(x['inputs'] for x in run['routing'])
  r=analyze(root/(label+'.log'));records[label]=r
  assert r['summary']['bypass']==int(mutant)
  assert r['violations']==(['stale request accepted','stale request called vendor','stale request called STATUS'] if mutant else [])
  if mutant:assert r['stale']['vendor_delta']==r['stale']['status_delta']==1 and r['stale']['status']>=0
 comparisons=[]
 for mode in ['sample','stream']:
  a=records['direct-'+mode];b=records['controlled-'+mode]
  comparisons.append(dict(mode=mode,getter_differences=[dict(direct=x,controlled=y) for x,y in zip(a['getter_vector'],b['getter_vector']) if x!=y],eos_context_and_timing_differences={k:dict(direct=a['eos'][k],controlled=b['eos'][k]) for k in a['eos'] if a['eos'][k]!=b['eos'][k]}))
 identities={}
 for name,machine in [('host.exe',0x14c),('controller.exe',0x8664)]:
  data=(B/name).read_bytes();actual=struct.unpack_from('<H',data,struct.unpack_from('<I',data,0x3c)[0]+4)[0];assert actual==machine
  identities[name]=dict(machine=actual,sha256=hashlib.sha256(data).hexdigest())
 prior=json.loads((B/'prior-evidence-hashes.json').read_text())
 assert all(hashlib.sha256((B.parent/'miles-rpc-contract'/n).read_bytes()).hexdigest()==h for n,h in prior.items())
 output=dict(runs=records,comparisons=comparisons,identity=identities,prior_evidence_unchanged=True)
 (B/'analysis.json').write_text(json.dumps(output,indent=2))
 print(json.dumps(dict(outcome='four guarded passes; two diagnostic oracle failures detected',comparisons=comparisons),indent=2));return 0
if __name__=='__main__':sys.exit(main())
