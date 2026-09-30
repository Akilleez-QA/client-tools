from pathlib import Path
import re,json,hashlib,math
b=Path(__file__).resolve().parent
runs=json.loads((b/'run-v1/results.json').read_text())
rows=[]
for run in runs['runs']:
 text=(b/'run-v1'/ (run['label']+'.log')).read_text(errors='replace')
 def fields(kind):
  line=next((l for l in text.splitlines() if l.startswith(kind+' ')),None)
  return dict((k,int(v)) for k,v in re.findall(r'(\w+)=(-?\d+)',line or ''))
 c=fields('completion');s=fields('observer_summary');e=fields('event')
 obs=[tuple(map(int,m)) for m in re.findall(r'observer epoch=(\d+) qpc=(\d+) seen=(\d+)',text)]
 row={'label':run['label'],'returncode':run['returncode'],'producer_observed':run.get('producer_observed'), 'completion':c,'observer_summary':s,'event':e,'observer_count':len(obs)}
 if s and c:
  freq=s['frequency'];first=s['first'];start=s['start'];cb=c['callback']
  row.update(callback_from_start_ms=(cb-start)*1000/freq,publish_delay_ms=(s['published']-cb)*1000/freq, first_seen_delay_ms=(obs[first][1]-cb)*1000/freq if first>=0 else None, maximum_observer_gap_ms=max((obs[i][1]-obs[i-1][1])*1000/freq for i in range(1,len(obs))), max_epoch_lateness_ms=max((t-start)*1000/freq-i-s['phase_us']/1000 for i,t,v in obs), callback_first_scheduled_epoch=(cb-start)*1000/freq-s['phase_us']/1000)
  row['first_scheduled_epoch_at_or_after_callback']=math.ceil(row['callback_first_scheduled_epoch'])
  row['additional_epochs_to_first_seen']=first-row['first_scheduled_epoch_at_or_after_callback']
  row['structural_ok']=run['returncode']==0 and run.get('producer_observed') and len(obs)==600 and [o[0] for o in obs]==list(range(600)) and c.get('count')==1 and c.get('status')==2 and c.get('pos')==204 and c.get('total')==204 and first>=0 and all(v==0 for _,_,v in obs[:first]) and all(v==1 for _,_,v in obs[first:]) and row['publish_delay_ms']>=0
 else: row['structural_ok']=False
 rows.append(row)
summary={'runs_expected':24,'runs_recorded':len(rows),'structural_passes':sum(bool(r['structural_ok']) for r in rows),'rows':rows,'cleanup':{k:runs.get(k) for k in ['defaults_unchanged','sink_removed','unload','private_wineserver_stop']}}
for arm in ['direct','queued','unsolicited']:
 vals=[r for r in rows if r['label'].startswith(arm+'-') and 'publish_delay_ms' in r]
 summary[arm]={k:[min(r[k] for r in vals),max(r[k] for r in vals)] for k in ['publish_delay_ms','first_seen_delay_ms','maximum_observer_gap_ms','max_epoch_lateness_ms']} if vals else {}
(b/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='rows'},indent=2))
